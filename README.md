# API Endpoints

User Registration

Endpoint: /register_user/
Method: POST
Description: Register a new user.
Authentication: Required (Admin)

User Edit
Endpoint: /edit_user/{id}/
Method: PUT
Description: Edit user information.
Authentication: Required (Admin)


Get All Users
Endpoint: /get_all_users/
Method: GET
Description: Get a list of all users.
Authentication: Required (Admin)


User Login
Endpoint: /login/
Method: POST
Description: Authenticate and obtain an access token.
Authentication: Not required


User Logout
Endpoint: /logout/
Method: POST
Description: Log out and invalidate the access token.
Authentication: Required


Create Group
Endpoint: /groups/create/
Method: POST
Description: Create a new group.
Authentication: Required (Admin)


List Groups
Endpoint: /groups/list/
Method: GET
Description: Get a list of all active groups.
Authentication: Required

Delete Group
Endpoint: /groups/{group_id}/delete/
Method: DELETE
Description: Delete a group.
Authentication: Required (Creator)

Update Group
Endpoint: /groups/{group_id}/update/
Method: PUT
Description: Update group information.
Authentication: Required (Creator)

Get Group Details
Endpoint: /groups/{group_id}/
Method: GET
Description: Get details of a group.
Authentication: Required

Get Group Messages
Endpoint: /groups/{group_id}/messages/
Method: GET
Description: Get messages for a group.
Authentication: Required

Send Message to Group
Endpoint: /groups/{group_id}/send_message/
Method: POST
Description: Send a message to a group.
Authentication: Required (Group Member)

Add Member to Group
Endpoint: /groups/{group_id}/add_member/
Method: POST
Description: Add a user to a group.
Authentication: Required (Admin or Creator)

Remove Member from Group
Endpoint: /groups/{group_id}/remove_member/
Method: DELETE
Description: Remove a user from a group.
Authentication: Required (Admin or Creator)

Like Message
Endpoint: / messages/<int:message_id>/like_message/
Method: POST
Description: Like Message in group
Authentication: Required (Admin or Creator)


Installation
Install all necessary library 
pip install -r requirements.txt

Prerequisites 

To Run project use below steps 
Go to root folder 
Python manage.py makemigrations 
Python manage.py migrate 
Python manage.py makemigrations group_chat(optional)
Python manage.py migrate group_chat(optional)

(create super user / admin)
Python manage.py createsuperuser(optional)
(enter username , email and password )

Python manage.py runserver 
I have already created  super user 
Username – bodake@gmail.com
Password – admin

You can check test/test_api.py file and do modification in this file like , change based url (port) and login details for admin




Authentication
In this project, we use Simple JWT (JSON Web Tokens) for authentication. JSON Web Tokens are a widely used method for securely transmitting information between parties as a JSON object. Here's how authentication works in our project:
User Login: To log in, users send a POST request to the /login/ endpoint with their username and password. If the credentials are valid, the server will respond with an access token. The access token should be saved by the client application for future authenticated requests. It it expires it will refresh the token .

Authorization Header: For authenticated requests, the access token should be included in the request headers using the "Bearer" token type. Here's an example of how to include the access token in the request header:
Authorization: Bearer <access_token>
Testing
Explain how to run tests for your project. You can use the provided pytest script, for example:
pytest tests/test_api.py
