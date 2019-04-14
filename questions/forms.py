from django import forms
from .models import Question
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import StrictButton, FieldWithButtons

class QuestionAddForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'text']  # list of fields you want from model
        widgets = {'text': forms.Textarea(attrs={'placeholder': 'Введите текст вопроса'}),
                   'description': forms.Textarea(attrs={'placeholder': 'Введите краткое описание вопроса (300 символов).'}),
        }

    def __init__(self, *args, **kwargs):
        super(QuestionAddForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = "Введите заголовок вопроса"


class SortingForm(forms.Form):
    sort_field = forms.ChoiceField(choices=(('-date', u'Сначала новые'),
                                            ('date', u'Сначала старые'),
                                            ('-rate', u'Сначала популярные')), required=False)

class SearchForm(forms.Form):
    keywords = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(FieldWithButtons('keywords', StrictButton(' <i class="fa fa-search"></i>', type="submit", css_class="btn-primary search-btn"), css_class="d-inline"))