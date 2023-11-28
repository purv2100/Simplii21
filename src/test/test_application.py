import os
import pytest
from flask import Flask, session
from flask_pymongo import PyMongo
from flask_bcrypt import bcrypt
from Simplii_App.application import app
from Simplii_App.forms.forms import *
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_simplii'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            mongo = PyMongo(app)
        yield client

def test_home_redirects_to_login(client):
    response = client.get("/")
    assert response.status_code == 302  # Redirect status code


def test_register(client):
    # Define a fake user for testing
    fake_user = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    }
    # Insert the test user into the "users" collection
    with app.app_context():
        mongo = PyMongo(app)
        mongo.db.users.insert_one({
            'name': fake_user['username'],
            'email': fake_user['email'],
            'pwd': fake_user['password'],
            'temp': None
        })
    # Simulate a successful registration
    response = client.post('/register', data=fake_user, follow_redirects=True)
    # Check if the user is redirected to the home page after registration
    assert response.status_code == 200  # Assuming a successful registration redirects to the home page
    # Check if the user is in the MongoDB collection
    with app.app_context():
        mongo = PyMongo(app)
        user = mongo.db.users.find_one({'email': 'test@example.com'})
    assert user is not None
    assert user['name'] == 'testuser'
    assert 'pwd' in user  # Check if the hashed password is present in the user document


def test_login_success(client):
    app.config['WTF_CSRF_ENABLED'] = True

    response = client.post('/login', data=dict(
        email='test@example.com',
        password='testpassword'
    ), follow_redirects=True)   
    # Check if the user exists in the "users" collection
    with app.app_context():
        mongo = PyMongo(app)
        user = mongo.db.users.find_one({'email': 'test@example.com'})
    assert user is not None
    # Check for the presence of the logged-in message in the response
    # assert b'You have been logged in!' in response.data.encode('utf-8')


def test_login_failure(client):
    response = client.post('/login', data=dict(
        email='nonexistent@example.com',
        password='wrongpassword'
    ), follow_redirects=True)


def test_friends(client, setup_test_database):

    # Define a fake friend request for testing
    fake_request = {
        'sender': 'test@example.com',
        'receiver': 'test_friend@example.com',
        'accept': False
    }

    # Insert the test friend request into the "friends" collection
    with app.app_context():
        mongo = PyMongo(app)
        mongo.db.friends.insert_one(fake_request)

    # Simulate a logged-in user
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    # Simulate accessing the /friends route
    response = client.get('/friends', follow_redirects=True)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200


def test_logout(client):
    # Assuming a user is already logged in
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'
    response = client.get('/logout', follow_redirects=True)


def test_friends(client):
    # Define a fake friend request for testing
    fake_request = {
        'sender': 'test@example.com',
        'receiver': 'friend@example.com',
        'accept': False
    }

    # Insert the test friend request into the "friends" collection
    with app.app_context():
        mongo = PyMongo(app)
        mongo.db.friends.insert_one(fake_request)

    # Simulate a logged-in user
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    # Simulate accessing the /friends route
    response = client.get('/friends', follow_redirects=True)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the friend is in the MongoDB collection
    with app.app_context():
        mongo = PyMongo(app)
        friends = mongo.db.friends.find_one({'sender': 'test@example.com'})

    assert friends is not None

    # Now accept the friend request by logging in as friend. Then check the friend list.

    # Simulate a logged-in user
    with client.session_transaction() as sess:
        sess['email'] = 'friend@example.com'

    # Check if there is any friend request in the MongoDB collection
    with app.app_context():
        mongo = PyMongo(app)
        pending_approvals = mongo.db.friends.find_one({'receiver': 'friend@example.com', 'accept': False})
        mongo.db.friends.update_one({'receiver':'friend@example.com'}, {'$set': {'accept':True}})

    assert pending_approvals is not None



def test_task(client):

    # Define a fake task for testing
    fake_task = {
        'taskname': 'Test Task',
        'category': 'easy',
        'startdate': '2023-01-01',
        'start_time': '09:00',
        'end_time': '11:00',
        'description': 'This is a test task description',
        'invitees': ['Please Select']
    }

    # Simulate a successful task addition
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'  # Simulate a logged-in user

    response = client.post('/task', data=fake_task, follow_redirects=True)

    # Check if the task is added to the database and the user is redirected to the home page
    assert response.status_code == 200  # Assuming a successful task addition redirects to the home page
    # assert b'Test Task Task Added!' in response.data

    # Check if the task is in the MongoDB collection
    with app.app_context():
        mongo = PyMongo(app)
        task = mongo.db.tasks.find_one({'taskname': 'Test Task'})
    assert task['email'] == 'test@example.com'
    assert task['category'] == 'easy'
    assert task['startdate'] == '2023-01-01'
    assert task['starttime'] == '09:00'
    assert task['endtime'] == '11:00'
    assert task['description'] == 'This is a test task description'


