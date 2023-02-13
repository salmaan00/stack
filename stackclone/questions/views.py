from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,View,ListView,DetailView
# Create your views here.e:/myDjango/myenv/Scripts/activate.bat
# 
from questions.forms import RegistrationForm,LoginForm,QuestionForm,AnswerForm
from questions.models import MyUser,Questions,Answers
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.generic import FormView
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "u must login")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


class IndexView(CreateView,ListView):
    template_name="home.html"
    form_class=QuestionForm
    model=Questions
    success_url=reverse_lazy("index")
    context_object_name="questions"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    def get_queryset(self):
        return Questions.objects.all().exclude(user=self.request.user)

# def signout_view(request,*args,**kwargs):
#     logout(request)
#     return redirect("index")


class SignupView(CreateView):
    model=MyUser
    form_class=RegistrationForm
    template_name='register.html'
    success_url=reverse_lazy("register")

class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"

       

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():

            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
        if usr:
            login(request, usr)
            return redirect("index")
        else:
            messages.error(request,"invalid credentials")
            return render(request,self.template_name,{"form":form})
        
@method_decorator(signin_required,name="dispatch")
class QuestionDetailView(DetailView,FormView):
    model=Questions
    template_name="question-detail.html"
    pk_url_kwarg:str="id"
    context_object_name:str="questions"
    form_class=AnswerForm


# localhost:8000/questions/{id}/answer
def add_answer(request,*args,**kwargs):
   if request.method=="POST":

    form=AnswerForm(request.POST)
    if form.is_valid():
     answer=form.cleaned_data.get("answer")
     qid=kwargs.get("id")
     ques=Questions.objects.get(id=qid)
     Answers.objects.create(questions=ques,user=request.user,answer=answer)
     return redirect("index")
   else:
    return redirect("index")


# localhost:800/answers/{id}/upvote
def upvote_view(request,*args,**kwargs):
    ans_id=kwargs.get("id")
    ans=Answers.objects.get(id=ans_id)
    ans.upvote.add(request.user)
    ans.save()
    return redirect("index")

def remove_view(request,*args,**kwargs):
    ans_id=kwargs.get("id")
    Answers.objects.get(id=ans_id).delete()
    return redirect("index")

@signin_required
def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")
