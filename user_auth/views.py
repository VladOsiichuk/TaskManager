from django.conf import settings
from rest_framework import viewsets, mixins
from .serializers import UserSerializer
from django.contrib.auth import get_user_model, login, logout, authenticate
from rest_framework import status
from rest_framework.response import Response


class UserViewSet(viewsets.ViewSet,
                  mixins.CreateModelMixin,
                  # mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    """
    create:
    Create a new user instance
    """
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
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
