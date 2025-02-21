from django.urls import path
from .views import (
    IndexView,
    DetailView,
    ResultsView,
    CreateQuestionView,
    VoteView,
    ResetVotesView,
    EditQuestionView,
    DeleteQuestionView,
)
"""
app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    
    path('reset_votes/<int:question_id>/', views.reset_votes, name='reset_votes'),
    path('new/', views.CreateQuestionView.as_view(), name="createnew"),
    path("<int:question_id>/edit/", views.edit, name="edit"),
    path('delete/<int:question_id>/', views.delete_question, name='delete'),
]
"""
app_name = "polls"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<int:pk>/", DetailView.as_view(), name="detail"),
    path('new/', CreateQuestionView.as_view(), name="createnew"), 
    path("<int:pk>/edit/", EditQuestionView.as_view(), name="edit"),
    path("<int:pk>/results/", ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", VoteView.as_view(), name="vote"),
    path('reset_votes/<int:question_id>/', ResetVotesView.as_view(), name='reset_votes'),
    path("delete/<int:pk>/", DeleteQuestionView.as_view(), name="delete"),
    #path('delete/<int:question_id>/', views.delete_question, name='delete'),

]