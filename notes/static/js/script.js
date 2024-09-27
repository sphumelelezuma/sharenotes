function filterContent() {
    const toggle = document.getElementById('toggle').value;
    const postsContainer = document.getElementById('posts-container');
    const documentsContainer = document.getElementById('documents-container');

    if (toggle === 'posts') {
        postsContainer.style.display = 'block';
        documentsContainer.style.display = 'none';
    } else {
        postsContainer.style.display = 'none';
        documentsContainer.style.display = 'block';
    }
}
