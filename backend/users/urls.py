from django.urls import path
from .views import RegisterView, LoginView, ChatViewSet, MessageViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('chats/', ChatViewSet.as_view({'get': 'list', 'post': 'create'}), name='chat-list'),
    path('chats/<int:pk>/', ChatViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='chat-detail'),
    path('messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='message-list'),
]
