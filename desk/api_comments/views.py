from desk.model import Column, Desk, Task, Comment
from .serializers import CommentSerializer, CreateCommentSerializer
from rest_framework import generics
from rest_framework import mixins, permissions
from rest_framework.authentication import SessionAuthentication
from api_rules.permissions import IsStaffOfDeskOrHigher
from rest_framework.response import Response
from api_rules.permissions import IsStaffOfDeskOrHigher


class CommentAPIView(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticated, IsStaffOfDeskOrHigher]
    authentication_classes = [SessionAuthentication]
    serializer_class = CommentSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self, *args, **kwargs):
        return Comment.objects.prefetch_related("related_comment__related_comment__related_comment").all()

    def get(self, request, *args, **kwargs):

        # desk = Desk.objects.prefetch_related("permissionrow_set").filter(id=self.kwargs['desk_id']).first()
        # self.check_object_permissions(self.request, desk)

        queryset = self.filter_queryset(self.get_queryset()).filter(is_child=False)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            print(type(serializer.data), len(serializer.data))
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CreateCommentAPIView(generics.CreateAPIView):

    permission_classes = [permissions.IsAuthenticated, IsStaffOfDeskOrHigher]
    authentication_classes = [SessionAuthentication]
    serializer_class = CreateCommentSerializer

    def perform_create(self, serializer):
        task_id = self.kwargs["task_id"]
        return serializer.save(related_task_id=task_id, author=self.request.user)

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        # return success response
        return Response(serializer.data, status=201)
