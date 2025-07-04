from django.urls import path
from .views import (RegisterView, profile_view,telegram_login_page, bot_login, claim_cipher,
                    CharacterListView, DailyTaskListView, CompleteTaskView, UserCharacterListCreateView,
                    SettingsAPIView, MiningActionView, MiningView, DailyHafezTaskView, complete_hafez_task,
                    AllTasksStatusView, BootsEnegry, UnlockSkinView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .bot_views import SendTelegramMessageView,MessageHistoryView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', profile_view, name='profile'),
    path('telegram_login_page/', telegram_login_page, name='telegram_login_page'),
    path('bot_login/', bot_login, name='bot_login'),
    path('characters/', CharacterListView.as_view(), name='character_list'),
    path('', views.index, name='index'),
    path('move/<int:row>/<int:col>/', views.move_tile, name='move'),
    path('reset/', views.reset_board, name='reset'),
    path('tasks/', DailyTaskListView.as_view(), name='daily-tasks'),
    path('tasks/<int:task_id>/complete/', CompleteTaskView.as_view(), name='complete-task'),
    path('user_characters/', UserCharacterListCreateView.as_view(), name='character-list-create'),
    path('user_characters/<int:pk>/increase_coins/', UserCharacterListCreateView.as_view()),
    path('settings/', SettingsAPIView.as_view(), name='settings-api'),
    path("send-message/", SendTelegramMessageView.as_view(), name="send-message"),
    path("chat-history/<int:user_id>/", MessageHistoryView.as_view(), name="chat-history"),
    path('profit/', views.ClaimProfitView.as_view(), name='profit'),
    path('claim-cipher/<int:pk>/', claim_cipher, name='claim_cipher'),
    path('mining/', MiningView.as_view(), name='mining-list'),  # GET all mining cards
    path('mining_card/', MiningActionView.as_view(), name='mining'),
    path('daily-hafez-task/', DailyHafezTaskView.as_view(), name='daily-hafez-task'),
    path('complete-hafez-task/', complete_hafez_task, name='complete-hafez-task'),
    path('task-status/', AllTasksStatusView.as_view(), name='task-status'),
    path('boost-energy/', BootsEnegry.as_view(), name='boost-energy'),
    path('unlock_skin/', UnlockSkinView.as_view(), name='unlock-skin'),




    
]
