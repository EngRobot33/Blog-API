from django.core.exceptions import ValidationError
from django.db import models

from ..user.models import User


class Relation(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = 'Relation'
        verbose_name_plural = 'Relations'
        db_table = 'relations'
        indexes = [models.Index(fields=['follower', 'following'])]

    def clean(self):
        if self.follower == self.following:
            raise ValidationError({"follower": "Follower cannot be following!"})

    def __str__(self):
        return f"{self.follower} -> {self.following}"
