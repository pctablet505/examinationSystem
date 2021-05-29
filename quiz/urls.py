from django.urls import path
from quiz import views

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('add/<str:quiz_id>', views.add, name='add'),
    path('submit/<str:quiz_id>', views.submit, name='submit'),
    path('participate', views.participate, name='participate'),
    path('givequiz/<int:question_number>', views.qive_quiz, name='givequiz'),
    path('finish', views.finish, name='finish'),
]
