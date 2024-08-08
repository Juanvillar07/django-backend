from rest_framework import serializers
from .models import Tarea, Usuario


class TareasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        #fields = ('id', 'titulo', 'descripcion', 'completada', 'fecha_creacion')
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()