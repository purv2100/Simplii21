### Module application

#### Functions

##### `about_us()`

The `about_us()` function displays the About Us page (about.html) template. The route "/about" will redirect to the `about_us()` function.

##### `ajaxapproverequest()`

The `ajaxapproverequest()` function updates friend request information in the database. The route "/ajaxapproverequest" redirects to the `ajaxapproverequest()` function. Details corresponding to the given email address are fetched from the database entries, and approve request details are updated.

- **Input:**
  - Email (retrieved from the session)
  - Receiver (retrieved from the form data in the request)

- **Output:**
  - Database update of accept as TRUE information into the database.
  - Returns JSON response with status True if the operation is successful, and False otherwise.

##### `ajaxcancelrequest()`

The `ajaxsendrequest()` function updates friend request information in the database. The route "/ajaxsendrequest" redirects to the `ajaxsendrequest()` function. Details corresponding to the given email address are fetched from the database entries, and send request details are updated.

- **Input:**
  - Email (retrieved from the session)
  - Receiver (retrieved from the form data in the request)

- **Output:**
  - Database entry of receiver information into the database.
  - Returns JSON response with status True if the operation is successful, and False otherwise.

##### `ajaxsendrequest()`

The `ajaxsendrequest()` function updates friend request information in the database. The route "/ajaxsendrequest" redirects to `ajaxsendrequest()` function. Details corresponding to the given email address are fetched from the database entries, and send request details are updated.

- **Input:**
  - Email (retrieved from the session)
  - Receiver (retrieved from the form data in the request)

- **Output:**
  - Database entry of receiver information in the database.
  - Returns JSON response with status True if the operation is successful, and False otherwise.

##### `analytics()`

Display analytics information based on user's tasks.

The "/analytics" route generates and displays various charts and graphs based on the user's tasks. It checks if the user is logged in (session email is present) and if there are tasks associated with the user. If tasks are found, it generates the following analytics:

1. **Task Complexity Histogram** based on 'Category' (Easy, Medium, Hard).
2. **Side-by-side bar chart** of expected hours and actual hours required to complete tasks.
3. **Time charts** showing the distribution of completed tasks across different years, months, and weeks.
4. **Pie chart** to show the distribution of completed and incomplete tasks.

**Input:**
- Takes in user email as input from session.

**Output:**
- Rendered template 'analytics.html' with the following variables:
  - `hist_html`: HTML representation of the Task Complexity Histogram.
  - `exp_act_html`: HTML representation of the Side-by-side bar chart for Expected vs Actual Hours.
  - `by_year_html`: HTML representation of the Year-wise distribution of completed tasks.
  - `by_month_html`: HTML representation of the Monthly distribution of completed tasks.
  - `by_week_html`: HTML representation of the Weekly distribution of completed tasks.
  - `pie_html`: HTML representation of the Completed vs Incomplete Tasks Pie chart.
  - `title`: 'Analytics'.

##### `completeTask()`

The `completeTask()` function marks a task as completed. The "/complete_task" route handles marking a task as completed. If the user is logged in (session email is present), it updates the 'tasks' collection in the MongoDB to mark the specified task as completed. It also calculates and updates the progress for the task.

- **Input:**
  - If the user is logged in and the request method is POST:
    - Email (retrieved from the session)
    - Task name (retrieved from the form submission)
    - Actual hours taken to complete the task (retrieved from the form submission)

- **Output:**
  - If the user is logged in and the request method is POST:
    - If the task is already completed, flash a danger message: 'Task already completed!'
    - If the task is not completed:
      - Flash a success message: '{task} Task Completed!'
      - Redirect to the home page.

##### `dashboard()`

The `dashboard()` function displays the user's tasks on the dashboard. The "/dashboard" route displays the user's tasks on the dashboard. If the user is logged in (session email is present), the route fetches tasks from the database associated with the user's email and passes them to the 'dashboard.html' template.

- **Input:**
  - Takes in user email as input from session

- **Output:**
  - Rendered template 'dashboard.html' with the 'tasks' variable.
        - tasks: A list of tasks associated with the user's email

##### `deleteTask()`

The `deleteTask()` function will delete the particular user task from the database. The route "/deleteTask" redirects to `deleteTask()` function.

