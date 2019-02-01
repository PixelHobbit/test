from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from .models import Share, ShareType
from read_statistics.utils import read_statistics_once_read

def get_share_list_common_data(request, shares_all_list):
    paginator = Paginator(shares_all_list, settings.EACH_PAGE_SHARES_NUMBER)
    page_num = request.GET.get('page', 1) # 获取url的页面参数（GET请求）
    page_of_shares = paginator.get_page(page_num)
    currentr_page_num = page_of_shares.number # 获取当前页码
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
    share_dates = Share.objects.dates('created_time', 'month', order="DESC")
    share_dates_dict = {}
    for share_date in share_dates:
        share_count = Share.objects.filter(created_time__year=share_date.year,
                                         created_time__month=share_date.month).count()
        share_dates_dict[share_date] = share_count

    context = {}
    context['shares'] = page_of_shares.object_list
    context['page_of_shares'] = page_of_shares
    context['page_range'] = page_range
    context['share_types'] = ShareType.objects.annotate(share_count=Count('share'))
    context['share_dates'] = share_dates_dict
    return context

def share_list(request):
    shares_all_list = Share.objects.all()
    context = get_share_list_common_data(request, shares_all_list)
    return render_to_response('share/share_list.html', context)

def shares_with_type(request, share_type_pk):
    share_type = get_object_or_404(shareType, pk=share_type_pk)
    shares_all_list = Share.objects.filter(share_type=share_type)
    context = get_share_list_common_data(request, shares_all_list)
    context['share_type'] = share_type
    return render_to_response('share/shares_with_type.html', context)

def shares_with_date(request, year, month):
    shares_all_list = Share.objects.filter(created_time__year=year, created_time__month=month)
    context = get_share_list_common_data(request, shares_all_list)
    context['shares_with_date'] = '%s年%s月' % (year, month)
    return render_to_response('share/shares_with_date.html', context)

def share_detail(request, share_pk):
    share = get_object_or_404(Share, pk=share_pk)
    read_cookie_key = read_statistics_once_read(request, share)

    context = {}
    context['previous_share'] = Share.objects.filter(created_time__gt=share.created_time).last()
    context['next_share'] = Share.objects.filter(created_time__lt=share.created_time).first()
    context['share'] = share
    response = render_to_response('share/share_detail.html', context) # 响应
    response.set_cookie(read_cookie_key, 'true') # 阅读cookie标记
    return response
