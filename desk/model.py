from django.db import models
from django.conf import settings
from django.utils.timezone import now



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

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Desk post"
        verbose_name_plural = "Desk posts"

    # This one is necessary to check if user is ADMIN(IsAdminOfDesk)
    @property
    def desk_author(self):
        return self.author


class Column(models.Model):
    """
    class describing the Column of Desk
    @related_desk: board to which is related this one
    @author: who created this one
    @order_in_desk: the order of column in the desk
    @name: title of column
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    related_desk = models.ForeignKey(Desk, related_name='columns',
                                     on_delete=models.CASCADE, help_text='ID of desk for which Column is related')
    name = models.CharField(max_length=64, help_text="Title of the Column")

    created = models.DateField(auto_now_add=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Column"
        verbose_name_plural = "Columns"

    # This one is necessary to check if user is ADMIN(IsAdminOfDesk)
    @property
    def desk_author(self):
        return self.related_desk.author


def upload_task_image(instance, filename):
    return "uploads/tasks/{filename}".format(filename=filename)


class Task(models.Model):
    """
    @author: who created this one
    @related_column: the column to which this one is related currently
    @current_executor: to who task is assigned
    @description: description
    @task_deadline: deadline of execution
    """

    related_column = models.ForeignKey(Column, related_name='tasks',
                                       on_delete=models.CASCADE, help_text="ID of column for which Task is related")
    current_executor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         help_text="ID of user for who task is assigned")
    name = models.CharField(max_length=64, help_text='Title of the task')
    description = models.TextField(max_length=500, help_text='Description of the Task')
    task_deadline = models.DateField(default=now,
                                     help_text='Deadline of the task. format=Date(MM-DD-YYYY)')

    image = models.ImageField(upload_to=upload_task_image, blank=True, null=True)
    priority_choices = [
        ("Високий", "HIGH"),
        ("Середній", "MEDIUM"),
        ("Низький", "LOW"),
    ]
    priority = models.CharField(max_length=8, choices=priority_choices, default="Середній")

    def __str__(self):
        return f"{self.name} - " + self.description[:25] + "..."

    # This one is necessary to check if user is ADMIN(IsAdminOfDesk)
    @property
    def desk_author(self):
        return self.related_column.related_desk.author


def upload_comment_image(instance, filename):
    return "uploads/comments/{filename}".format(filename=filename)


class Comment(models.Model):
    """
    @author: who created comment
    @comment_body: comment
    @related_task: for which task is this one
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_body = models.TextField(max_length=500, help_text='Comment text')
    related_task = models.ForeignKey(Task, related_name='comments',
                                     on_delete=models.CASCADE, help_text='ID of task for which this one is related')

    image = models.ImageField(upload_to=upload_comment_image, null=True, blank=True)

    is_child = models.BooleanField(default=False)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, blank=True, null=True,
                               related_name='related_comment')

    # This one is necessary to check if user is ADMIN(IsAdminOfDesk)
    @property
    def desk_author(self):
        return self.related_task.related_column.related_desk.author

