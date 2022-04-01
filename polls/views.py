from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Question
# Create your views here.

def index(request):
    return HttpResponse("hello world!")

def index2(request):
    myname = "TXD"
    taisan = ["tai san 1", "tai san 2", "tai san 3"]
    context = {"name":myname, "taisan":taisan}

    return render(request, "polls/index.html", context)

def questionList(request):
    # question = get_object_or_404(Question, pk=1)
    question = Question.objects.all()
    context = {"question": question}

    return render(request, "polls/question_list.html", context)

def questionDetail(request, question_id):
    q = Question.objects.get(pk = question_id)
    context = {"question": q}
    return render(request,"polls/question_detail.html",context)

def vote(request, question_id):
    q = Question.objects.get(pk = question_id)
    try:    
        data = request.POST["choicee"]
        c = q.choice_set.get(pk = data)
        c.vote = c.vote + 1
        c.save()
        context = {"question": q}
        return render(request, "polls/result.html", context)
    except:
        return(HttpResponse("khong co data"))