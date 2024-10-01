from django.urls import path
from django.conf import settings
from django.conf.urls.static import static 
from .views import home, create_post, register, login_view, logout_view, upload_document
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('register/', views.register, name='register'),  # Registration path
    path('login/', views.login_view, name='login'),  # Login path
    path('logout/', views.logout_view, name='logout'),  # Logout path
    path('upload/', views.upload_document, name='upload_document'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('document/delete/<int:document_id>/', views.delete_document, name='delete_document'),  # URL pattern for document delete
    path('toggle_reaction/<str:content_type>/<int:object_id>/', views.toggle_reaction, name='toggle_reaction'),
    path('add-comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  # URL for post detail
    path('toggle_reaction/<int:post_id>/', views.toggle_reaction, name='toggle_reaction'),
    path('posts/<int:post_id>/react/', views.react_to_post, name='react_to_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files in development