from django.shortcuts import render, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Shift, Result


def index(request):
    shift_list = Shift.objects.all().order_by('-date')
    paginator = Paginator(shift_list, 10)
    page = request.GET.get('page')
    shift_list = paginator.get_page(page)


    params = {
        'shift_list': shift_list,
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
