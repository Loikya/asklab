from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import UserProfileInfo
from django.views.generic import DetailView
from django.db.models import Sum




def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.email = form.cleaned_data.get('email')
            user.profile.age = form.cleaned_data.get('age')
            if (form.cleaned_data.get('avatar_image')):
                user.profile.avatar_image = form.cleaned_data.get('avatar_image')
            user.save()
            return redirect('question_list')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

class UserProfileView(DetailView):
    model = UserProfileInfo
    template_name = 'user_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['questions_count'] = self.object.user.created_questions.count()
        context['answers_count'] = self.object.user.answer_set.count()
        context['question_rate'] = self.object.user.created_questions.aggregate(rate_sum=Sum('rate'))['rate_sum']
        context['answer_rate'] = self.object.user.answer_set.aggregate(rate_sum=Sum('rate'))['rate_sum']
        return context

