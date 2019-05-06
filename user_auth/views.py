from api_rules.permissions import PermissionRow
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from django.contrib.auth import get_user_model, login, logout, authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from redis_manager.permission_cache_manager import PermissionCacheManager
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.views import APIView
from django.conf import settings
from django.middleware.csrf import get_token
from django.core.mail import send_mail

User = get_user_model()


class UserAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
        print("register works...")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        data = request.data
        email = data.get('email')
        password = data.get('password')
        # login user
        user = authenticate(request, email=email, password=password)

        login(request, user)
        print(request.session.session_key)
        # write user's data in cookie
        send(request, email)
        response = Response(set_users_cookie(user, request), status=status.HTTP_201_CREATED, headers=headers)
        response.set_cookie("username", user.username, domain="protected-mountain-24825.herokuapp.com")
        return response


class AuthAPIView(generics.CreateAPIView):
    """
    View to login
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    authentication_classes = []

    def post(self, request, *args, **kwargs):
        print("login works....")
        if request.user.is_active:
            return Response({'detail': 'user is already authenticated'}, status=400)

        data = request.data

        email = data.get('email')
        password = data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:

            PermissionCacheManager.set_user_perms_in_cache(user.id)
                
            login(request, user)
            
            response = Response(set_users_cookie(user, request), status=200)
            print("view...")
            #response = set_users_cookie(user, response, request)
            return response

        return Response({"error": "invalid credentials"}, status=400)


def set_users_cookie(user, request):

    user_data = {
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "sessionid": request.session.session_key,
                "csrftoken": get_token(request)
            }

    return user_data


class LogoutAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    authentication_classes = []

    def post(self, request):

        logout(request)
        response = Response({"detail": "Successfully logged out. See cookie"}, status=200)
        response.delete_cookie("email")
        response.delete_cookie("user_id")
        response.delete_cookie("username")
        response.delete_cookie("first_name")
        response.delete_cookie("last_name")

        return response


def send(request, email):

    subject = "Hi for registering"
    message = "This is message."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(
        subject=subject,
        message=message,
        from_email=email_from,
        recipient_list=recipient_list
    )
