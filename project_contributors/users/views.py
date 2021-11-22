import ast
from .models import User
from rest_framework import generics
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .serializers import AddSkillsSerializer, RemoveSkillsSerializer
from django.contrib.auth import authenticate

@method_decorator(login_required, name='dispatch')
class AddSkills(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = AddSkillsSerializer
    
    def post(self, request, *args, **kwargs):
        serializer_class = AddSkillsSerializer(data=request.data)
        user = User.objects.get(username=request.session.get("username"))
        if serializer_class.is_valid(raise_exception=True):
            current_skills = ast.literal_eval(user.skills)
            if not user.skills:
                user.skills = serializer_class.data["added_skills"]
            else:
                for skill in serializer_class.data["added_skills"]:
                    if skill in current_skills:
                        return Response(f"Skill {skill}, already registered.", status=HTTP_200_OK)
                    current_skills.append(skill)
            
            user.skills = current_skills
            user.save()
            return Response(f"Skills have beed added successfully.", status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class RemoveSkills(generics.GenericAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = RemoveSkillsSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = RemoveSkillsSerializer(data=request.data)
        user = User.objects.get(username=request.session.get("username"))
        if serializer_class.is_valid(raise_exception=True):
            current_skills = ast.literal_eval(user.skills)
            for skill in serializer_class.data["deleted_skills"]:
                if skill in current_skills:
                    current_skills.remove(skill)
                else:
                    return Response(f"Skill: {skill} has not been registered.", status=HTTP_200_OK)
            user.skills = current_skills
            user.save()
            return Response(f"Skills deleted success", status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)