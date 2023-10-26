# Authorizations

## Description

Allow new users to be authenticated using either Google, GitHub, or Twitter. Then store the user information in MySQL databases. No need to remember multiple passwords.

## Table of Contents

- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Schemas](#schemas)

## API Endpoints

- **Login with Google**: [GET /api/google/login](#login-with-google)
  - Redirects to Google login. Once login details are entered, it redirects to /callback that receives the Google authentications and saves the user to the database.
- **Logout**: [GET /api/google/logout](#logout)
  - Clears the session data.
- **Index**: [GET /api/google](#index)
  - Displays available login options.
- **Login with GitHub**: [GET /api/github](#login-with-github)
  - Redirects to GitHub login.
- **Get All Users**: [GET /api/user/all](#get-all-users)
  - Returns a list of all users in the database.
- **Get User by ID**: [GET /api/user/{user_id}](#get-user-by-id)
  - Returns a specific user by their ID.
- **Update User by ID**: [PATCH /api/user/{user_id}](#update-user-by-id)
  - Update a user by their ID.
- **Delete User by ID**: [DELETE /api/user/{user_id}](#delete-user-by-id)

## Authentication

- To access protected endpoints, use Bearer Token Authentication with a JSON Web Token (JWT) in the `Authorization` header.

## Schemas

### Base Schema

```basemodel schema```
{
  "id": "string (uuid)",
  "created_at": "string (date-time)",
  "updated_at": "string (date-time)"
}

```user schema```
{
  "id": "string (uuid)",
  "account_id": "integer",
  "name": "string",
  "email": "string",
  "token": "string",
  "created_at": "string (strftime('%Y-%m-%d %H:%M:%S'))",
  "updated_at": "string (strftime('%Y-%m-%d %H:%M:%S'))"
}
