from django.urls import path
from .views import BotUserApiView, BotUserListApiView, BotUpdateView, VerifyCodeView

urlpatterns = [
    path('verify-code/', VerifyCodeView.as_view(), name='verify_code'),
    path('bot-users/', BotUserApiView.as_view(), name='bot-users'),
    path('bot-users/list/', BotUserListApiView.as_view(), name='bot-users-list'),
    path('bot-users/update/<str:user_id>/', BotUpdateView.as_view(), name='bot-users-update'),
]
