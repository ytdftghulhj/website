import json

from django.contrib.auth import authenticate

from blog.serializers import *
from .models import *
from rest_framework import  viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError





class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class SubscriptionsViewSet(viewsets.ModelViewSet):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class RegistrUserView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get',  'post']

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        serializer = UserRegistrSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # self.http_method_names.append("GET")\

        serializer = UserRegistrSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class AuthUserView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def create(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid()

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        try:
            user = CustomUser.objects.get(email=email)
        except Exception as e:
            raise ValidationError({"400": f'Такого аккаунта нет'})
        user = authenticate(username=email, password=password, request=request)
        if user is not None:
            return Response({'user': user.email}, status=status.HTTP_200_OK)
        else:
            raise ValidationError({"400": f'Данные не найдены'})
