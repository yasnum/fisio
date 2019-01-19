from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from boards.models import Board, Topic, Post
from boards.forms import NewTopicForm, PostForm
from django.http import HttpResponse #new
from django.contrib.auth.decorators import login_required
from django.db.models import Count
#from django.http import Http404
from django.views.generic import UpdateView
from django.utils import timezone
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 

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

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'homeboard.html'

def board_topics(request, pk):
    #board = Board.objects.get(pk=pk)
    board = get_object_or_404(Board, pk=pk)
   ## topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    #return render(request, 'topics.html', {'board': board})
  ##  return render(request, 'topics.html', {'board': board, 'topics': topics})
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 4)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)

    return render(request, 'topics.html', {'board': board, 'topics': topics})
   # try:
   #     board = Board.objects.get(pk=pk)
   # except Board.DoesNotExist:
   #     raise Http404
   # return render(request, 'topics.html', {'board': board})

@login_required
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
            topic.starter = request.user
            topic.save()
            #post = Post.objects.create(
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

#GCBV Pagination
class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

