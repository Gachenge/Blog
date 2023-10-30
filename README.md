# API Documentation

## Description

Allow new users to be authenticated using either Google, GitHub, or Twitter. Then store the user information in MySQL databases. No need to remember multiple passwords.

## Table of Contents

- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Schemas](#schemas)

## API Endpoints

### Login with Google

- **Summary**: Login with Google
- **Description**: Redirects to Google login. Once login details are entered, it redirects to `/callback` that receives the Google authentications and saves the user to the database.
- **Path**: `/api/google/login`
- **Method**: GET
- **Responses**:
  - 302 - Redirect to Google login page
  - 500 - State does not match

### Logout

- **Summary**: Logout
- **Description**: Clears the session data.
- **Path**: `/api/google/logout`
- **Method**: GET
- **Responses**:
  - 302 - Redirect to the index

### Index

- **Summary**: Index
- **Description**: Displays available login options.
- **Path**: `/api/google`
- **Method**: GET
- **Responses**:
  - 200 - OK

### Login with GitHub

- **Summary**: Login with GitHub
- **Description**: Redirects to GitHub login.
- **Path**: `/api/github`
- **Method**: GET
- **Responses**:
  - 302 - Redirect to GitHub login page

### Get All Users

- **Summary**: Returns a list of all users in the database
- **Description**: Once a user is authenticated, they are added to the database. This returns a list of all users saved.
- **Path**: `/api/user/all`
- **Method**: GET
- **Responses**:
  - 200 - Returns a list of all users, by ID, name, and email

### Get User by ID

- **Summary**: Returns a specific user by their ID
- **Path**: `/api/user/{user_id}`
- **Method**: GET
- **Parameters**:
  - `user_id` (path, required, string)
- **Responses**:
  - 200 - Returns a specific user by their ID

### Update User by ID

- **Summary**: Allows an update for a user by their ID
- **Path**: `/api/user/{user_id}`
- **Method**: PATCH
- **Parameters**:
  - `user_id` (path, required, string)
- **Request Body**:
  - Type: `application/json`
  - Schema:
    ```json
    {
      "name": "string",
      "email": "string",
      "avatar": "string"
    }
    ```
- **Responses**:
  - 200 - User updated successfully
  - 400 - Key is not valid

### Delete User by ID

- **Summary**: Deletes a user by their ID
- **Path**: `/api/user/{user_id}`
- **Method**: DELETE
- **Parameters**:
  - `user_id` (path, required, string)
- **Responses**:
  - 200 - User deleted successfully

### Protected Area

- **Summary**: Protected Area
- **Description**: Requires login, displays protected content.
- **Path**: `/api/google/protected_area`
- **Method**: GET
- **Responses**:
  - 200 - OK

### Create a Blog Post

- **Summary**: Create a blog post
- **Path**: `/api/posts/create`
- **Method**: POST
- **Request Body**:
  - Type: `application/json`
  - Schema:
    ```json
    {
      "body": "string",
      "image_url": "string"
    }
    ```
- **Responses**:
  - 200 - Post created successfully
  - 400 - Post must have a body

### Get a Particular Post by ID

- **Summary**: Returns a particular post by ID
- **Path**: `/api/posts/{post_id}`
- **Method**: GET
- **Parameters**:
  - `post_id` (path, required, string)
- **Responses**:
  - 200 - Get a particular user by ID
  - 404 - Post not found

### Update Details for a Post

- **Summary**: Update details for a post
- **Path**: `/api/posts/{post_id}`
- **Method**: PATCH
- **Parameters**:
  - `post_id` (path, required, string)
- **Request Body**:
  - Type: `application/json`
  - Schema:
    ```json
    {
      "body": "string",
      "image_url": "string"
    }
    ```
- **Responses**:
  - 200 - Post updated successfully
  - 400 - Key is not valid
  - 404 - Post not found

### Delete a Post

- **Summary**: Delete a post
- **Description**: Get a post by ID and delete it
- **Path**: `/api/posts/{post_id}`
- **Method**: DELETE
- **Parameters**:
  - `post_id` (path, required, string)
- **Responses**:
  - 200 - Post deleted successfully
  - 404 - Post not found

### Return a List of All Posts

- **Summary**: Return a list of all posts
- **Description**: Get all blog posts
- **Path**: `/api/posts/all`
- **Method**: GET
- **Responses**:
  - 200 - Successful response

### All Posts by a Particular User

- **Summary**: All posts by a particular user
- **Description**: Get every post a user has
- **Path**: `/api/posts/user/{user_id}`
- **Method**: GET
- **Parameters**:
  - `user_id` (path, required, string)
- **Responses**:
  - 200 - Successful response
  - 404 - User not found

### All Posts by the Current User

- **Summary**: All posts by the current user
- **Description**: Returns a list of all my posts
- **Path**: `/api/posts/myposts`
- **Method**: GET
- **Responses**:
  - 200 - Successful response

### Get a Comment on a Particular Post

- **Summary**: Get a comment on a particular post
- **Description**: Get all comments on a post
- **Path**: `/api/posts/{post_id}/comments`
- **Method**: GET
- **Parameters**:
  - `post_id` (path, required, string)
- **Responses**:
  - 200 - Successful response

### Make a Comment on a Post

- **Summary**: Make a comment on a post
- **Description**: Create a comment on a particular post
- **Path**: `/api/posts/{post_id}/comments`
- **Method**: POST
- **Parameters**:
  - `post_id` (path, required, string)
- **Request Body**:
  - Type: `application/json`
  - Schema:
    ```json
    {
      "text": "string",
      "image_url": "string"
    }
    ```
- **Responses**:
  - 200 - Successful response
  - 400 - A comment must have text

## Authentication

To access protected endpoints, use Bearer Token Authentication with a JSON Web Token (JWT) in the `Authorization` header.

## Schemas

### Base Schema

- Type: `object`
- Properties:
  - `id`: Unique identifier of the model
  - `created_at`: Timestamp of when the model was created (format: date-time)
  - `updated_at`: Timestamp of when the model was last updated
  - `formatted_created_at`: Formatted created timestamp
  - `formatted_updated_at`: Formatted updated timestamp

### Comment

- Type: `object`
- Properties:
  - `user_id`: User ID who made the comment
  - `post_id`: ID of the post associated with the comment
  - `text`: Comment text
  - `image_url`: URL of an image associated with the comment

### Post

- Type: `object`
- Properties:
  - `user_id`: User ID who made the post
  - `body`: Post content
  - `image_url`: URL of an image associated with the post

### User

- Type: `object`
- Properties:
  - `account_id`: User's account ID
  - `name`: User's name
  - `email`: User's email address
  - `avatar`: URL of the user's avatar image
  - `token`: User's authentication token
