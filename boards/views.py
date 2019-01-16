from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from boards.models import Board, Topic, Post
from .forms import NewTopicForm
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
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
   # return render(request, 'new_topic.html', {'board': board}) 
   # if request.method == 'POST':
   #     subject = request.POST['subject']
   #     message = request.POST['message']

   #     user = User.objects.first()  # TODO: get the currently logged in user

   #     topic = Topic.objects.create(
   #         subject=subject,
   #         board=board,
   #         starter=user
   #     )

   #     post = Post.objects.create(
   #         message=message,
   #         topic=topic,
   #         created_by=user
   #     )
   #     return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
   
   # return render(request, 'new_topic.html', {'board': board})
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})