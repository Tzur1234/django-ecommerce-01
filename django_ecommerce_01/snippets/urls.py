from django.urls import path

urlpatterns = [
 path('list/', views.SnippetDetail.as_view()),
 path('<int:pk>/', views.SnippetList.as_view()),
]