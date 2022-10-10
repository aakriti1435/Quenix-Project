from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .constants import *


def get_pagination(request, data):
    page = request.GET.get('page', 1)
    paginator = Paginator(data, PAGE_SIZE)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    return data