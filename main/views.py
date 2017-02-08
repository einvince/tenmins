from django.shortcuts import render, redirect

from tenmins.models import Article, Comment, Ticket, UserProfile
from tenmins.forms import CommentForm, ProfileForm
from django.forms.formsets import formset_factory

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def index(request):
    article_list = Article.objects.all()

    page_robot = Paginator(article_list, 9)
    page_num = request.GET.get('page')
    try:
        article_list = page_robot.page(page_num)
    except EmptyPage:
        article_list = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger:
        article_list = page_robot.page(1)

    context = {}
    context["article_list"] = article_list

    return render(request, 'index.html', context)


def detail(request, id):
    context = {}
    article = Article.objects.get(id=id)
    try:
        user_vote = Ticket.objects.get(voter_id=request.user.id, article_id=id)
        context["user_vote"] = user_vote.choice
    except:
        pass
    if request.method == "GET":
        form = CommentForm
    context["article"] = article
    context['form'] = form
    return render(request, 'detail.html', context)

@login_required()
def detail_vote(request, id):
    if request.method == "POST":
        try:
            user_vote = Ticket.objects.get(
                voter_id=request.user.id, article_id=id)
            print(request.POST["vote"])
            user_vote.choice = request.POST["vote"]
            user_vote.save()
        except ObjectDoesNotExist:
            new_ticket = Ticket(voter_id=request.user.id,
                                article_id=id, choice=request.POST["vote"])
            new_ticket.save()
    return redirect(to='detail', id=id)


def comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            comment = form.cleaned_data["comment"]
            article = Article.objects.get(id=id)
            c = Comment(name=name, comment=comment, belong_to=article)
            c.save()
            return redirect(to="detail", id=id)
    return redirect(to="detail", id=id)


def index_login(request):
    if request.method == "GET":
        form = AuthenticationForm

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(to="index")

    context = {}
    context['form'] = form

    return render(request, 'login.html', context)


def index_register(request):
    if request.method == "GET":
        form = UserCreationForm

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='login')

    context = {}
    context['form'] = form

    return render(request, 'register.html', context)


@login_required(redirect_field_name='index_register',)
def vote(request, id):
    voter_id = request.user.id

    try:
        # 如果找不到登陆用户对此篇文章的操作，就报错
        user_ticket_for_this_article = Ticket.objects.get(
            voter_id=voter_id, article_id=id)
        user_ticket_for_this_article.choice = request.POST["vote"]
        user_ticket_for_this_article.save()
    except ObjectDoesNotExist:
        new_ticket = Ticket(voter_id=voter_id, article_id=id,
                            choice=request.POST["vote"])
        new_ticket.save()

    # 如果是点赞，更新点赞总数
    if request.POST["vote"] == "like":
        article = Article.objects.get(id=id)
        article.likes += 1
        article.save()

    return redirect(to="detail", id=id)


@login_required
def logout(request):
    auth.logout(request)
    return redirect(to='index')


@login_required(redirect_field_name='index')
def profile(request):
    context = {}
    if request.method == 'GET':
        try:
            form = ProfileForm(
                initial={"sex": request.user.profile.sex, "name": request.user.username, })
        except:
            form = ProfileForm(initial={"name": request.user.username,})

        context['form'] = form
    return render(request, 'myinfo.html', context)


@login_required(redirect_field_name='index')
def modify_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.username = form.cleaned_data['name']
            profile=UserProfile(belong_to=request.user)
            profile.sex = form.cleaned_data['sex']
            profile.avatar = request.FILES['avatar']
            profile.save()
            if not authenticate(username=request.user.username, password=form.cleaned_data['password']):
                request.user.set_password(form.cleaned_data['password'])
                request.user.save()
                return redirect(to='login')
            return redirect(to='profile')


@login_required(redirect_field_name='index')
def mycollection(request):
    context = {}
    user_like= Ticket.objects.filter(choice="like",voter=request.user)
    page_robot = Paginator(user_like, 3)
    page_num = request.GET.get('page')

    try:
        user_like_article = page_robot.page(page_num)
    except EmptyPage:
        user_like_article = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger:
        user_like_article = page_robot.page(1)

    context['user_like_article'] = user_like_article


    return render(request, 'mycollection.html', context)
