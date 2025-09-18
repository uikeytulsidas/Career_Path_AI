from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # how many tokens the user has consumed
    token_usage = models.IntegerField(default=0)

    # max tokens allowed (you can set 100, 150, etc.)
    token_limit = models.IntegerField(default=150)


class Chat(models.Model):
    """A chat session for a user (like a conversation)."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chats"
    )
    title = models.CharField(max_length=255, blank=True, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class Message(models.Model):
    """Messages inside a chat (user or AI)."""
    SENDER_CHOICES = (
        ("user", "User"),
        ("ai", "AI"),
    )

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    text = models.TextField(blank=True, null=True)
    skills = models.JSONField(blank=True, null=True)  # extracted skills
    recommendations = models.JSONField(blank=True, null=True)  # AI recommendations
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:30] if self.text else '...' }"
