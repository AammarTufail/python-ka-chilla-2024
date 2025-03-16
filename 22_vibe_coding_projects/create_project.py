import os

# Dictionary mapping file paths to their content
files = {
    # portfolio_site/manage.py
    "portfolio_site/manage.py": r'''#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable?") from exc
    execute_from_command_line(sys.argv)
''',

    # portfolio_site/portfolio_site/__init__.py (empty)
    "portfolio_site/portfolio_site/__init__.py": "",

    # portfolio_site/portfolio_site/settings.py
    "portfolio_site/portfolio_site/settings.py": r'''import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'replace-this-with-your-secret-key'
DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'landing',
    'projects',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio_site.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
''',

    # portfolio_site/portfolio_site/urls.py
    "portfolio_site/portfolio_site/urls.py": r'''from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),        # Landing page as the root
    path('projects/', include('projects.urls')),  # Projects page
]
''',

    # portfolio_site/portfolio_site/wsgi.py
    "portfolio_site/portfolio_site/wsgi.py": r'''import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')

application = get_wsgi_application()
''',

    # portfolio_site/landing/__init__.py (empty)
    "portfolio_site/landing/__init__.py": "",

    # portfolio_site/landing/urls.py
    "portfolio_site/landing/urls.py": r'''from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
''',

    # portfolio_site/landing/views.py
    "portfolio_site/landing/views.py": r'''from django.shortcuts import render

def home(request):
    return render(request, 'landing/home.html')
''',

    # portfolio_site/projects/__init__.py (empty)
    "portfolio_site/projects/__init__.py": "",

    # portfolio_site/projects/urls.py
    "portfolio_site/projects/urls.py": r'''from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
]
''',

    # portfolio_site/projects/views.py (with image support)
    "portfolio_site/projects/views.py": r'''import requests
from django.shortcuts import render

def project_list(request):
    github_url = "https://api.github.com/users/AammarTufail/repos"
    try:
        response = requests.get(github_url)
        response.raise_for_status()
        repos = response.json()
    except requests.exceptions.RequestException:
        repos = []

    # Custom short descriptions mapping (repository name -> custom description)
    custom_descriptions = {
        "Project1": "This project uses machine learning to optimize industrial processes.",
        "Project2": "A data visualization tool for industrial KPIs and performance metrics.",
        "Project3": "An automated report generator that integrates various industrial data sources."
    }
    
    # Custom images mapping (repository name -> image URL)
    custom_images = {
        "Project1": "https://link.to/project1_image.png",
        "Project2": "https://link.to/project2_image.png",
        "Project3": "https://link.to/project3_image.png"
    }

    for repo in repos:
        # Override description if custom description exists
        if repo['name'] in custom_descriptions:
            repo['description'] = custom_descriptions[repo['name']]
        # Use custom image if provided; otherwise, use GitHub's open_graph_image_url (if available)
        if repo['name'] in custom_images:
            repo['image_url'] = custom_images[repo['name']]
        else:
            repo['image_url'] = repo.get('open_graph_image_url', '')

    return render(request, 'projects/project_list.html', {'repos': repos})
''',

    # portfolio_site/templates/base.html
    "portfolio_site/templates/base.html": r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Portfolio{% endblock %}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="{% url 'home' %}">Portfolio</a>
        <div class="collapse navbar-collapse">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item"><a class="nav-link" href="{% url 'home' %}">Home</a></li>
                <li class="nav-item"><a class="nav-link" href="{% url 'project_list' %}">Projects</a></li>
            </ul>
        </div>
    </nav>
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
''',

    # portfolio_site/templates/landing/home.html
    "portfolio_site/templates/landing/home.html": r'''{% extends 'base.html' %}
{% block title %}Home{% endblock %}
{% block content %}
<div class="jumbotron">
    <h1 class="display-4">Welcome to My Data Science Portfolio!</h1>
    <p class="lead">I am a Data Scientist specializing in industrial applications. Explore my projects below.</p>
    <hr class="my-4">
    <p>Click below to view my projects from GitHub.</p>
    <a class="btn btn-primary btn-lg" href="{% url 'project_list' %}" role="button">View Projects</a>
</div>
{% endblock %}
''',

    # portfolio_site/templates/projects/project_list.html (updated to include images)
    "portfolio_site/templates/projects/project_list.html": r'''{% extends "base.html" %}
{% block title %}Projects{% endblock %}
{% block content %}
<h2>My GitHub Projects</h2>
{% if repos %}
<ul class="list-group">
    {% for repo in repos %}
    <li class="list-group-item">
        <h4>
            <a href="{{ repo.html_url }}" target="_blank">{{ repo.name }}</a>
        </h4>
        {% if repo.image_url %}
        <img src="{{ repo.image_url }}" alt="{{ repo.name }}" class="img-fluid" style="max-width: 300px;">
        {% endif %}
        <p>{{ repo.description|default:"No description provided." }}</p>
    </li>
    {% endfor %}
</ul>
{% else %}
<p>No repositories found or an error occurred while fetching data.</p>
{% endif %}
{% endblock %}
'''
}

# Function to create the directory structure and write files
def create_project_structure():
    for filepath, content in files.items():
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created {filepath}")

if __name__ == "__main__":
    create_project_structure()
    print("\nDjango portfolio project created successfully in the 'portfolio_site' folder.")
