# ShareNotes

Welcome to **ShareNotes**, a platform that allows users to share, react to, and comment on posts, as well as manage documents. ShareNotes makes it easy for users to collaborate, engage, and share ideas or resources. The web app provides an intuitive interface for creating and interacting with posts, comments, and documents. Built using modern web technologies, ShareNotes combines the power of a user-friendly front-end with a robust back-end to provide a seamless experience.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
- [Usage Guide](#usage-guide)
  - [Creating Posts](#creating-posts)
  - [Adding Comments](#adding-comments)
  - [Document Management](#document-management)
  - [Reactions](#reactions)
- [Contributing](#contributing)

## Features
- **User Authentication**: Register and log in to access the platform.
- **Posts**: Users can create, and delete posts with content and optional images.
- **Comments**: Engage with posts by adding comments.
- **Reactions**: React to posts with hearts.
- **Document Sharing**: Upload, manage, and share documents.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
  - HTML and CSS for structuring and styling pages.
  - JavaScript for enhancing interactivity and enabling asynchronous form submissions.
- **Backend**: Python with Django Framework
  - Django serves as the back-end framework for handling requests, database interactions, and user management.
- **Database**: MySQL
  - Stores user, post, comment, reaction, and document data.

## Getting Started

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/sphumelelezuma/sharenotes.git
    ```
2. **Navigate to the Project Directory**:
    ```bash
    cd sharenotes
    ```
3. **Create and Activate a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
4. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5. **Set Up the Database**:
    - Make sure MySQL is running, and create a database called `sharenotes_db`.
    - Update `settings.py` with your MySQL credentials.

6. **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

7. **Create a Superuser**:
    ```bash
    python manage.py createsuperuser
    ```

8. **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```

9. **Access the Application**:
    - Open your web browser and navigate to `http://127.0.0.1:8000`.

### Usage

- **Register** to create a new account.
- **Log in** using your credentials to access all features.

## Usage Guide

### Creating Posts
- Navigate to the "Create Post" section to write a new post.
- Add a title, content, and optionally upload an image.
- Click "Submit" to share your post with other users.

### Adding Comments
- Click on any post to view details and comments.
- Use the comment form to add your thoughts or reply to other comments.

### Document Management
- Go to the "Upload File" section to upload files.
- Fill in the title and description, and select a file to upload.
- Uploaded documents can be viewed and downloaded by other users.

### Toggle between Posts and Documents
- Users toggle between posts and documents as they are on different sections on the home page. Documents are viewed separately to posts.

### Reactions
- React to posts by clicking on the "Heart" icons, icons changes with reaction click.
- The number of reactions will be displayed on each post, along with an indicator if you have already reacted(heart icon tells that).

## Contributing
We welcome contributions to improve ShareNotes! If you'd like to contribute:
- Fork the repository.
- Create a new branch (`git checkout -b feature-branch`).
- Commit your changes (`git commit -m "Add new feature"`).
- Push to the branch (`git push origin feature-branch`).
- Open a pull request.

