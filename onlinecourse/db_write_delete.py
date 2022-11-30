# Django specific settings
import inspect
import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
#from django.db import connection
# Ensure settings are read
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()

import sys
from django.conf import settings
import django



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR",BASE_DIR)

# para que encuentre lel modulo "onlinecourse"
sys.path.append(BASE_DIR) #append your main project 


# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


INSTALLED_APPS = ['onlinecourse.apps.OnlinecourseConfig']
#INSTALLED_APPS = ['.apps.OnlinecourseConfig']
INSTALLED_APPS = [
    'onlinecourse.apps.OnlinecourseConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
#settings.configure(DATABASES=DATABASES,INSTALLED_APPS = INSTALLED_APPS)
#django.setup()



from .models import Course

def clean_data():
    # Delete all data to start from fresh
    #Enrollment.objects.all().delete()
    #User.objects.all().delete()
    #Learner.objects.all().delete()
    #Instructor.objects.all().delete()
    Course.objects.all().delete()
    #Lesson.objects.all().delete()


def write_courses():
    # Add Courses
    course_cloud_app = Course(name="Cloud Application Development with Database",
                              description="Develop and deploy application on cloud")
    course_cloud_app.save()
    course_python = Course(name="Introduction to Python",
                           description="Learn core concepts of Python and obtain hands-on "
                                       "experience via a capstone project")
    course_python.save()

    print("Course objects all saved... ")

def write_Questions():
      
    print("write_Questions ")  
   
    # Get related courses
    course_cloud_app = Course.objects.get(name__contains='Cloud')
    print(course_cloud_app)
    #course_python = Course.objects.get(name__contains='Python')

    # Add Question to courses
    #course_cloud_app.questions.add()


    # question text
    question_text = "Question1"
    # question grade/mark
    grade =  3
  


print(Course.objects.all())


#def write_Choices():




def populate():
    #clean_data()    
    #write_courses()

    write_Questions()