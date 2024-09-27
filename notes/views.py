from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .utils import resize_image  # Import the resize_image function
from .forms import PostForm, UserRegistrationForm, DocumentForm
from .models import Post, Document


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    documents = Document.objects.all().order_by('-id')
    print(f'Posts: {posts}')
    print(f'Documents: {documents}')
    return render(request, 'home.html', {'posts': posts, 'documents': documents})

@login_required 
def create_post(request):
    if request.method == 'POST':
        print("Received POST request")
        form = PostForm(request.POST, request.FILES)  # Use PostForm here
        print("Form data:", request.POST)
        print("Files data:", request.FILES)
        
        if form.is_valid():
            print("Form is valid")
            post = form.save(commit=False)  # Don't save yet
            post.author = request.user  # Set the author to the logged-in user

            # Check if the image is present
            if request.FILES.get('image'):
                print("Image file found")
                image_file = resize_image(request.FILES['image'])
                post.image.save(image_file.name, image_file)  # Save the resized image
            
            post.save()  # Now save the post
            print("Post saved successfully")
            return redirect('home')  # Redirect after successful upload
        else:
            print("Form errors:", form.errors)  # Log form errors
    else:
        form = PostForm()  # Initialize a new PostForm instance
    return render(request, 'create_post.html', {'form': form})  # Render the template with the form


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)  # Log the user in
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Use the built-in AuthenticationForm
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)  # Authenticate user
            if user is not None:
                login(request, user)  # Log the user in
                return redirect('home')  # Redirect to home after successful login
            else:
                messages.error(request, 'Invalid username or password.')  # Show error message
        else:
            messages.error(request, 'Invalid username or password.')  # Show error message
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required 
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user  # Set the uploaded_by field
            document.save()
            return redirect('home')  # Redirect to the home page after upload
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)  # Ensure user is owner of post
    post.delete()
    return redirect('home')  # Redirect to the homepage or posts list after deletion

@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)  # Get the document or return 404
    if request.method == 'POST':  # Ensure it's a POST request for deletion
        document.delete()  # Delete the document
        return redirect('home')  # Redirect to home or another page after deletion
    return render(request, 'confirm_delete.html', {'document': document})  # Render a confirmation template