from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
from .models import Answer
from answers.form import AnswerAddForm
from django.shortcuts import resolve_url, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
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
from django.http import HttpResponseRedirect


def ajax_login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        return django.http.JsonResponse('Unauthorized', status=401, safe=False)

    return wrapper

class AnswerDelete(DeleteView):
    model = Answer

    def get(self, request, *args, **kwargs):
        return redirect('question_list')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()

        if self.object.autor == self.request.user:
            messages.success(request, 'Ответ удален')
            return super(AnswerDelete, self).delete(request, *args, **kwargs)
        messages.error(request, 'Вы не можете удалить этот ответ')
        return redirect('question_detail', pk=self.object.pk)  # Also add id of Article

    def get_success_url(self):
        if self.object.question.pk != None:
            return reverse_lazy('question_detail', kwargs={'pk': self.object.question.pk, })

class AnswerUpdate(LoginRequiredMixin, UpdateView):
    model = Answer
    form_class = AnswerAddForm
    template_name = 'update_answer.html'
    def get_success_url(self):
        return resolve_url('question_detail', pk=self.object.question.pk)

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can delete Articles """
        obj = self.get_object()
        if obj.autor != self.request.user:
            return redirect('question_detail', pk=obj.question.pk)
        return super(AnswerUpdate, self).dispatch(request, *args, **kwargs)


@ajax_login_required
def edit_rate(request, pk):
    if request.is_ajax():
        answer = Answer.objects.get(pk=pk)
        if request.POST['isLike'] == '1':
            answer.rate = answer.rate + 1
            request.user.profile.liked_by_answ.add(answer)
            if(answer.disliked_by_answ.filter(id=request.user.profile.id)):
                request.user.profile.disliked_by.remove(answer)
            answer.save()
        elif request.POST['isLike'] == '0':
            answer.rate = answer.rate - 1
            if (answer.liked_by_answ.filter(id=request.user.profile.id)):
                request.user.profile.liked_by_answ.remove(answer)
            request.user.profile.disliked_by_answ.add(answer)
            answer.save()
        elif request.POST['isLike'] == '3':
            answer.rate = answer.rate + 1
            if (answer.disliked_by_answ.filter(id=request.user.profile.id)):
                request.user.profile.disliked_by_answ.remove(answer)
            answer.save()
        elif request.POST['isLike'] == '2':
            answer.rate = answer.rate - 1
            if (answer.liked_by_answ.filter(id=request.user.profile.id)):
                request.user.profile.liked_by_answ.remove(answer)
            answer.save()
        elif request.POST['isLike'] == '4':
            answer.rate =answer.rate + 2
            request.user.profile.liked_by_answ.add(answer)
            if (answer.disliked_by_answ.filter(id=request.user.profile.id)):
                request.user.profile.disliked_by_answ.remove(answer)
            answer.save()
        elif request.POST['isLike'] == '5':
            answer.rate = answer.rate - 2
            request.user.profile.disliked_by_answ.add(answer)
            if (answer.liked_by_answ.filter(id=request.user.profile.id)):
                request.user.profile.liked_by_answ.remove(answer)
            answer.save()
        new_rate = answer.rate
    else:
        new_rate = "Send AJAX!"

    return HttpResponse(new_rate)
