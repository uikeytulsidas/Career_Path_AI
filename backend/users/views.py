from django.shortcuts import render

from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from analyzer.utils import extract_skill_and_recommendations
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status

User = get_user_model()


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "username": user.username})
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)





class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    
from rest_framework import viewsets, permissions
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user).order_by("-created_at")


    # def get_queryset(self):
    #     # Only return chats of the logged-in user
    #     return Chat.objects.filter(user=self.request.user).distinct()

    def perform_create(self, serializer):
        # Ensure the chat belongs to the current user
        serializer.save(user=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        return Message.objects.filter(chat__user=self.request.user).order_by("created_at")

    # def get_queryset(self):
    #     # Restrict messages to chats of the logged-in user
    #     return Message.objects.filter(chat__user=self.request.user)

    def perform_create(self, serializer):
        # Message must belong to a chat owned by the user
        chat = serializer.validated_data["chat"]
        if chat.user != self.request.user:
            raise PermissionError("You do not own this chat.")
        serializer.save()
        # serializer.save(sender="user")

