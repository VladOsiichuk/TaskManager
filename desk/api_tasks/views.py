from desk.model import Column, Desk, Task, Comment
from .serializers import CreateTaskSerializer, UpdateTaskSerializer
from rest_framework import generics
from rest_framework import mixins, permissions
from rest_framework.authentication import SessionAuthentication
from api_rules.permissions import IsEditorOfDeskOrHigher
from rest_framework import status
from rest_framework.response import Response
from desk.api_comments.serializers import CommentSerializer
from desk.actions.actions_data import get_columns_and_users, get_comments


class TaskAPIView(generics.CreateAPIView,
                  generics.ListAPIView
                  ):

    permission_classes = [permissions.IsAuthenticated, IsEditorOfDeskOrHigher]
    authentication_classes = [SessionAuthentication]
    serializer_class = CreateTaskSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'task_id'
#    queryset = Task.objects.all()

    def get_queryset(self, *args, **kwargs):

        #print(self.kwargs['id'])
        qs = Task.objects.prefetch_related('comments').filter(related_column_id=self.kwargs['column_id'])
        return qs # self.queryset.filter(related_column_id=self.kwargs['column_id'])

    def perform_create(self, serializer):
        column_id = self.kwargs["column_id"]
        return serializer.save(related_column_id=column_id)

    def post(self, request, *args, **kwargs):
        """
        Creates a new Task.
        """

        # create Task object
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        # add users and columns for task
        data = get_columns_and_users(self.kwargs['desk_id'], serializer.data)

        # return success response
        return Response(data, status=201)


class TaskDetailAPIView(mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.RetrieveAPIView,
                        ):

    permission_classes = [permissions.IsAuthenticated, IsEditorOfDeskOrHigher]
    authentication_classes = [SessionAuthentication]

    queryset = Task.objects.prefetch_related("comments__author").all()

    lookup_field = 'id'
    lookup_url_kwarg = 'task_id'
    serializer_class = UpdateTaskSerializer
    # prefetch_related("comments")

    def retrieve(self, request, *args, **kwargs):
        """
        Get information about task with ID=task_id. If Task is not related to the
        Column with ID=column_id then 404 error
        """
        instance = Task.objects.select_related("current_executor", "related_column").filter(id=self.kwargs["task_id"]).first()

        # self.check_object_permissions(self.request, instance)

        if instance is None:
            return Response({"detail": "not found"}, status=404)

        serializer = self.get_serializer(instance)
        new_data = get_columns_and_users(self.kwargs['desk_id'], serializer.data)
        new_data['current_executor'] = {"id": instance.current_executor.id, "username": instance.current_executor.username}

        new_data = get_comments(new_data, self.kwargs[self.lookup_url_kwarg])
        return Response(new_data)

    def put(self, request, *args, **kwargs):
        return Response({"message": "please use PATCH method instead"}, status=400)

    def patch(self, request, *args, **kwargs):
        """
        Updates the Task. Allowed only to EDITOR, ADMIN and person for who task is assigned
        """
        partial = kwargs.pop('partial', False)

        instance = Task.objects.prefetch_related("comments").filter(id=self.kwargs["task_id"]).first()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def delete(self, request, *args, **kwargs):
        """
        Delete task which has task_id
        """
        return self.destroy(request, *args, **kwargs)
