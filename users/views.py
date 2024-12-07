from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib import messages

# Create your views here.


class Login(View):
    @staticmethod
    def get(request):
        return render(request, "login.html")

    def post(self,request):
        Data = request.POST
        username = Data.get("username")
        Password = Data.get("password")
        user = authenticate(username=username, password=Password)

        if user:
            login(request, user)
            if user.user_role == 'Admin':
                return redirect("/dashboard")
            else:
                return redirect("userdasboard")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("/login")