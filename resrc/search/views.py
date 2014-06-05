#-*- coding: utf-8 -*-:
from django.shortcuts import render
from forms import LinksSearchForm


def search(request):
    if 'q' in request.GET:
        query = request.GET['q']
    else:
        query = ''

    # we retrieve the query to display it in the template
    form = LinksSearchForm(request.GET)

    # we call the search method from the LinksSearchForm. Haystack do the work!
    results = form.search()

    return render(request, 'search/search.html', {
        'query' : query,
        'links' : results,
    })
