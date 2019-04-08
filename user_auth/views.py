from api_rules.permissions import PermissionRow
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from django.contrib.auth import get_user_model, login, logout, authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse
from rest_framework import permissions

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

        # write user's data in cookie
        user_data = {
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name
        }

        response = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        response = set_users_cookie(user_data, response)

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
        print(request.user.is_active)
        if request.user.is_active:
            return Response({'detail': 'user is already authenticated'}, status=400)

        data = request.data

        email = data.get('email')
        password = data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:

            user_perms = PermissionRow.objects.filter(user=user)
            if user_perms.count() > 1:
                # cache permissions
                permission_dict = {perm.related_desk_id: perm.permission for perm in user_perms}

                cache.set(user.id, permission_dict, DEFAULT_TIMEOUT)

            login(request, user)
            user_data = {
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
            response = Response({
                "detail": "Successfully authenticated. See cookie",
                "user_data": user_data
            }, status=200)
            

            response = set_users_cookie(user_data, response)
            return response

        return Response({"error": "invalid credentials"}, status=401)

def set_users_cookie(user_data, response):
    response.set_cookie("email", user_data["email"])
    response.set_cookie("username", user_data["username"])
    response.set_cookie("first_name", user_data["first_name"])
    response.set_cookie("last_name", user_data["last_name"])

    return response