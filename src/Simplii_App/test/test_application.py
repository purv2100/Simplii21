import os
import pytest
from flask import Flask, session
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from src.application import create_app
from forms import ForgotPasswordForm, RegistrationForm, LoginForm, ResetPasswordForm, PostingForm, ApplyForm, TaskForm, UpdateForm


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_simplii'
    mongo = PyMongo(app)

    with app.test_client() as client:
        yield client
    os.environ.pop('MAIL_SERVER', None)
    os.environ.pop('MAIL_PORT', None)
    os.environ.pop('MAIL_USE_TLS', None)
    os.environ.pop('MAIL_USE_SSL', None)
    os.environ.pop('MAIL_USERNAME', None)
    os.environ.pop('MAIL_PASSWORD', None)


def test_home_redirects_to_login(client: Any):
    response = client.get('/')
    assert response.status_code == 302  # Redirect status code


def test_login_success(client: Any):
    # Assuming a user exists in the test database
    # with email: 'test@example.com' and password: 'testpassword'
    response = client.post('/login', data=dict(
        email='test@example.com',
        password='testpassword'
    ), follow_redirects=True)
    assert b'You have been logged in!' in response.data
    assert session.get('email') == 'test@example.com'


def test_login_failure(client: Any):
    response = client.post('/login', data=dict(
        email='nonexistent@example.com',
        password='wrongpassword'
    ), follow_redirects=True)
    assert b'Login Unsuccessful. Please check username and password' in response.data
    assert session.get('email') is None


def test_logout(client: Any):
    # Assuming a user is already logged in
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    response = client.get('/logout', follow_redirects=True)
    assert b'success' in response.data
    assert session.get('email') is None
