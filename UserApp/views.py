from django.shortcuts import render
from .forms import RegisterForm, UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import logout

# Create your views here.
def register(req):
    if req.method == "POST":
        forms=RegisterForm(req.POST)
        if forms.is_valid():
            forms.save()
            return redirect('login')
    else:
        forms = RegisterForm()
    return render(req,"register.html",{'forms':forms})

def logout_view(req):
    logout(req)
    return redirect("login")