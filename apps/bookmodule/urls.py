from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="books.index"),
    path('index2/<int:val1>/', views.index2, name="books.index2"),
    path('<int:bookId>', views.viewbook),
]