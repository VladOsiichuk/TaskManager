from django.core.cache import cache
from desk.model import Comment
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from desk.api_comments.serializers import CommentSerializer


class CommentCacheManager:
    """pass where comments will be saved in cache: cache.get('comments_related_task_id')"""
    ttl = settings.CACHE_TTL * 30 * 60
    key = 'comments_'

    @classmethod
    def get_comments_from_cache(self, related_task_id):
        comments = cache.get(self.key + str(related_task_id))
        print(type(comments))
        # if comments is None:
        #    return self.set_comments_in_cache(related_task_id)
        
        return comments if comments is not None else self.set_comments_in_cache(related_task_id)
        
    @classmethod
    def set_comments_in_cache(self, related_task_id):

        comments = Comment.objects.filter(related_task_id=related_task_id, is_child=False)
        
        serializer = CommentSerializer(comments, many=True)
        cache.set(self.key + str(related_task_id), serializer.data, self.ttl)

        return serializer.data

    # TODO: Nested comments are inserted incorrectly
    @classmethod
    def update_comments_in_cache(self, related_task_id, new_data):
        
        comment_data = cache.get(self.key + str(related_task_id))
        key = self.key + str(related_task_id)

        if comment_data is None:
            cache.set(key, new_data, self.ttl)
        
        else:
            comment_data.append(new_data)
            cache.set(key, comment_data, self.ttl)
        
        cache.expire(key, self.ttl)

        return comment_data or new_data


    @classmethod
    def is_cached(self, related_task_id):
        """Return True or False if comments for this task are cached"""
        data = cache.get(self.key + str(related_task_id))
        return True if data else False
