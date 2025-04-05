from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
import copy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

QUESTIONS = [
    {
        'title' : f'Title {i}', 
        'id' : i,
        'text' : f'This is text for question {i}',
    } for i in range(30)
]

ANSWERS = [
    {
        'text': f'This is text for answer {i}',
        'rating': 5,
        'id': i,
    } for i in range(10)
] 

def paginate(objects_list, request, per_page=10):
    try:
        page_num = int(request.GET.get('page', 1))
    except(TypeError, ValueError):
        page_num = 1
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        if page_num < 0:
            page = paginator.page(1)
        else:
            page = paginator.page(paginator.num_pages)
    return page

# Create your views here.
def index(request):
    page = paginate(QUESTIONS, request, 5)
    return render(request, template_name='index.html', context={'questions' : page.object_list, 'page_obj' : page})

def hot(request):
    q = copy.deepcopy(QUESTIONS)[::-1]
    page = paginate(q, request, 5)
    return render(request, template_name='hot.html', context={'questions' : page.object_list, 'page_obj' : page})

def question(request, question_id):
    page = paginate(ANSWERS, request, 5)
    return render(request, template_name='single_question.html', context={'question' : QUESTIONS[question_id], 'answers' : page.object_list, 'page_obj': page})

def login(request):
    return render(request, template_name='login.html')

def signup(request):
    return render(request, template_name='signup.html')

def ask(request):
    return render(request, template_name='ask.html')

def tag(request, tag):
    page = paginate(QUESTIONS, request, 5)
    return render(request, template_name="questions_by_tag.html", context={'questions' : page.object_list, 'page_obj' : page, 'tag' : tag})

def profile(request):
    return render(request, template_name='profile.html')