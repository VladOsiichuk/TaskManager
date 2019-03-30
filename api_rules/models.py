from django.db import models
from desk.model import Desk
from django.conf import settings


class PermissionRow(models.Model):
    """
    This one model is created with the aim to connect each participant to desk with special permission
    """
    permission = models.CharField(max_length=6, default="STAFF")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    related_desk = models.ForeignKey(Desk, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'related_desk')
