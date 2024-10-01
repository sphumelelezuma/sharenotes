from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json 
from django.core.files.storage import FileSystemStorage
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .utils import resize_image  # Import the resize_image function
from .forms import PostForm, UserRegistrationForm, DocumentForm, CommentForm
from .models import Post, Document, Reaction, Comment, NestedComment


@login_required 
def home(request):
    posts = Post.objects.all().prefetch_related('comments', 'reactions').order_by('-created_at')
    documents = Document.objects.all().order_by('-id')

    # Fetch user's reactions (specific to Post)
    post_content_type = ContentType.objects.get_for_model(Post)
    user_reactions = Reaction.objects.filter(user=request.user, content_type=post_content_type)

    # Include comments and reaction counts for each post
    for post in posts:
        post.reaction_count = Reaction.objects.filter(content_type=post_content_type, object_id=post.id, is_active=True).count()
        # Check if the user reacted to this post
        post.user_reacted = user_reactions.filter(object_id=post.id, is_active=True).exists()

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


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Fetch related reactions for this post
    post_content_type = ContentType.objects.get_for_model(Post)
    reactions = Reaction.objects.filter(content_type=post_content_type, object_id=post.id)

    likes_count = reactions.count()
    comments = post.comments.all()

    # Check if the user has liked the post
    has_liked = reactions.filter(user=request.user).exists()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments, 
        'has_liked': has_liked,
        'likes_count': likes_count,
    })


@login_required
def toggle_reaction(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content_type = ContentType.objects.get_for_model(Post)

    # Check if the user has already reacted
    reaction = Reaction.objects.filter(user=request.user, content_type=content_type, object_id=post.id).first()

    if reaction:
        # If the reaction already exists, deactivate it
        reaction.is_active = not reaction.is_active
        reaction.save()
        response_message = "Reaction removed" if not reaction.is_active else "Reaction added"
    else:
        # Create a new reaction if it doesn't exist
        reaction = Reaction(user=request.user, content_type=content_type, object_id=post.id)
        reaction.save()
        response_message = "Reaction added"

    # Update the post's reaction count based on active reactions
    reaction_count = Reaction.objects.filter(content_type=content_type, object_id=post.id, is_active=True).count()

    return JsonResponse({
        'message': response_message,
        'total_reactions': reaction_count
    })
 

def get_reaction_count(post):
    return Reaction.objects.filter(post=post, is_active=True).count()
    

def post_list(request):
    posts = Post.objects.all()
    posts_with_reaction_count = []

    for post in posts:
        reaction_count = Reaction.objects.filter(post=post, is_active=True).count()
        posts_with_reaction_count.append({
            'post': post,
            'reaction_count': reaction_count,
        })

    return render(request, 'post_detail.html', {'posts': posts_with_reaction_count})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form}) 
    

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)


@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content_type = ContentType.objects.get_for_model(Post)
        existing_reaction = Reaction.objects.filter(user=request.user, content_type=content_type, object_id=post.id).first()

        # Toggle the like status
        if existing_reaction:
            existing_reaction.delete()
            liked = False
        else:
            Reaction.objects.create(
                user=request.user,
                content_type=content_type,
                object_id=post.id
            )
            liked = True

        # Get the updated likes count
        likes_count = Reaction.objects.filter(content_type=content_type, object_id=post.id, is_active=True).count()

        return JsonResponse({'likes_count': likes_count, 'liked': liked})



@login_required
def react_to_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        # Check if a reaction already exists for this user and post
        reaction, created = Reaction.objects.get_or_create(user=user, post=post)

        if not created:
            # If the reaction already exists, toggle its active state
            reaction.is_active = not reaction.is_active
            reaction.save()
        else:
            # If the reaction was just created, set it to active
            reaction.is_active = True

        # Update the post's reaction count based on active reactions
        post.reactions_count = post.reactions.filter(is_active=True).count()
        post.save()

        # Return the updated reaction count
        return JsonResponse({"reactions_count": post.reactions_count})

    return JsonResponse({"error": "Invalid request method."}, status=400)