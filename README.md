# Project Description
The project was created to develop programming skills. Calendar is a project using Django, MySQL, HTML, CSS, and Python technologies. The project contains four applications: blog, forum, user profile, and menstrual calendar.

# Blog
On the blog, only administrators can add posts, and logged-in and non-logged-in users can add comments. RichTextField is used for the body of posts and comments.

# Forum
In the forum application, only logged-in users can add new posts and comment on existing ones. RichTextField is used for the body of posts and comments.

# Users
The user account application allows for registration, password change, and password reset with the submission of a token and email in the terminal (only in the production stage). On the user's main profile, there are links to the latest commented posts and quick access to menstrual calendar options.

# Cycle Calendar
The main part of the project is the menstrual calendar. Logged-in users can add their personalized calendar or add a user's calendar from whom they received a special code. After creating a personalized calendar, twelve personalized cycles are automatically generated that the user can view. After creating the calendar, the user can change personalized data that affects predicted cycles and reset the current cycle, which also generates personalized cycles. The last option is the ability to share your calendar with another person. By going to the Share tab, we go to the page with generating a unique code assigned to our profile. By sending this code, we only share viewing our menstrual calendar with another person. In the Share List tab, we can see who is observing our calendar and remove people, revoking their access to our calendar.

# Technologies
The project uses the following technologies:
 
- Python - programming language
- Django - web framework in Python
- MySQL - database management system
- HTML - markup language for creating web pages
- CSS - style sheet for describing the look of web pages

# Planned Changes
Planned changes for the project in the future include:

1. Optimizing the display of the menstrual calendar
2. Deployment through Heroku
3. Adding post and comment editing on the forum by users.

# Cloning the repository

Clone the repository using the command below :
```bash
git clone https://github.com/UserMarekDrag/calendar.git
```

Move into the directory where we have the project files : 
```bash
cd calendar
```

Create a virtual environment :
```bash
# Create our virtual environment
python -m venv venv
```

Activate the virtual environment : <br><br>
windows
```bash
venv\scripts\activate
```
linux
```bash
source venv/bin/activate
```

Install the requirements :
```bash
pip install -r requirements.txt
```

Migrate Database
```bash
python manage.py migrate
```

Create Super User
```bash
python manage.py createsuperuser
```

### Running the App

To run the App, we use :
```bash
python manage.py runserver
```
> ⚠ Then, the development server will be started at http://127.0.0.1:8000/


# Author
Marek Drąg

## Documentation
You can check up django documentation page for any further information.
[Django Docs](https://docs.djangoproject.com/en/4.0/)