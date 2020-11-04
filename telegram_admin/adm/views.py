from datetime import date

from dateutil.relativedelta import relativedelta
from django.shortcuts import render, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Shift, Result
from django.db.models import Count
from django.db.models import Q

def index(request):
    labels = []
    data = []
    shift_list = Shift.objects.exclude(Q(user=None) | Q(score=None) | Q(score=0)).order_by('-date')
    # shift_list_q = Shift.objects.exclude(user=None,score=None).order_by('-date')
    for shift in shift_list:
        labels.append(shift.date.strftime('%d.%m'))
        data.append(shift.score)
    paginator = Paginator(shift_list, 10)
    page = request.GET.get('page')
    shift_list = paginator.get_page(page)

    params = {
        'shift_list': shift_list,
        'labels': labels,
        'data': data,
    }
    template = 'adm/index.html'
    return render(request, template, params)


def result(request, shift_id):
    # result = Result.objects.filter(shift_id=shift_id)
    result = get_list_or_404(Result,shift_id=shift_id)
    info = Result.objects.filter(shift_id=shift_id)[0]
    params = {
        "result": result,
        "info":info
    }
    template = 'adm/result.html'
    return render(request, template, params)


def user_result(request, user_id):
    TODAY = date.today()
    MINUS_2_MONTH = TODAY + relativedelta(months=-2)
    shift_list = Shift.objects.filter(user_id=user_id, date__gte= MINUS_2_MONTH).exclude(score=None).order_by('-date')
    negative_results_q = Result.objects.filter(user_id=user_id, result=False).values('category').annotate(dcount=Count('category'))
    params = {
        "shift_list": shift_list,
        'negative': negative_results_q,
    }
    template = 'adm/user_result.html'
    return render(request, template, params)