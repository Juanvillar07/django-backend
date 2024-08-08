from django.shortcuts import render
from rest_framework import viewsets
from .serializer import TareasSerializer
from .serializer import UsuarioSerializer
from .models import Tarea, Usuario

# Create your views here.


class TareaView(viewsets.ModelViewSet):
    serializer_class = TareasSerializer
    queryset = Tarea.objects.all()

class UsuarioView(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()
