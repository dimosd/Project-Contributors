from .models import Project
from rest_framework import serializers
from django.core.exceptions import ValidationError


class CreateProjectSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField()
    description = serializers.CharField()
    maximum_collaborators = serializers.IntegerField()
    collaborators = serializers.IntegerField()


    class Meta:
        model = Project
        fields = (
            'project_name',
            'description',
            'maximum_collaborators',
            'collaborators',
        )


class RemoveProjectSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField()


    class Meta:
        model = Project
        fields = (
            'project_name',
        )


class CompleteProjectSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField()
    status = serializers.ChoiceField(choices=["In progress", "Completed"])


    class Meta:
        model = Project
        fields = (
            'project_name',
            'status',
        )


class CompleteProjectSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField()
    status = serializers.ChoiceField(choices=["In progress", "Completed"])


    class Meta:
        model = Project
        fields = (
            'project_name',
            'status',
        )


class SendCollaborationSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField()


    class Meta:
        model = Project
        fields = (
            'project_name',
        )

class HandleCollaborationSerializer(serializers.ModelSerializer):
    contributor_name = serializers.CharField()
    action = serializers.ChoiceField(choices=["accept", "decline"])

    class Meta:
        model = Project
        fields = (
            'contributor_name',
            'action',
        )