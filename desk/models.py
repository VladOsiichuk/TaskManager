from django.db import models
from user_auth.models import CustomUser


class Desk(models.Model):
    """
    class describing the desk
    @author: who created the desk
    @name: the name of the desk
    @description: short description of the desk
    """

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.name}"


class Column(models.Model):
    """
    @related_desk: board to which is related this one
    @author: who created this one
    @order_in_desk: the order of column in the desk
    @name: title of column
    """

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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
    current_executor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    task_deadline = models.DateField(blank=True)

    def __str__(self):
        return f"{self.name}"
