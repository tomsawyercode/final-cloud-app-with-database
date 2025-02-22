from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
# <HINT> Import any new Models here
from .models import Course, Enrollment, Submission, Choice
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.

#from .db_write import *


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        # Check if user enrolled
        num_results = Enrollment.objects.filter(user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled


# CourseListView
class CourseListView(generic.ListView):

    
    #print("CourseListView")
    #populate()
    
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    
    template_name = 'onlinecourse/course_detail_bootstrap.html'


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()

    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))


# <HINT> Create a submit view to create an exam submission record for a course enrollment,
# you may implement it based on following logic:
         # Get user and course object, then get the associated enrollment object created when the user enrolled the course
         # Create a submission object referring to the enrollment
         # Collect the selected choices from exam form
         # Add each selected choice object to the submission object
         # Redirect to show_exam_result with the submission id
#def submit(request, course_id):

def submit_exam(request, course_id): # to create an exam submission record for a course enrollment,
    print("Exam Submission ---------------------")

    user = User.objects.get(username=request.user)
    print("user:",user.id,request.user)

    # https://docs.djangoproject.com/en/4.1/topics/db/queries/

    #enroll = Enrollment.objects.all()    
    #print(enroll.values(),course_id)
    enrollment = Enrollment.objects.get(user_id=user.id, course_id=course_id)
    print("enrollment:",enrollment)

    submission = Submission.objects.create(enrollment=enrollment)

    # for every question add the choice
    # Add each selected choice object to the submission object
    
    #https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_many/

    answers = extract_answers(request)
    for a in answers:
        print("a:",a)
        ch= Choice.objects.get(id=a)
        submission.choices.add(ch)

    print("   Choices:",submission.choices)
    
    submission.save()


    return HttpResponseRedirect(reverse(viewname='onlinecourse:show_exam_result', args=(course_id,submission.id)))

    # the reverse function allows to retrieve url details from url's.py file through the name value provided there

    #return HttpResponse("Exam Submission course id: {}".format(course_id), content_type="text/plain")




#    Get the current user and the course object, then get the associated the enrollment object

#(HINT: Enrollment.objects.get(user=..., course=...))

#    Create a new submission object referring to the enrollment

#(HINT: Submission.objects.create(enrollment=...))

#    Collect the selected choices from HTTP request object (HINT: you could use request.POST to get the payload dictionary, and

# get the choice id from the dictionary values, an example code snippet is also provided)

 #   Add each selected choice object to the submission object
 #   Redirect to a show_exam_result view with the submission id to show the exam result
 #   Configure urls.py to route the new submit view such as path('<int:course_id>/submit/', ...),



# <HINT> A example method to collect the selected choices from the exam form from the request object
def extract_answers(request):
    submitted_anwsers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_anwsers.append(choice_id)
            print("choice:",choice_id)
    return submitted_anwsers


# <HINT> Create an exam result view to check if learner passed exam and show their question results and result for each question,
# you may implement it based on the following logic:
        # Get course and submission based on their ids
        # Get the selected choice ids from the submission record
        # For each selected choice, check if it is a correct answer or not
        # Calculate the total score


# onlinecourse/17/show_exam_result/8
# http://127.0.0.1:8000/onlinecourse/17/show_exam_result/8


 # https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_many/
def show_exam_result(request, course_id, submission_id):
    print("show_exam_result-------------------------------")

    template_name = 'onlinecourse/exam_result_bootstrap.html'


    submission = Submission.objects.get(id=submission_id)

    print("Submission:",submission.id)
    print("Choices:")
    # Loop over the submission choices
    sub_ch_list=[]
    for ch in submission.choices.all():
        #print("Question:",ch.question_id.question_text)
        #print("   grade:",ch.question_id.grade)
        #print("      ch:",ch.id,ch.choice_text,ch.is_correct)
        sub_ch_list.append(ch.id)

    # Loop over the exam choices
    course = Course.objects.get(id=course_id)
    grade=0
    questions=[]
    for q in course.question_set.all():
        print("Question:",q.question_text)
        print("   grade:",q.grade)

        ch_list=[]
        for ch in q.choice_set.all():        
            color=''
            label=''
            if ch.id in sub_ch_list :
                if ch.is_correct :
                   color="green"
                   grade=grade+q.grade
                   label='Correct answer:'
                else:
                   color= "red"
                   label= 'Wrong answer:'
            else:
                if ch.is_correct :
                   color= "#FFBF00"                   
                   label='Not Selected:'
                else:
                   color= "black"

            print("      ch:",ch.id,ch.choice_text,ch.is_correct,color,label)    
            ch_out = {'choice_text':ch.choice_text,'color':color,'label':label}
            ch_list.append(ch_out)

        q_out={'question_text':q.question_text,'choices':ch_list}
        # add question            
        questions.append(q_out)


    #print("grade:",grade) 
    # Username extraction ?
    # Submissionn-Enrollment->User
    #print("enrollment id:",submission.enrollment.id)      
    #print("enrollment id:",submission.enrollment.user.username)
     




    context={'course_id': course_id,'username':submission.enrollment.user.username,'grade':grade,'questions':questions}

    #print("context:",context)



    #context['course_list'] = course_list
    return render(request, template_name, context)


    #return HttpResponse(" course: {} submission:{}".format(course_id,submission_id), content_type="text/plain")
    #print("course:",course_id,"  submission:", submission_id)



