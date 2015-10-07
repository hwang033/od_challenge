"""
This module defines helper tool classes or functions
"""

import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def custom_pagination(request, queryset):
    """Pagination helper function

    Arguments:
        request -- the django request object
        queryset -- A django queryset that will be evaluated for pagination

    Returns:
        A tuple (django.core.paginator.Page, str of links for header)
    """

    # processing paging
    page = request.GET.get('page')
    per_page = request.GET.get('per_page')
    if per_page is None or not per_page.isdigit():
       per_page = 50

    # construct queryset
    paginator = Paginator(queryset, per_page)
    try:
        paged_records = paginator.page(page)
    except PageNotAnInteger:
        paged_records = paginator.page(1)
    except EmptyPage:
        paged_records = paginator.page(paginator.num_pages)

    # construct Link url tempalte
    base_url = re.sub('\?.*$', '?', request.build_absolute_uri())
    params = ['%s=%s' % (p, request.GET.get(p))
              for p in request.GET if p != 'page']
    params.append('page=%d')

    link_url_tmplt = base_url + '&'.join(params)

    # generate links for paging
    links = []
    if paged_records.has_previous():
        prev_link = link_url_tmplt % paged_records.previous_page_number()
        links.append("<%s>; rel=prev" % prev_link)
    if paged_records.has_next():
        next_link = link_url_tmplt % paged_records.next_page_number()
        links.append("<%s>; rel=next" % next_link)

    return paged_records, ', '.join(links)