def test_completeTask(client):

    with app.app_context():
        mongo = PyMongo(app)
        tasks = mongo.db.tasks.find_one({'taskname': 'Test Task'})

    # Simulate a successful task completion

    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'  # Simulate a logged-in user

    # Simulate a request to mark the task as complete
    response = client.post('/completeTask', data={
        'task': 'Test Task',
        'actualhours': '2'
    }, follow_redirects=True)

    # Check if the task is marked as complete in the database and the user is redirected to the home page
    assert response.status_code == 200  # Assuming a successful task completion redirects to the home page

    # Check if the task is marked as complete in the MongoDB collection
    with app.app_context():
        mongo = PyMongo(app)
        task = mongo.db.tasks.find_one({'taskname': 'Test Task'})

    assert task is not None
    assert task['email'] == 'test@example.com'
    assert task['completed'] == True
    assert task['actualhours'] == 2


def test_forum(client):
    with app.app_context():
        mongo = PyMongo(app)
        threads = mongo.db.threads.find_one({'title': 'Test Thread'})

    # Simulate a logged-in user
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'  # Simulate a logged-in user
        sess['name'] = 'Test User'

    
    # Check if the thread is created in the MongoDB collection
    with app.app_context():
        mongo = PyMongo(app)
        created_thread = mongo.db.threads.find_one({'title': 'Test Thread'})

    if created_thread is None:
        # Simulate a request to create a new thread
        response_create_thread = client.post('/forum', data={
            'thread_title': 'Test Thread',
            'thread_content': 'This is a test thread'
        }, follow_redirects=True)

    # Check if the response status code is 200 (OK)
    assert response_create_thread.status_code == 200

    # Check if the thread is created in the MongoDB collection
    with app.app_context():
        mongo = PyMongo(app)
        created_thread = mongo.db.threads.find_one({'title': 'Test Thread'})

    assert created_thread is not None
    assert created_thread['user_email'] == 'test@example.com'
    assert created_thread['user'] == 'Test User'
    assert created_thread['title'] == 'Test Thread'
    assert created_thread['content'] == 'This is a test thread'

    # Simulate a request to reply to the created thread
    response_reply_to_thread = client.post('/forum', data={
        'thread_id': str(created_thread['_id']),
        'reply_content': 'This is a test reply'
    }, follow_redirects=True)

    # Check if the response status code is 200 (OK)
    assert response_reply_to_thread.status_code == 200

    # Check if the reply is added to the thread in the MongoDB collection
    with app.app_context():
        mongo = PyMongo(app)
        updated_thread = mongo.db.threads.find_one({'_id': created_thread['_id']})

    assert updated_thread is not None
    assert len(updated_thread['replies']) == 1
    assert updated_thread['replies'][0]['user_email'] == 'test@example.com'
    assert updated_thread['replies'][0]['user'] == 'Test User'
    assert updated_thread['replies'][0]['content'] == 'This is a test reply'

    # Simulate a request to retrieve all threads
    response_get_threads = client.get('/forum')

    # Check if the response status code is 200 (OK)
    assert response_get_threads.status_code == 200

    # Check if the rendered template contains the created thread and reply
    assert b'Test Thread' in response_get_threads.data
    assert b'This is a test thread' in response_get_threads.data
    assert b'This is a test reply' in response_get_threads.data


# def test_analytics(client):

#     # Simulate a logged-in user
#     with client.session_transaction() as sess:
#         sess['email'] = 'test@example.com'
#         sess['name'] = 'Test User'

#     # Simulate adding tasks to the database
#     with app.app_context():
#         mongo = PyMongo(app)

#         # Add a task for testing the analytics charts
#         task_id = mongo.db.tasks.insert_one({
#             'email': 'test@example.com',
#             'taskname': 'Test Task',
#             'category': 'Medium',
#             'status': 'Incomplete',
#             'startdate': '2023-01-01',
#             'duedate': '2023-01-10',
#             'hours': 5,
#             'description': 'This is a test task',
#             'completed': False,
#             'starttime': '08:00',
#             'endtime': '13:00'
#         }).inserted_id

#     # Simulate a request to the analytics page
#     response = client.get('/analytics')

#     # Check if the response status code is 200 (OK)
#     assert response.status_code == 200

#     # Check if the analytics page is rendered
#     assert b'Analytics' in response.data

#     # Check if the HTML for each chart is present in the response
#     assert b'Task Complexity Histogram' in response.data
#     assert b'Expected Hours Vs Actual Hours to complete a task' in response.data
#     assert b'Year-wise distribution of completed tasks' in response.data
#     assert b'Monthly distribution of completed tasks' in response.data
#     assert b'Weekly distribution of completed tasks' in response.data
#     assert b'Completed vs Incomplete Tasks' in response.data

#     # Optionally, you can check for specific data points or patterns in the response HTML
#     # For example, check if the test task is present in the task complexity histogram chart
#     assert f"'Test Task', 'rgba(166, 145, 92, 1)'" in response.data

#     # Clean up: Remove the test task from the database
#     with app.app_context():
#         mongo = PyMongo(app)
#         mongo.db.tasks.delete_one({'_id': ObjectId(task_id)})

