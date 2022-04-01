from . import views
from django.views.generic import TemplateView
from django.urls import path

app_name = 'polls' #implements URLnamespace

urlpatterns = [
    path('hello/', views.index, name = "index"),
    path('hello2/', views.index2, name= "index2"),
    path('list/', views.questionList, name= "questionList"),
    path('detail/<int:question_id>', views.questionDetail, name="questionDetail"),
    path('result/<int:question_id>', views.vote, name="vote")
]