from django.urls import path
from users.views import Login
urlpatterns = [
    path('', Login.as_view()),
    path('login', Login.as_view()),

]