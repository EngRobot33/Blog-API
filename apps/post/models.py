from django.db import models

from ..common.models import BaseModel
from ..user.models import User


class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=127, primary_key=True)
    title = models.CharField(max_length=127, unique=True)
    content = models.TextField()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        db_table = 'posts'
        indexes = [models.Index(fields=['author', 'slug', 'title', 'content', ])]

    def __str__(self):
        return self.slug
