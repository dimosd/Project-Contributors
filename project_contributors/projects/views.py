import ast
from users.models import User
from django.http import response
from rest_framework import generics
from django.db.models.expressions import F
from rest_framework.response import Response
from django.http.response import JsonResponse
from .models import Project, CollaborationOffer
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from .serializers import CreateProjectSerializer, RemoveProjectSerializer, CompleteProjectSerializer, SendCollaborationSerializer, HandleCollaborationSerializer


@method_decorator(login_required, name='dispatch')
class CreateProject(generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = CreateProjectSerializer
    
    def post(self, request, *args, **kwargs):
        serializer_class = CreateProjectSerializer(data=request.data)
        user = User.objects.get(username=request.session.get("username"))
        if serializer_class.is_valid(raise_exception=True):
            if Project.objects.filter(project_name=serializer_class.data["project_name"]).exists():
                return Response(f"Your project:{serializer_class.data['project_name']} already exists."
                                , status=HTTP_200_OK)
            project = Project(
                    project_name=serializer_class.data["project_name"],
                    description=serializer_class.data["description"],
                    maximum_collaborators=serializer_class.data["maximum_collaborators"],
                    collaborators=serializer_class.data["collaborators"],
                    created_user_id = user.pk
                )
            project.save()
            return Response(f"Your project:{serializer_class.data['project_name']} has been created successfuly!"
                            , status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class RemoveProject(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RemoveProjectSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = RemoveProjectSerializer(data=request.data)
        user = User.objects.get(username=request.session.get("username"))
        if serializer_class.is_valid(raise_exception=True):
            project = Project.objects.filter(project_name=serializer_class.data["project_name"], created_user_id=user.pk).exists()
            if project:
                project = Project.objects.get(project_name=serializer_class.data["project_name"], created_user_id=user.pk)
                project.delete()
                return Response(f"Your project:{serializer_class.data['project_name']} has been deleted successfuly!"
                                , status=HTTP_200_OK)
            return Response(f"Your project:{serializer_class.data['project_name']} not exists."
                , status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class CompleteProject(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RemoveProjectSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = CompleteProjectSerializer(data=request.data)
        user = User.objects.get(username=request.session.get("username"))
        if serializer_class.is_valid(raise_exception=True):
            project = Project.objects.filter(project_name=serializer_class.data["project_name"], created_user_id=user.pk).exists()
            if project:
                project = Project.objects.filter(project_name=serializer_class.data["project_name"], created_user_id=user.pk)
                project.update(project_status=serializer_class.data['status'])
                return Response(f"Your project:{serializer_class.data['project_name']} has been upated successfuly!"
                                , status=HTTP_200_OK)
            return Response(f"Your project:{serializer_class.data['project_name']} not exists."
                , status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class OpenProjects(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        qs = Project.objects.annotate(open_seats=(F('maximum_collaborators')-F('collaborators')))
        projects = list(qs.filter(open_seats__gt=0, project_status="In progress").values())
        return JsonResponse(projects, safe=False)

@method_decorator(login_required, name='dispatch')
class SendCollaboration(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        serializer_class = SendCollaborationSerializer(data=request.data)
        user = User.objects.get(username=request.session.get("username"))
        
        if serializer_class.is_valid(raise_exception=True):
            project = Project.objects.filter(project_name=serializer_class.data["project_name"]).exists()
            
            if project:
                project_info = Project.objects.get(project_name=serializer_class.data["project_name"])
                if project_info.maximum_collaborators < project_info.collaborators:
                    return Response(f"Seats for collaboration offers for project:{serializer_class.data['project_name']} closed."
                                , status=HTTP_200_OK)
                if CollaborationOffer.objects.filter(project_name=serializer_class.data["project_name"], user=user).exists():
                    return Response(f"Your have already send collaboration offer for project:{serializer_class.data['project_name']}"
                                , status=HTTP_200_OK)
                collaboration_offer = CollaborationOffer(
                    project_name = serializer_class.data["project_name"],
                    user = user
                )
                collaboration_offer.save()
                return Response(f"Your collaboration offer for project:{serializer_class.data['project_name']} has been added successfuly!"
                                , status=HTTP_200_OK)
            return Response(f"Project:{serializer_class.data['project_name']} not exists any more."
                , status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class SeeCollaborationOffers(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        serializer_class = SendCollaborationSerializer(data=request.data)
        user = User.objects.get(username=request.session.get("username"))
        if serializer_class.is_valid(raise_exception=True):
            project = Project.objects.filter(project_name=serializer_class.data["project_name"]).exists()
            if project:
                project_info = Project.objects.get(project_name=serializer_class.data["project_name"])
                if project_info.created_user_id != user.pk:
                    return Response(f"You must be the creator of project:{serializer_class.data['project_name']} in order to see collaboration offers."
                                , status=HTTP_401_UNAUTHORIZED)
                offers = CollaborationOffer.objects.filter(project_name=serializer_class.data["project_name"])
                profiles = []
                for offer in offers:
                    user_profile = {
                        "username": offer.user.username,
                        "email": offer.user.email,
                        "skills": offer.user.skills
                    }
                    profiles.append(user_profile)
                return Response(profiles, status=HTTP_200_OK)
            return Response(f"Project:{serializer_class.data['project_name']} not exists any more."
                , status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class HandleCollaborationOffers(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        serializer_class = HandleCollaborationSerializer(data=request.data)
        user = User.objects.get(username=request.session.get("username"))
        if serializer_class.is_valid(raise_exception=True):
            contributor = User.objects.filter(username=serializer_class.data["contributor_name"])
            offer = CollaborationOffer.objects.filter(user__username=serializer_class.data["contributor_name"]).exists()
            project = Project.objects.filter(created_user_id=user.pk)
            if offer:
                project_info = Project.objects.get(created_user_id=user.pk)
                if project_info.created_user_id != user.pk:
                    return Response(f"You must be the creator of project:{project_info.project_name} in order to handle collaboration offers."
                                , status=HTTP_401_UNAUTHORIZED)
                offer = CollaborationOffer.objects.filter(user__username=serializer_class.data["contributor_name"])
                if serializer_class.data["action"] == "accept":
                    offer.delete()
                    project.update(collaborators = project_info.collaborators + 1)
                    return Response("Offer successfully accepted.", status=HTTP_200_OK)
                else:
                    offer.delete()
                    return Response("Offer successfully denied.", status=HTTP_200_OK)
            return Response(f"Offer not exists any more.")
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)
