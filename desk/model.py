from django.db import models
from django.core.serializers import serialize
#from django.contrib.auth import get_user_model
from django.conf import settings
import json


class DeskQuerySet(models.QuerySet):

    # def serialize(self):
    #     list_values = list(self.values('author', 'name', 'description'))
    #     return json.dumps(list_values)
    pass


class DeskManager(models.Manager):
    def get_queryset(self):
        return DeskQuerySet(self.model, using=self._db)


class Desk(models.Model):
    """
    class describing the desk
    @author: who created the desk
    @name: the name of the desk
    @description: short description of the desk
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=500)

    objects = DeskManager()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Desk post"
        verbose_name_plural = "Desk posts"

    # def serialize(self):
    #     data = {
    #         "id": self.id,
    #         "name": self.name,
    #         "author": self.author.id,
    #         "description": self.description
    #     }
    #
    #     data = json.dumps(data)
    #     return data


class Column(models.Model):
    """
    @related_desk: board to which is related this one
    @author: who created this one
    @order_in_desk: the order of column in the desk
    @name: title of column
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    related_desk = models.ForeignKey(Desk, on_delete=models.CASCADE)
    order_in_desk = models.IntegerField
    name = models.CharField(max_length=64)
    created = models.DateField(auto_now_add=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    """
    @author: who created this one
    @related_column: the column to which this one is related currently
    @current_executor: to who task is assigned
    @description: description
    @task_deadline: deadline of execution
    """

    related_column = models.ForeignKey(Column, on_delete=models.CASCADE)
    current_executor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    task_deadline = models.DateField(blank=True)

    def __str__(self):
        return f"{self.name}"


class Comment(models.Model):
    """
    @author: who created comment
    @comment_body: comment
    @related_task: for which task is this one
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_body = models.TextField(max_length=500)
    related_task = models.ForeignKey(Task, on_delete=models.CASCADE)

    # TODO
    # after add fields for img attaching or video attaching
