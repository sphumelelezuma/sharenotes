from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Use GenericForeignKey to support reactions to different models (e.g., Post)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("content_type", "object_id", "user")  # Ensure uniqueness based on user and content object
        indexes = [
            models.Index(fields=['content_type']),
            models.Index(fields=['object_id']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user} reacted to {self.content_object}"



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented on {self.post.title}"

class NestedComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} replied to comment ID {self.comment.id}"

class Document(models.Model):
    title = models.CharField(max_length=255, default='Untitled Document', null=False)
    description = models.TextField(default='', null=False)
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    reactions_count = models.IntegerField(default=0)  # Field to keep track of reaction count

    # Add this line
    reactions = GenericRelation(Reaction)

    def __str__(self):
        return self.title



