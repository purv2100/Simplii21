import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.application import app, mongo

@pytest.fixture
def client():
    app.config['TESTING']=True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/simplii21_test'
    mongo.init_app(app)
    client = app.test_client()
    yield client, mongo

def test_home_route_without_email(client):

    response = client[0].get('/home', follow_redirects=True)
    # Assert that the response is a redirect
    assert response.history[0].status_code == 302
    # Assert that redirection target is login
    assert response.history[0].headers.get('Location').split('/')[-1] == 'login'

def test_home_route_with_email(client):
    # Add email in session to test dashboard route
    with client[0].session_transaction() as sess:
        sess['email'] = 'apexarcheole@gmail.com'
    # Check for redirections
    response = client[0].get('/home', follow_redirects=True)
    # Assert that the response is a redirect
    assert response.history[0].status_code == 302
    # Assert that redirection target is login
    assert response.history[0].headers.get('Location').split('/')[-1] == 'dashboard'

def test_friends_route_without_email(client):

    response = client[0].get('/friends', follow_redirects=True)
    # Assert that the response is a redirect
    assert response.history[0].status_code == 302
    # Assert that redirection target is login
    assert response.history[0].headers.get('Location').split('/')[-1] == 'login'

def test_friends_route_with_email(client):

    with client[0].session_transaction() as sess: 
        sess['email'] = 'apexarcheole@gmail.com'

    response = client[0].get('/friends')
    # Assert that the response is a success
    assert response.status_code == 200
    # Assert that the response contains data from friends.html
    assert b'id="friendsCard"' in response.data

def test_dashboard(client):
    
    with client[0].session_transaction() as sess:
        sess['email'] = 'apexarcheole@gmail.com'

    response = client[0].get('/dashboard')
    #Assert that the response is a success
    assert response.status_code == 200
    #Assert that the response contains data from dashboard.html
    assert b'ddl1Category' in response.data

def test_analytics_tasks(client):

    with client[0].session_transaction() as sess:
        sess['email'] = 'apexarcheole@gmail.com'

    response = client[0].get('/analytics')
    # Test when there are no tasks
    if len(list(client[1].db.tasks.find({'email': sess['email']}, {'email'}))) == 0:
        # Assert that the response is a redirect
        assert response.status_code == 302
        # Assert that redirection target is task
        assert response.location.endswith('/task')
    else:
        #Assert that the response is a success
        assert response.status_code == 200
        #Assert that the response contains data from dashboard.html
        assert b'exp_act_html' in response.data
    
def test_aboutus(client):

    response = client[0].get('/about_us')
    #Assert that the response is a success
    assert response.status_code == 200
    #Assert that the response contains data from dashboard.html
    assert b'Introducing you to Simplii-' in response.data

def test_forum(client):

    with client[0].session_transaction() as sess:
        sess['email'] = 'apexarcheole@gmail.com'
        sess['name'] = 'Purv'

    #GET request to forum route
    response = client[0].get('/forum')
    #Assert that the response is a success
    assert response.status_code == 200
    #Assert that the response contains data from forum.html
    assert b'Create a New Thread' in response.data

    #POST request to forum route
    response = client[0].post('/forum', data = {'thread_title': 'New Title', 'thread_content': 'This is a volatile testing thread.'})
    #Assert that the response is a redirect
    assert response.status_code == 302
    #Assert that the response has redirection to forum
    assert response.location.endswith('/forum')
    # Delete the data that has been added
    mongo.db.threads.delete_one({'title': 'New Title', 'content': 'This is a volatile testing thread.'})

def test_register_without_email(client):

    #GET request to register route
    response = client[0].get('/register')
    #Assert that the response is a success
    assert response.status_code == 200
    #Assert that the response contain data from register.html
    assert b'Join Today' in response.data

    #POST request to register route
    response = client[0].post('/register', data={
    'username': 'archeole21',
    'email': 'apexarcheole@gmail.com',
    'password': '1234',
    'confirm_password': '1234'
    })
    #Assert that the request is redirected
    assert response.status_code == 302
    #Assert that the response has redirection to home
    assert response.location.endswith('/home')
    #Delete the user that was created for testing
    mongo.db.users.delete_one({
    'name': 'archeole21',
    'email': 'apexarcheole@gmail.com',
    })

def test_register_with_email(client):

    with client[0].session_transaction() as sess:
        sess['email'] = 'apexarcheole@gmail.com'

    response = client[0].get('/register')

    #Assert that the response is a redirect
    assert response.status_code == 302
    #Assert that the response has redirection to forum
    assert response.location.endswith('/home')

def test_login_with_email(client):

    with client[0].session_transaction() as sess:
        sess['email'] = 'apexarcheole@gmail.com'

    response = client[0].get('/login')

    #Assert that the response is a redirect
    assert response.status_code == 302
    #Assert that the response has redirection to forum
    assert response.location.endswith('/home')

def test_login_without_email(client):

    response = client[0].post('/login', data = {'email': 'apexarcheole@gmail.com', 'password': '1234'})

    #Assert that the respoonse is redirect
    assert response.status_code == 302
    #Assert that the response has been redirected to dashboard
    assert response.location.endswith('/dashboard')


def test_login_without_email_failed(client):

    response = client[0].post('/login', data = {'email': 'apexarcheole@gmail.com', 'password': 'jsdkhflaiushdla'})
    #Assert that the response is redirect
    assert response.status_code == 200
    #Assert that the response contain data from login.html
    assert b'Log In' in response.data    

def test_task_without_email(client):

    response = client[0].get('/task')

    #Assert that the response is redirect
    assert response.status_code == 302
    #Assert that the response has been redirected to home
    assert response.location.endswith('/home')

def test_task_with_email(client):

    with client[0].session_transaction() as sess:
        sess['email'] = 'apexarcheole@gmail.com'

    response = client[0].post('/task', data ={ 
        'taskname': 'Testing Task', 
        'invitees':["Please Select"], 
        'category':'easy', 
        'startdate': '2023-12-23', 
        'start_time':'1:00', 
        'end_time':'2:00', 
        'description':'asdfaf'})
    
    #Assert that the response is redirect
    assert response.status_code == 302
    #Assert that the response has been redirected to home
    assert response.location.endswith('/home')

    response = client[0].post('/task', data ={
        'email': sess['email'], 
        'taskname': 'Testing Task', 
        'invitees':["Please Select"], 
        'category':'easy', 
        'startdate': '2023-12-23', 
        'start_time':'1:00', 
        'end_time':'2:00', 
        'description':'asdfaf'})
    
    #Assert that the response is redirect
    assert response.status_code == 302
    #Assert that the response has been redirected to home
    assert response.location.endswith('/task')

    #Delete the testing task
    mongo.db.tasks.delete_one({'taskname': 'Testing Task'})

    
