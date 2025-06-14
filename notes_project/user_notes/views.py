from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import AccessToken


from .authentication import EmailJWTAuthentication
from .models import Note
from .serializers import NoteSerializer,RegisterSerializer

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request,username=email, password=password)
    if user is None:
        return Response({'error':'Password is incorrect'},status = status.HTTP_401_UNAUTHORIZED)

    token = AccessToken.for_user(user)
    token['user_id'] = user.email
    return Response({'access':str(token)},status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([EmailJWTAuthentication])
@permission_classes([IsAuthenticated])
def list_notes(request):
    notes = Note.objects.filter(user=request.user)
    serializer = NoteSerializer(notes,many=True)
    return Response({'notes':serializer.data},status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([EmailJWTAuthentication])
@permission_classes([IsAuthenticated])
def add_note(request):
    serializer = NoteSerializer(data=request.data,context={'request':request})
    if serializer.is_valid():
        serializer.save()
        return Response({'note_id':serializer.instance.pk},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([EmailJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_note(request):
    note_id = request.data.get('id')
    if not note_id:
        return Response({'error':'note_id is required'},status=status.HTTP_400_BAD_REQUEST)
    try:
        note = Note.objects.get(id=note_id)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)