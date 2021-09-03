from django.shortcuts import render, redirect
from .forms import UserSignupForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        new_user = UserSignupForm(request.POST)
        if new_user.is_valid():
            new_user.save()
            return redirect('home')
        else:
            context = { "form": new_user }
            return render(request, 'users/signup.html', context)
    else:
        form = UserSignupForm()
        context = { "form": form }
        return render(request, 'users/signup.html', context)