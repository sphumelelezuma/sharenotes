// Function to toggle reactions (like/unlike) on a post 
async function toggleReaction(postId) {
    console.log('Toggling reaction for post ID:', postId); // Debugging statement
    const reactionIcon = document.getElementById(`reaction-icon-${postId}`);
    const reactionCounter = document.getElementById(`reaction-counter-${postId}`);
    
    // Ensure the reactionIcon is not null
    if (!reactionIcon || !reactionCounter) {
        console.error(`Reaction icon or counter not found for post ID: ${postId}`);
        return;
    }

    const reacted = reactionIcon.getAttribute('data-reacted') === 'true';
    const reactionType = reacted ? 'unlike' : 'like';

    try {
        const response = await fetch(`/toggle_reaction/${postId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // Ensure CSRF token is handled
            },
            body: JSON.stringify({ reaction_type: reactionType }),
        });

        const data = await response.json();

        if (data.error) {
            console.error(data.error);
            return;
        }

        // Update UI elements for the specific post
        reactionCounter.innerText = data.total_reactions; // Update total reactions
        reactionIcon.querySelector('img').src = reacted ? "/static/icons/heart_outline.png" : "/static/icons/heart_filled.png"; // Update icon
        reactionIcon.setAttribute('data-reacted', !reacted); // Update reacted state
    } catch (error) {
        console.error('Error:', error);
    }
}




// Existing filterContent function
function filterContent() {
    const toggle = document.getElementById('toggle').value;
    const postsContainer = document.getElementById('posts-container');
    const documentsContainer = document.getElementById('documents-container');

    // Toggle between posts and documents based on user selection
    if (toggle === 'posts') {
        postsContainer.style.display = 'block';
        documentsContainer.style.display = 'none';
    } else {
        postsContainer.style.display = 'none';
        documentsContainer.style.display = 'block';
    }
}

// New script for handling persistent reactions and comments
document.addEventListener("DOMContentLoaded", function () {
    const reactionIcons = document.querySelectorAll(".reaction-icon");
    const commentButtons = document.querySelectorAll(".comment-button");

    reactionIcons.forEach(icon => {
        icon.addEventListener("click", async () => {
            const postId = icon.dataset.postId; // Get the post ID from the icon's dataset
            await toggleReaction(postId);
        });
    });

    commentButtons.forEach(button => {
        button.addEventListener("click", () => {
            const postId = button.dataset.postId; // Get the post ID from the button's dataset
            toggleCommentSection(postId);
        });
    });
});


// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function toggleCommentSection(postId) {
    console.log(`Toggling comments for post ID: ${postId}`); // Debugging statement
    const commentsSection = document.querySelector(`.comments-section[data-post-id="${postId}"]`);

    if (commentsSection) {
        if (commentsSection.style.display === 'none' || commentsSection.style.display === '') {
            commentsSection.style.display = 'block';
        } else {
            commentsSection.style.display = 'none';
        }
        console.log(`Comments section is now: ${commentsSection.style.display}`); // Debugging statement
    } else {
        console.error(`Comments section not found for post ID: ${postId}`);
    }
}

