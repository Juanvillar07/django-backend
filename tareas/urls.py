from django.urls import path, include
from rest_framework import routers
from tareas import views

router = routers.DefaultRouter()
router.register(r"tareas", views.TareaView, 'tareas')

urlpatterns = [
    path("api/v1/", include(router.urls))
]

