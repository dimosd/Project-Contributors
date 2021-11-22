from django.db import models
from django.conf import settings
from django.db.models.enums import Choices



class Project(models.Model):
    

    project_name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)
    maximum_collaborators = models.IntegerField(null=True, default=0)
    collaborators = models.IntegerField(null=True, default=0)
    created_user_id = models.IntegerField(null=True)
    project_status = models.CharField(max_length=255, null=True, default="In progress")
    collaborators_ids = models.CharField(max_length=255, null=True, default="[]")
 
class CollaborationOffer(models.Model):


    project_name = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)