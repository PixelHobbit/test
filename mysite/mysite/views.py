from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data
from blog.models import Blog
from notice.models import Notice

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    notice = Notice.objects

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['notice'] = notice
    return render_to_response('home.html', context)

def page_not_found(request):
    return render_to_response('404.html')
