from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('_nested_admin/', include('nested_admin.urls')),
]