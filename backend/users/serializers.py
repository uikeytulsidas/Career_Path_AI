from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Chat, Message
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','password']
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "chat", "sender", "text", "skills", "recommendations", "created_at"]
        read_only_fields = ["id", "created_at","sender"]


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ["id", "title", "user", "created_at", "messages"]
        read_only_fields = ["id", "created_at", "messages","user"]

# class MessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Message
#         fields = ["id", "chat", "sender", "text", "skills", "recommendations", "created_at"]
#         read_only_fields = ["id", "created_at"]


# Sidebar chats should NOT include messages (prevents duplication)
# class ChatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Chat
#         fields = ["id", "title", "user", "created_at"]
#         read_only_fields = ["id", "created_at","user"]

