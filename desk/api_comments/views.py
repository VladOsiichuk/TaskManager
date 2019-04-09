from desk.model import Column, Desk, Task, Comment
from .serializers import CommentSerializer, CreateCommentSerializer
from rest_framework import generics
from rest_framework import mixins, permissions
from rest_framework.authentication import SessionAuthentication
from api_rules.permissions import IsStaffOfDeskOrHigher
from rest_framework.response import Response
from api_rules.permissions import IsStaffOfDeskOrHigher
from redis_manager.comments_cache_manager import CommentCacheManager


class CommentAPIView(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticated, IsStaffOfDeskOrHigher]
    authentication_classes = [SessionAuthentication]
    serializer_class = CommentSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'
    paginator = None

    def get_queryset(self, *args, **kwargs):
        return Comment.objects.prefetch_related("related_comment__related_comment__related_comment").all()

    def get(self, request, *args, **kwargs):

        # desk = Desk.objects.prefetch_related("permissionrow_set").filter(id=self.kwargs['desk_id']).first()
        # self.check_object_permissions(self.request, desk)
        #data = CommentCacheManager.get_comments_from_cache(related_task_id=self.kwargs["task_id"])
        #return Response(data)
        queryset = self.filter_queryset(self.get_queryset()).filter(is_child=False, related_task_id=self.kwargs['task_id'])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
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
        comment = serializer.data
        #CommentCacheManager.update_comments_in_cache(related_task_id=self.kwargs["task_id"], new_data=comment)
        
        # return success response
        return Response(comment, status=201)

