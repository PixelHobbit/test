from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from .models import View, ViewType
from read_statistics.utils import read_statistics_once_read

def get_view_list_common_data(request, views_all_list):
    paginator = Paginator(views_all_list, settings.EACH_PAGE_VIEWS_NUMBER)
    page_num = request.GET.get('page', 1) # 获取url的页面参数（GET请求）
    page_of_views = paginator.get_page(page_num)
    currentr_page_num = page_of_views.number # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取日期归档对应的博客数量
    view_dates = View.objects.dates('created_time', 'month', order="DESC")
    view_dates_dict = {}
    for view_date in view_dates:
        view_count = View.objects.filter(created_time__year=view_date.year,
                                         created_time__month=view_date.month).count()
        view_dates_dict[view_date] = view_count

    context = {}
    context['views'] = page_of_views.object_list
    context['page_of_views'] = page_of_views
    context['page_range'] = page_range
    context['view_types'] = ViewType.objects.annotate(view_count=Count('view'))
    context['view_dates'] = view_dates_dict
    return context

def view_list(request):
    views_all_list = View.objects.all()
    context = get_view_list_common_data(request, views_all_list)
    return render_to_response('view/view_list.html', context)

def views_with_type(request, view_type_pk):
    view_type = get_object_or_404(ViewType, pk=view_type_pk)
    views_all_list = View.objects.filter(view_type=view_type)
    context = get_view_list_common_data(request, views_all_list)
    context['view_type'] = view_type
    return render_to_response('view/views_with_type.html', context)

def views_with_date(request, year, month):
    views_all_list = View.objects.filter(created_time__year=year, created_time__month=month)
    context = get_view_list_common_data(request, views_all_list)
    context['views_with_date'] = '%s年%s月' % (year, month)
    return render_to_response('view/views_with_date.html', context)

def view_detail(request, view_pk):
    view = get_object_or_404(View, pk=view_pk)
    read_cookie_key = read_statistics_once_read(request, view)

    context = {}
    context['previous_view'] = View.objects.filter(created_time__gt=view.created_time).last()
    context['next_view'] = View.objects.filter(created_time__lt=view.created_time).first()
    context['view'] = view
    response = render_to_response('view/view_detail.html', context) # 响应
    response.set_cookie(read_cookie_key, 'true') # 阅读cookie标记
    return response
