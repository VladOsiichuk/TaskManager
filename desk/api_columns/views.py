from desk.model import Column
from .serializers import ColumnSerializer
from rest_framework import generics
from rest_framework import mixins, permissions
from rest_framework.authentication import SessionAuthentication
from api_rules.permissions import IsParticipantOfDesk


class ColumnAPIView(generics.ListAPIView,
                    mixins.CreateModelMixin):

    permission_classes = [permissions.IsAuthenticated, IsParticipantOfDesk]
    authentication_classes = [SessionAuthentication]
    serializer_class = ColumnSerializer
    passed_id = None
    queryset = Column.objects.all()
