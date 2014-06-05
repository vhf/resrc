#-*- coding: utf-8 -*-:
from haystack.forms import SearchForm


class LinksSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        # (the main work is run internally by Haystack here).
        sqs = super(LinksSearchForm, self).search()


        # if something goes wrong
        if not self.is_valid():
            return self.no_query_found()

        # you can then adjust the search results and ask for instance
        # to order the results by title
        sqs = sqs.order_by('title')

        return sqs
