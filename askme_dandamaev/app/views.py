from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
import copy
from app.models import Question, Answer, Tag
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    questions = Question.objects.new()
    page = paginate(questions, request, 5)
    return render(request, template_name='index.html', context={'questions' : page.object_list, 'page_obj' : page})

def hot(request):
    questions = Question.objects.hot()
    page = paginate(questions, request, 5)
    return render(request, template_name='hot.html', context={'questions' : page.object_list, 'page_obj' : page})


def question(request, question_id):
    try:
        question, answers = Question.objects.get_question_with_answers(question_id)  
        page = paginate(answers, request, 5)
        return render(request, 'single_question.html', {
            'question': question,
            'answers': page.object_list,
            'page_obj': page,
        })
    except Question.DoesNotExist:
        raise Http404("Вопрос не найден")

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