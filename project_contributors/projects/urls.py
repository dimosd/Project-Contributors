from django.urls import path
from .views import CreateProject, RemoveProject, CompleteProject, OpenProjects, SendCollaboration, SeeCollaborationOffers, HandleCollaborationOffers


urlpatterns = [
    path('create_project/', CreateProject.as_view(), name="create_project"),
    path('remove_project/', RemoveProject.as_view(), name="remove_project"),
    path('open_projects/', OpenProjects.as_view(), name="open_projects"),
    path('complete_project/', CompleteProject.as_view(), name="complete_project"),
    path('collaboration_offer/', SendCollaboration.as_view(), name="collaboration_offer"),
    path('collaboration_offers/', SeeCollaborationOffers.as_view(), name="collaboration_offers"),
    path('handle_collaboration_offer/', HandleCollaborationOffers.as_view(), name="handle_collaboration_offer"),
    path('statistics/', RemoveProject.as_view(), name="open_projects"),
]