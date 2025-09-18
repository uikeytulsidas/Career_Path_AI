from django.urls import path
from .views import GeminiAPIView
urlpatterns = [
    path('analyzer/', GeminiAPIView.as_view(), name='career-analysis'),
     path('gemini/', GeminiAPIView.as_view(), name='careerai'),
]