from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
from .models import Question
from .forms import QuestionAddForm, SortingForm, SearchForm
from answers.form import AnswerAddForm
from django.shortcuts import resolve_url, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse
import functools
import django.http
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


def ajax_login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        return django.http.JsonResponse('Unauthorized', status=401, safe=False)

    return wrapper

from functools import wraps


class QuestionListView(ListView):
    model = Question
    template_name = 'questions.html'
    context_object_name = 'questions'
    #paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        self.sort_form = SortingForm(request.GET)
        self.sort_form.is_valid()
        return super(QuestionListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        questions = Question.objects.all().order_by('-date')
        if self.sort_form.cleaned_data['sort_field']:
            questions = Question.objects.all().order_by(self.sort_form.cleaned_data['sort_field'])
        return questions

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        context['sort_form'] = self.sort_form
        if self.sort_form.cleaned_data['sort_field']:
            context['current_sort_field'] = self.sort_form.cleaned_data['sort_field']
        return context

class UserQuestionListView(ListView):
    model = Question
    template_name = 'user_questions.html'
    context_object_name = 'questions'
    #paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        self.sort_form = SortingForm(request.GET)
        self.sort_form.is_valid()
        self.user_pk = self.kwargs.get('pk')
        return super(UserQuestionListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        questions = Question.objects.filter(autor_id=self.user_pk).order_by('-date')
        if self.sort_form.cleaned_data['sort_field']:
            questions = Question.objects.all().order_by(self.sort_form.cleaned_data['sort_field'])
        return questions

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserQuestionListView, self).get_context_data(**kwargs)
        context['sort_form'] = self.sort_form
        context['username'] = User.objects.get(pk=self.user_pk)
        if self.sort_form.cleaned_data['sort_field']:
            context['current_sort_field'] = self.sort_form.cleaned_data['sort_field']
        return context


@method_decorator(login_required, name='dispatch')
class QuestionAddView(LoginRequiredMixin, CreateView):
    form_class = QuestionAddForm
    template_name = 'add_question.html'

    def get_success_url(self):
        return resolve_url('question_detail', pk=self.object.pk)
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super(QuestionAddView, self).form_valid(form)


class QuestionDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('question_list')

    def get(self, request, *args, **kwargs):
        return redirect('question_list')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.object.autor == self.request.user:
            messages.success(request, 'Вопрос удален')
            return super(QuestionDelete, self).delete(request, *args, **kwargs)
        messages.error(request, 'Вы не можете удалить этот вопрос')
        return redirect('question_detail', pk=self.object.pk)  # Also add id of Article

class QuestionUpdate(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionAddForm
    template_name = 'add_question.html'
    def get_success_url(self):
        return resolve_url('question_detail', pk=self.object.pk)

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can delete Articles """
        obj = self.get_object()
        if obj.autor != self.request.user:
            return redirect('question_detail', pk=obj.pk)
        return super(QuestionUpdate, self).dispatch(request, *args, **kwargs)

class QuestionView(FormMixin, DetailView):
    model = Question
    template_name = 'question_tread.html'
    context_object_name = 'question'
    form_class = AnswerAddForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get_success_url(self):
        return resolve_url('question_detail', pk=self.object.pk)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        new_answer = form.save(commit=False)
        new_answer.autor = self.request.user
        new_answer.question = self.get_object()
        new_answer.save()
        return super(QuestionView, self).form_valid(form)

@ajax_login_required
def edit_rate(request, pk):
    if request.is_ajax():
        question = Question.objects.get(pk=pk)
        if request.POST['isLike'] == '1':
            question.rate = question.rate + 1
            request.user.profile.liked_by.add(question)
            if(question.disliked_by.filter(id=request.user.profile.id)):
                request.user.profile.disliked_by.remove(question)
            question.save()
        elif request.POST['isLike'] == '0':
            question.rate = question.rate - 1
            if (question.liked_by.filter(id=request.user.profile.id)):
                request.user.profile.liked_by.remove(question)
            request.user.profile.disliked_by.add(question)
            question.save()
        elif request.POST['isLike'] == '3':
            question.rate = question.rate + 1
            if (question.disliked_by.filter(id=request.user.profile.id)):
                request.user.profile.disliked_by.remove(question)
            question.save()
        elif request.POST['isLike'] == '2':
            question.rate = question.rate - 1
            if (question.liked_by.filter(id=request.user.profile.id)):
                request.user.profile.liked_by.remove(question)
            question.save()
        elif request.POST['isLike'] == '4':
            question.rate = question.rate + 2
            request.user.profile.liked_by.add(question)
            if (question.disliked_by.filter(id=request.user.profile.id)):
                request.user.profile.disliked_by.remove(question)
            question.save()
        elif request.POST['isLike'] == '5':
            question.rate = question.rate - 2
            request.user.profile.disliked_by.add(question)
            if (question.liked_by.filter(id=request.user.profile.id)):
                request.user.profile.liked_by.remove(question)
            question.save()
        new_rate = question.rate
    else:
        new_rate = "Send AJAX!"

    return HttpResponse(new_rate)


class SearchListView(ListView):
    """
    Display a Blog List page filtered by the search query.
    """
    model = Question
    template_name = 'search_result.html'
    context_object_name = 'questions'

    def dispatch(self, request, *args, **kwargs):
        self.search_form = SearchForm(request.GET)
        self.search_form.is_valid()
        return super(SearchListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = Question.objects.all()
        if self.search_form.cleaned_data['keywords']:
            keywords = self.search_form.cleaned_data['keywords']
            query = SearchQuery(keywords)
            keywords = keywords.split(" ")
            for keyword in keywords:
                query = query| SearchQuery(keyword)

            title_vector = SearchVector('title', weight='A')
            description_vector = SearchVector('description', weight='B')
            text_vector = SearchVector('text', weight='c')
            vectors = title_vector + description_vector + text_vector
            qs = qs.annotate(search=vectors).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vectors, query)).order_by('-rank')

        return qs

