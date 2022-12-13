from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
from .models import Answer, Question, QuestionSet, User, UserAnswer
from .forms import UserForm


class Register(View):
    def get(self, request):
        form = UserForm()
        return render(request, "mcq/register.html",
                      context={"form": form})

    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username, email, password)
        user.set_password(password)
        user.save()
        messages.success(request, "Registration successful")
        login(request, user)
        return redirect ("catalog") # TODO: make a catalog with the sets of questions


class Login(View):
    def get(self, request):
        form = UserForm()
        return render(request, "mcq/login.html",
                      context={"form": form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            print(username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("catalog")


class Catalog(View):
    def get(self, request):
        question_sets = QuestionSet.objects.all()
        return render(request,
               "mcq/catalog.html",
               {'question_sets':question_sets})


class QuestionView(View):

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        context = {'question': question,
                   'answers': question.answers(),}
        return render(request, 'mcq/question.html', context)

    def post(self, request):
        pass # TODO: gotta have a user first. The user must have the archive of tests.
                #TODO: back to catalog button


class SubmitAnswer(View):
    def get(self, request, question_id):
        answers = request.GET.getlist('answer')
        for answer in answers:
            user_answer = UserAnswer(answer, request.user)
            user_answer.save()
        return redirect(UserAnswer.next_question(question_id)) # Might want to change where this method belongs.