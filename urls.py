from django.urls import path
from .views import hello,signup,login,logout,contacts,chat,forgot,setpwd,search
urlpatterns=[
    path('hello/',hello,name='hello'),
    path('signup/',signup,name='signup'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('contacts/<str:user_name>',contacts,name='contacts'),
    path('chat/',chat,name='chat'),
    path('forgot/',forgot,name='forgot'),
    path('setpwd/<str:user_name>',setpwd,name='setpwd'),
    path('search/<str:user_name&<str:search_input',search,name='search'),
]