from django.urls import path
from .views import RegisterView, profile_view,telegram_login_page, bot_login, CharacterListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', profile_view, name='profile'),
    path('telegram_login_page/', telegram_login_page, name='telegram_login_page'),
    path('bot_login/', bot_login, name='bot_login'),
    path('characters/', CharacterListView.as_view(), name='character_list'),
]
