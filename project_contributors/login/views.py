from users.models import User
from rest_framework import generics
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login, authenticate
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from .serializers import UserSerializer, UserLoginSerializer, ResetSerializer


class Record(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            User.objects.create_user(
                            username=serializer_class.data["username"],
                            email=serializer_class.data["email"],
                            password=serializer_class.data["password"],
                            age=serializer_class.data["age"],
                            first_name=serializer_class.data["first_name"],
                            last_name=serializer_class.data["last_name"],
                            country=serializer_class.data["country"],
                            residence=serializer_class.data["residence"]
                        )
            return Response(f"Hello {serializer_class.data['username'].capitalize()}. You have been registered successfully!"
                            , status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Login(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            user = authenticate(username=serializer_class.data["username"], password=serializer_class.data["password"])
            if user:
                login(request, user)
                request.session["username"] = serializer_class.data["username"]
                return Response(f"{user.get_username().capitalize()} successfully logged in!", status=HTTP_200_OK)
            return Response(f"Wrong credentials for user: {serializer_class.data['username']}. Try again", status=HTTP_401_UNAUTHORIZED)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class Logout(generics.GenericAPIView):


    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(f"You are logged out from Project-contributors platform. Hope to see you again!", status=HTTP_200_OK)

@method_decorator(login_required, name='dispatch')
class Reset(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ResetSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = ResetSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            user = authenticate(username=serializer_class.data["username"], password=serializer_class.data["old_password"])
            if user:
                user.set_password(serializer_class.data["new_password"])
                user.save()
                return Response(f"{user.capitalize()}, your password has changed successfully!", status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)
