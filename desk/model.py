from django.db import models

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
    name = models.CharField(max_length=64, help_text="Title of the Desk")
    description = models.TextField(max_length=500, help_text='Description of the Desk')

    #objects = DeskManager()

    @property
    def desk_name(self):
        return self.name

    @property
    def desk_id(self):
        return self.id

    @property
    def desk_author(self):
        return self.author

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

    related_desk = models.ForeignKey(Desk, on_delete=models.CASCADE, help_text='ID of desk for which Column is related')
    name = models.CharField(max_length=64, help_text="Title of the Column")

    created = models.DateField(auto_now_add=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Column"
        verbose_name_plural = "Columns"

    @property
    def desk_name(self):
        return self.related_desk.name

    @property
    def desk_id(self):
        return self.related_desk.id

    @property
    def desk_author(self):
        return self.related_desk.author


class Task(models.Model):
    """
    @author: who created this one
    @related_column: the column to which this one is related currently
    @current_executor: to who task is assigned
    @description: description
    @task_deadline: deadline of execution
    """

    related_column = models.ForeignKey(Column, on_delete=models.CASCADE, help_text="ID of column for "
                                                                                   "who Task is related")
    current_executor = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                            help_text="ID of user for who task is assigned")
    name = models.CharField(max_length=64, help_text='Title of the task')
    description = models.TextField(max_length=500, help_text='Description of the Task')
    task_deadline = models.DateField(blank=True, help_text='Deadline of the task. format=Date(YYYY-MM-DD)')

    @property
    def desk_name(self):
        return self.related_column.related_desk.name

    @property
    def desk_id(self):
        return self.related_column.related_desk.id

    @property
    def desk_author(self):
        return self.related_column.related_desk.author

    def __str__(self):
        return f"{self.name}"


class Comment(models.Model):
    """
    @author: who created comment
    @comment_body: comment
    @related_task: for which task is this one
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_body = models.TextField(max_length=500, help_text='Comment text')
    related_task = models.ForeignKey(Task, on_delete=models.CASCADE, help_text='ID of task for which'
                                                                               ' this one is related')

    @property
    def desk_name(self):
        return self.related_task.related_column.related_desk.name

    @property
    def desk_id(self):
        return self.related_task.related_column.related_desk.id

    @property
    def desk_author(self):
        return self.related_task.related_column.related_desk.author

    # TODO
    # after add fields for img attaching or video attaching
