from users.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.core.validators import MaxValueValidator, MinValueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField()
    age = serializers.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    country = serializers.CharField()
    residence = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'age',
            'first_name',
            'last_name',
            'country',
            'residence'
        )


class UserLoginSerializer(serializers.ModelSerializer):


    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )


class ResetSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()


    class Meta:
        model = User
        fields = (
            'username',
            'old_password',
            'new_password',
        )

