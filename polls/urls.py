from django.urls import path
from . import views
from .views import (
    IndexView,
    DetailView,
    ResultsView,
    CreateQuestionView,
    CreateQuestionWithoutPostView,
    VoteView,
    ResetVotesView,
    EditQuestionView,
    DeleteQuestionView,
)

app_name = "polls"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<int:pk>/", DetailView.as_view(), name="detail"),
    path('create/<int:post_id>/', views.create_poll, name='createnew'),
    path('create/', CreateQuestionWithoutPostView.as_view(), name='create_without_post'),
    path("<int:pk>/edit/", EditQuestionView.as_view(), name="edit"),
    path("<int:pk>/results/", ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", VoteView.as_view(), name="vote"),
    path('reset_votes/<int:question_id>/', ResetVotesView.as_view(), name='reset_votes'),
    path("delete/<int:pk>/", DeleteQuestionView.as_view(), name="delete"),
]

