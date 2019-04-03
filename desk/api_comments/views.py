from desk.model import Column, Desk, Task, Comment
from .serializers import CommentSerializer, CreateCommentSerializer
from rest_framework import generics
from rest_framework import mixins, permissions
from rest_framework.authentication import SessionAuthentication
from api_rules.permissions import IsStaffOfDeskOrHigher
from rest_framework.response import Response


class CommentAPIView(
                     generics.ListAPIView
                     ):
    permission_classes = [permissions.IsAuthenticated, IsStaffOfDeskOrHigher]
    authentication_classes = [SessionAuthentication]
    serializer_class = CommentSerializer
    #lookup_field = 'id'
    #lookup_url_kwarg = 'comment_id'
    queryset = Comment.objects.prefetch_related("parent").all()

    def get_queryset(self, *args, **kwargs):

        return Comment.objects.filter(related_task_id=self.kwargs['task_id'], is_child=False)

    # def perform_create(self, serializer):
    #     task_id = self.kwargs["task_id"]
    #     return serializer.save(related_task_id=task_id, author=self.request.user)
    #
    # def post(self, request, *args, **kwargs):
    #
    #     # check if user has access to create a new comment
    #     task = Task.objects.prefetch_related("related_column__related_desk__permissionrow_set")
    #     .get(id=self.kwargs["task_id"])
    #
    #     # if provided task id is incorrect
    #     if not task:
    #         return Response({"error": "provided task id is incorrect"}, status=400)
    #
    #     self.check_object_permissions(request, task)
    #
    #     # # Check if selected column is related to the Current Desk
    #     # desk_id = self.kwargs["desk_id"]
    #     # related_column_id = self.kwargs["desk_id"]
    #     # col = Column.objects.get(id=related_column_id)
    #     #
    #     # # if desk_id is not the same as related_desk_id then return Bad Response
    #     # if col.related_desk_id != desk_id:
    #     #     return Response({"Message": f"Selected column(ID={related_column_id})"
    #     #     f" is not related to the desk with ID={related_column_id}"}, status=400)
    #
    #     # create Task object
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     self.perform_create(serializer)
    #
    #     # return success response
    #     return Response(serializer.data, status=201)


class CreateCommentAPIView(generics.CreateAPIView):

    permission_classes = [permissions.IsAuthenticated, IsStaffOfDeskOrHigher]
    authentication_classes = [SessionAuthentication]
    serializer_class = CreateCommentSerializer
    # lookup_field = 'id'
    # lookup_url_kwarg = 'comment_id'
    #queryset = Comment.objects.all()

    def perform_create(self, serializer):
        task_id = self.kwargs["task_id"]
        return serializer.save(related_task_id=task_id, author=self.request.user)

    def post(self, request, *args, **kwargs):

        # check if user has access to create a new comment
        task = Task.objects.prefetch_related("related_column__related_desk__permissionrow_set").get(id=self.kwargs["task_id"])

        # if provided task id is incorrect
        if not task:
            return Response({"error": "provided task id is incorrect"}, status=400)

        self.check_object_permissions(request, task)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        # return success response
        return Response(serializer.data, status=201)

