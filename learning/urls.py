from django.urls import path

from learning import views


urlpatterns = [
    path("learning/index.html", views.get_temp_here, name="temp_here"),
    path("learning/locationTemp.html", views.get_temp, name="temp"),
]