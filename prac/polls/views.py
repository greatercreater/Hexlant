from django.shortcuts import render
from .models import Board

# Create your views here.
def boardView(request):
    template_name = 'polls/poll.html'
    board_object = Board.objects.all()
    context = {
        'boardobject':board_object
    }
    return render(request, template_name, context)
