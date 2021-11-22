from django.urls import path
from .views import AddSkills, RemoveSkills


urlpatterns = [
    path('add_skills/', AddSkills.as_view(), name="add_skills"),
    path('remove_skills/', RemoveSkills.as_view(), name="remove_skills")
]