from django.shortcuts import render
from boards.models import Board
from django.http import HttpResponse #new

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