from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import AccessToken

from .models import Note
from .serializers import NoteSerializer,RegisterSerializer

User = get_user_model()

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request,username=email, password=password)
        if user is None:
            return Response({'error:Password is incorrect'},status = status.HTTP_401_UNAUTHORIZED)


        token = AccessToken.for_user(user)
        return Response({'access':str(token)},status=status.HTTP_200_OK)


class ListAddNotesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes,many=True)
        return Response({'notes':serializer.data},status=status.HTTP_200_OK)

    def post(self,request):
        serializer = NoteSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'note_id':serializer.instance.pk},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class DeleteNoteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,note_id):
        try:
            note = Note.objects.get(id=note_id)
            note.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)