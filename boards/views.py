from django.shortcuts import render, get_object_or_404
from boards.models import Board
from django.http import HttpResponse #new
#from django.http import Http404

# Create your views here.

def homes(request):
    #return HttpResponse('Hello, World!')
    #boards = Board.objects.all()
    #return render(request, 'homeboard.html', {'bord': boards})
   # boards_names = list()
   #for board in boards:
   #    boards_names.append(board.name)
   #response_html = '<br>'.join(boards_names)
    
    #return HttpResponse(response_html)
    boards = Board.objects.all()
    return render(request, 'homeboard.html', {'boards': boards})

def board_topics(request, pk):
    #board = Board.objects.get(pk=pk)
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})
   # try:
   #     board = Board.objects.get(pk=pk)
   # except Board.DoesNotExist:
   #     raise Http404
   # return render(request, 'topics.html', {'board': board})