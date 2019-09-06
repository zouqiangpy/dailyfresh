from django.urls import path,re_path,reverse
from .views import RegisterView,login,ActiveView
urlpatterns = [
    path('active/<str:id>', ActiveView.as_view(), name='active'),
    path('login/', login, name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]


