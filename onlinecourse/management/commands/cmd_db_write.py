from django.core.management.base import BaseCommand, CommandError


from onlinecourse.models import *


#python3 manage.py cmd_db_write

#def out(str):
#   self.stdout.write(self.style.SUCCESS(str))

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

       #print(Course.objects.all())
       #populate()  
       #print_exam()     
       updateGrade()
      
        
       print("Successfully populate")



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

def write_lesson():

    c1 = Course.objects.get(name__contains='Cloud')

    l1=Lesson(title = "Lesson_title", order = 0, course = c1,  content = "content here")
    l1.save()

    c2 = Course.objects.get(name__contains='Python')

    l1=Lesson(title = "Lesson_title", order = 0, course = c2,  content = "content here")
    l1.save()

def populate():
    clean_data()
    write_courses()
    write_lesson()
    write_Questions()



#https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_many/

def write_Questions():
      
    print("write_Questions and choices")  
   
    # Get related courses
    c1 = Course.objects.get(name__contains='Cloud')
    print(c1.id)
    print("Course:",c1)

    l1= Lesson.objects.get(course=c1.id)
    
    print("Lesson:",l1.title," Course:",l1.course.id)

    #course_python = Course.objects.get(name__contains='Python')

    q1=Question(question_text = "Question 1", grade =  30,course=c1,lesson=l1)
    q1.save()
    print("save id",q1.id)
    
    ch = Choice(choice_text="Q1 Choice 1 true",is_correct=True,question_id=q1)
    ch.save()
    ch = Choice(choice_text="Q1 Choice 2 false",is_correct=False,question_id=q1)
    ch.save()
    ch = Choice(choice_text="Q1 Choice 3 false",is_correct=False,question_id=q1)
    ch.save()



    q2=Question(question_text = "Question 2", grade =  30,course=c1,lesson=l1)
    q2.save()

    print("save id",q2.id)
    ch = Choice(choice_text="Q2 Choice 1 true",is_correct=True,question_id=q2)
    ch.save()
    ch = Choice(choice_text="Q2 Choice 2 false",is_correct=False,question_id=q2)
    ch.save()
    ch = Choice(choice_text="Q2 Choice 3 false",is_correct=False,question_id=q2)
    ch.save()


    q3=Question(question_text = "Question 3", grade =  40,course=c1,lesson=l1)
    q3.save()
    print("save id",q3.id)
    ch = Choice(choice_text="Q3 Choice 1 true",is_correct=True,question_id=q3)
    ch.save()
    ch = Choice(choice_text="Q3 Choice 2 false",is_correct=False,question_id=q3)
    ch.save()
    ch = Choice(choice_text="Q3 Choice 3 false",is_correct=False,question_id=q3)
    ch.save()



    #print(Question.objects.all())


def updateGrade():
     questions =  Question.objects.all()
     for q in questions:
        q.grade=30
        q.save()
     lastq= questions[len(questions)-1]
     lastq.grade=40
     lastq.save()







def print_exam():

    # Get related courses
    c1 = Course.objects.get(name__contains='Cloud')
    print(c1.id)
    print("Course:",c1)

    print("question:",c1.question_set.all())
    for q in c1.question_set.all():
        print(q.question_text)
        for ch in q.choice_set.all():
            print(ch.choice_text)









    