- **Input:**
  - The function takes email, task, status, category as the input and fetches from the database

- **Output:**
  - Our function will delete the particular user task from the database.

##### `emailReminder()`

The `emailReminder()` function is called by a cron job that runs at 8 am every day. This function checks if there is any uncompleted task that is due the next day. If yes, then it reminds the user to complete that task.

- **Output:**
  - Sends emails to users about uncompleted tasks.

##### `forgotPassword()`

The `forgotPassword()` function handles the password reset functionality. The route "/forgot_pass" is responsible for handling the password reset functionality. If the user is not logged in (session email is not present), the route renders the 'forgotPass.html' template and handles the submission of the password reset form.

- **Input:**
  - If the request method is POST:
    - Email (retrieved from the form submission)

- **Output:**
  - Rendered template 'forgotPass.html' with the 'title' and 'form' variables.

##### `friends()`

The `friends()` function displays the list of friends corresponding to the given email. The route "/friends" will redirect to the `friends()` function, which further redirects to the 'friends.html' page. The `friends()` function presents a list of functionalities such as "My Friends," "Add Friends," "Send Request," and "Pending Approvals." Details corresponding to the given email address are fetched from the database entries.

**Input:**
- Email (retrieved from the session)

**Output:**
- Rendered template 'friends.html' with the following variables:
  - `allUsers`: A list of all users with their names and emails.
  - `pendingRequests`: A list of friend requests sent by the user that are pending approval.
  - `active`: The email address of the current user.
  - `pendingReceivers`: A list of users who have sent friend requests to the current user (pending approval).
  - `pendingApproves`: A list of users whose friend requests to the current user are pending approval.
  - `myFriends`: A list of accepted friend relationships (sender, receiver, accept=True).
  - `myFriendsList`: A list of email addresses corresponding to the user's accepted friends.

##### `home()`

The `home()` function displays the homepage of our website. The route "/home" redirects to `home()` function.

- **Input:**
  - The function takes the session as the input

- **Output:**
  - Our function will redirect to the login page

##### `login()`

The `login()` function handles user login functionality. The "/login" route handles user login. If the user is not already logged in (session email is not present), it renders the login form. If the form is submitted and passes validation, it checks the credentials against the MongoDB 'users' collection and logs in the user if successful.

- **Input:**
  - If the user is not logged in:
    - If the request method is GET:
      - Rendered template 'login.html' with the login form.
    - If the request method is POST and the form validates successfully:
      - User credentials (retrieved from the form submission).
      - Check if the provided credentials match an entry in the 'users' collection.
        - If matched, flash a success message, log in the user, and redirect to the dashboard.
        - If not matched, flash an error message.
  - If the user is already logged in:
    - Redirect to the home page.

##### `forum()`

  forum() is a Flask route function that handles both GET and POST requests for the "/forum" route.
  If the request method is POST, it processes form submissions for creating new threads or replying to existing threads.
  If the request method is GET, it retrieves all threads from the 'threads' collection and renders the 'forum.html' template.
  
  POST Request (Creating a new thread):
  - Input:    
      - thread_title: Title of the new thread
      - thread_content: Content of the new thread
  
  - Output:
      - Creates a new thread document in the 'threads' collection with the following details:
          - user_email: Email of the user from the session
          - user: User's name from the session
          - title: Title of the thread
          - content: Content of the thread
          - timestamp: UTC timestamp of the thread creation
          - replies: An empty list to store replies for this thread
          - color: A randomly generated color code for the thread
      - Redirects back to the forum page after creating the new thread.
  
  POST Request (Replying to an existing thread):  
  - Input:
      - thread_id: ObjectId of the thread to which the user is replying
      - reply_content: Content of the reply
  
   -  Output:
        - Updates the specified thread document in the 'threads' collection by adding a new reply with the following details:
            - user_email: Email of the user from the session
            - user: User's name from the session
            - content: Content of the reply
            - timestamp: UTC timestamp of the reply
        - Redirects back to the forum page after processing the reply.
  
  GET Request:   
  - Output:    
      - Retrieves all threads from the 'threads' collection.
      - Renders the 'forum.html' template with the title 'Forum' and the list of threads.

    
