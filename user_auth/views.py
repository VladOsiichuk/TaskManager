from django.conf import settings
from rest_framework import viewsets, mixins
from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth import get_user_model, login, logout, authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from django.db.models import Q

from rest_framework import permissions

User = get_user_model()


class UserRegisterAPIView(generics.CreateAPIView):
    """
    create:
    Create a new user instance
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserRegisterSerializer

    authentication_classes = []

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        email = request.POST["email"]
        password = request.POST["password"]

        # login user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AuthView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    authentication_classes = []

    def post(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return Response({'error': 'user is already authenticated'}, status=400)

        data = request.data

        email = data.get('email')
        password = data.get('password')

        user = authenticate(request, email=email, password=password)

        # check this one
        # --------------------
        qs = User.objects.filter(
            Q(username__iexact=email) |
            Q(email__iexact=email)
        )

        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                login(request, user)
                return Response({"status": "Successfully authenticated. See cookie"}, status=200)
        # ---------------------
        return Response({"error": "invalid credentials"}, status=401)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #
    #     headers = self.get_success_headers(serializer.data)
    #     email = request.POST["email"]
    #     password = request.POST["password"]
    #
    #     # login user
    #     user = authenticate(request, email=email, password=password)
    #
    #     if user is not None:
    #         login(request, user)
    #
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
