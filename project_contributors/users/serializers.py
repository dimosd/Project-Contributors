from .models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError


class AddSkillsSerializer(serializers.ModelSerializer):
    added_skills = serializers.ListField()
    valid_skills = ['C++', 'Javascript,', 'Python', 'Java', 'Lua', 'Rust', 'Go', 'Julia']

    def validate(self, data):
        skills = data.get("added_skills", None)
        if len(skills)>3:
            raise ValidationError("At most 3 skills can be registered at any time.")
        for skill in skills:
            if skill not in self.valid_skills:
                raise ValidationError(f"Theese are the options of valid skills {self.valid_skills}")
        return data


    class Meta:
        model = User
        fields = (
            'added_skills',
        )

class RemoveSkillsSerializer(serializers.ModelSerializer):
    deleted_skills = serializers.ListField(required=True)


    class Meta:
        model = User
        fields = (
            'deleted_skills',
        )