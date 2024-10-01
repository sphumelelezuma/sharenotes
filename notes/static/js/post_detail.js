document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(likeButton => {
        likeButton.addEventListener('click', function () {
            const postId = likeButton.dataset.postId;

            fetch(`/like_post/${postId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ post_id: postId })
            })
            .then(response => response.json())
            .then(data => {
                // Update the like button image
                if (data.liked) {
                    likeButton.src = "/static/icons/heart_filled.png";
                } else {
                    likeButton.src = "/static/icons/heart_outline.png";
                }
                // Update the like count
                document.getElementById(`like-count-${postId}`).textContent = data.likes_count;
            })
            .catch(error => console.error('Error:', error));
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
