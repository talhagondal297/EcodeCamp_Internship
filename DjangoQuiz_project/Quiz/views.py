from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from .forms import *
from .models import *
from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            # If user is not authenticated, show a message and do not process the form
            return render(request, 'Quiz/home.html', {
                'questions': QuesModel.objects.all(),
                'error_message': 'You need to be log in to submit the quiz.'
            })
        
        # Process the form if the user is authenticated
        questions = QuesModel.objects.all()
        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            if q.ans == request.POST.get(q.question):
                score += 10
                correct += 1
            else:
                wrong += 1
        percent = score / (total * 10) * 100
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total
        }
        return render(request, 'Quiz/result.html', context)
    
    else:
        questions = QuesModel.objects.all()
        context = {
            'questions': questions
        }
        return render(request, 'Quiz/home.html', context)

def addQuestion(request):    
    if request.user.is_staff:
        form=addQuestionform()
        if(request.method=='POST'):
            form=addQuestionform(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        context={'form':form}
        return render(request,'Quiz/addQuestion.html',context)
    else: 
        return redirect('home') 

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = createuserform(request.POST)
        print("12")
        if form.is_valid():
            try:
                user = form.save()
                print("hello")
                login(request, user)  # Automatically log the user in after registration
                messages.success(request, "Registration successful. You are now logged in.")
                return redirect('home')
            except IntegrityError:
                messages.error(request, "Username already taken. Please choose a different username.")
        else:
            print("Form errors:", form.errors)  # Print form errors for debugging
    else:
        form = createuserform()
    
    context = {
        'form': form,
    }
    return render(request, 'Quiz/register.html', context)
   

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
       context={}
       return render(request,'Quiz/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('/')



