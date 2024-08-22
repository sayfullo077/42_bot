from .models import BotUser
from .serializers import BotUserSerializer
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.views import APIView
from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response


class BotUserApiView(ListCreateAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer


class BotUserListApiView(APIView):
    def get(self, request):
        users = BotUser.objects.all()
        serializer = BotUserSerializer(users, many=True)
        return Response(serializer.data)
    
    
class BotUpdateView(RetrieveUpdateAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer
    lookup_field = 'user_id'

    def patch(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        instance = self.get_object()
        instance.created_at = timezone.now()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(TemplateView):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        try:
            user = BotUser.objects.get(code=code)
        except BotUser.DoesNotExist:
            return render(request, self.template_name, {"error": "Code is invalid"})

        if timezone.now() - user.created_at > timezone.timedelta(minutes=1):
            return render(request, self.template_name, {"error": "Code validation time has expired."})

        return render(request, self.template_name, {"success": "Code is valid."})