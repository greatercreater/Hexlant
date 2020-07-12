from django.shortcuts import render
from .models import Page


def noticeView(request):
    template_name='notice/notice.html'
    notice_object=Page.objects.all()
    context={
        'noticeboard':notice_object
        }
    return render(request, template_name, context)

# Create your views here.
