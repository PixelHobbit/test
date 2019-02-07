from django.shortcuts import render_to_response, get_object_or_404
from .models import Star

def stars_list(request):
    stars = Star.objects.all()
    context = {}
    context['stars'] = stars
    return render_to_response('stars/stars_list.html',context)

def star_detail(request,star_pk):
    star = get_object_or_404(Star,pk=star_pk)
    context = {}
    context['star'] = star
    response = render_to_response('stars/star_detail.html', context)
    return response
