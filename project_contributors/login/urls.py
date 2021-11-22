from django.urls import path
from .views import Record, Login, Logout, Reset


urlpatterns = [
    path('add_user/', Record.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('reset_password/', Reset.as_view(), name="reset")
]