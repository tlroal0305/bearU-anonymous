from django.shortcuts import render
from board.models import Post
from django.core.paginator import Paginator

def board(request):
  # 게시글 리스트 
  if request.method == "GET":
    page = request.GET.get('page', 1)
    search_text = request.GET.get('search_text', "")
    post_set = Post.objects.filter(title__icontains = search_text).order_by('-id')
    paginator = Paginator(post_set, 4)
    
    post_set= paginator.get_page(page)
    
    context = {
      "post_set": post_set,
      "search_text": search_text 
    }
    return render (request, 'page/index.html', context=context)
  