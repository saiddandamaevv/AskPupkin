from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
import copy

QUESTIONS = [
    {
        'title' : f'Title {i}', 
        'id' : i,
        'text' : f'This is text for question {i}',
    } for i in range(30)
]

# Create your views here.
def index(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, per_page = 5)
    page = paginator.page(page_num)
    return render(request, template_name='index.html', context={'questions' : page.object_list, 'page_obj' : page})

def hot(request):
    q = copy.deepcopy(QUESTIONS)[::-1]
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(q, per_page = 5)
    page = paginator.page(page_num)
    return render(request, template_name='hot.html', context={'questions' : page.object_list, 'page_obj' : page})

def question(request, question_id):
    return render(request, template_name='single_question.html', context={'question' : QUESTIONS[question_id]})

def login(request):
    return render(request, template_name='login.html')

def signup(request):
    return render(request, template_name='signup.html')

def ask(request):
    return render(request, template_name='ask.html')