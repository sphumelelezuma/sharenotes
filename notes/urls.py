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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files in development