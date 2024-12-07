from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Create your views here.




class AdminDashboard( LoginRequiredMixin,View):
    login_url = '/login'
    @staticmethod
    def get(request):
        if request.user.user_role == "Admin":
            return render(request, 'admin_dashboard.html')
        else:
            return redirect('/')