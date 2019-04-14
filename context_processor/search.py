from questions.forms import SearchForm


def search(request):
    form = SearchForm()
    return {"search_form" : form}