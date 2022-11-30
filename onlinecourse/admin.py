from django.contrib import admin
# <HINT> Import any new Models here
from .models import Course, Lesson, Instructor, Learner, Question, Lesson, Choice

# <HINT> Register QuestionInline and ChoiceInline classes here

# https://github.com/ibm-developer-skills-network/final-cloud-app-with-database/blob/master/onlinecourse/admin.py

# Register your models here.
#---------------------------------------
class ChoiceInline(admin.StackedInline):
    model = Choice


class QuestionInline(admin.StackedInline): 
    model = Question
    


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    extra= 1




# -------------------------------Original 
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1 # 5 original


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline,QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


class LessonAdmin(admin.ModelAdmin):

    list_display = ['title']


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)

# -------------------------------Original  

# <HINT> Register Question and Choice models here

admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)

