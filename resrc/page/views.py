# -*- coding: utf-8 -*-:
from resrc.utils import render_template


def home(request):
    return render_template('home.html')


def faq(request):
    return render_template('pages/faq.html')


def about(request):
    return render_template('pages/about.html')
