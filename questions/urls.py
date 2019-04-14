from django.urls import path, re_path
from . import views
from answers.views import AnswerDelete, AnswerUpdate


urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question_list'),
    re_path(r'^question/(?P<pk>\d+)$', views.QuestionView.as_view(), name='question_detail'),
    re_path(r'^add$', views.QuestionAddView.as_view(), name='question_add'),
    path('edit_rate/<int:pk>/', views.edit_rate, name='edit-rate'),
    path('user/<int:pk>/', views.UserQuestionListView.as_view(), name='user-questions'),
    path('question/<int:pk>/delete/', views.QuestionDelete.as_view(), name='question-delete'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('answer/<int:pk>/delete/', AnswerDelete.as_view(), name='answer-delete'),
    path('answer/<int:pk>/update/', AnswerUpdate.as_view(), name='answer-update'),
    path('question/<int:pk>/update/', views.QuestionUpdate.as_view(), name='question-update'),

]
