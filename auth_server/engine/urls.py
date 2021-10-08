from django.urls import path
from engine.views import (
    GenerateTokensView,
    RefreshTokenView
)

# Url patterns used to get and refresh tokens
urlpatterns = [
    # Accepts user credentials and responds with a pair of tokens
    path('login/', GenerateTokensView.as_view()),
    # Accepts refresh token and responds with new access token
    path('refresh/', RefreshTokenView.as_view()),
]
