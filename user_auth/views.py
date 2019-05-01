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
        response = Response(set_users_cookie(user, request), status=status.HTTP_201_CREATED, headers=headers)
        response.set_cookie("username", user.username)
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
            
            #response = set_users_cookie(user, response, request)
            return response

        return Response({"error": "invalid credentials"}, status=401)


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
    #
    # domain = settings.SESSION_COOKIE_DOMAIN
    #
    # response.set_cookie("sessionid", user_data["sessionid"], domain=domain)
    # response.set_cookie("csrftoken", user_data["csrftoken"], domain=domain)
    # response.set_cookie("email", user_data["email"], domain=domain)
    # response.set_cookie("user_id", user_data["user_id"], domain=domain)
    # response.set_cookie("username", user_data["username"], domain=domain)
    # response.set_cookie("first_name", user_data["first_name"], domain=domain)
    # response.set_cookie("last_name", user_data["last_name"], domain=domain)
    #
    # return response


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
