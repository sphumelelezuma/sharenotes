from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    title = models.CharField(max_length=255, default='Untitled Document', null=False)  # Title of the document
    description = models.TextField(default='', null=False)  # Description of the document
    file = models.FileField(upload_to='documents/', null=True, blank=True)  # Document file
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # User who uploaded the document (nullable)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp for upload

    def __str__(self):
        return self.title  # Return the title of the document
 

class Post(models.Model):
    title = models.CharField(max_length=100)   # Title of the post
    content = models.TextField()                 # Content of the post
    image = models.ImageField(upload_to='images/', null=True, blank=True)  # Image upload
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # User who created the post
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for post creation

    def __str__(self):
        return self.title  # Return the title of the post
  
