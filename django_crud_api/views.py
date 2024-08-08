from rest_framework.decorators import api_view
from rest_framework.response import Response
from tareas.serializer import UsuarioSerializer
from tareas.models import Usuario
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from django.shortcuts import get_object_or_404
import requests

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def register(request):
    serializer = UsuarioSerializer(data=request.data)   

    if serializer.is_valid():
        serializer.save()
        
        user = Usuario.objects.get(username=serializer.data['username'])
        user.save()
        
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
    
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def Access(request):

    user = get_object_or_404(Usuario, username=request.data['username'])

    if user.password != request.data['password']:
        return Response({'message': 'Credenciales invalidas'}, status=status.HTTP_400_BAD_REQUEST)

    
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({
            'refresh': str(refresh),
            'access': access_token
        }, status=status.HTTP_200_OK)



@api_view(['POST'])
def logout(request):
    
    token = request.data.get('refresh')

    if not token:
        return Response({'message': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        
        token_obj = RefreshToken(token)
        token_obj.blacklist() 
    except Exception as e:
        return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def perfil(request):

    print(request.user)

    return Response("Tu estas logueado {}".format(request.user.username), status=status.HTTP_200_OK)


@api_view(['GET'])
def recursos(request):
    url = 'http://consultas.cuc.edu.co/api/v1.0/recursos'
    headers = {
            'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6InBydWViYTIwMjJAY3VjLmVkdS5jbyIsImV4cCI6MTY0OTQ1MzA1NCwiY29ycmVvIjoicHJ1ZWJhMjAyMkBjdWMuZWR1LmNvIn0.MAoFJE2SBgHvp9BS9fyBmb2gZzD0BHGPiyKoAo_uYAQ'  # Reemplaza 'tu_token_aqui' con tu token real
        }

    try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Error al consumir la API externa'}, status=response.status_code)
    except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
