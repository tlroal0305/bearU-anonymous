from django.shortcuts import render, redirect
from board.models import Post, Comment
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
import uuid

# 게시글 리스트 
def board( request ):
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
  
# 게시글 작성 
@login_required( login_url="signin")
def post_write( request ):
  if request.method == "GET":
    return render( request, "page/post_write.html" )
  
  if request.method == "POST":
    title = request.POST["title"]
    content = request.POST["content"]
    img = request.FILES.get("img", None)
    img_url = ""
    
    # 이미지 저장
    if img:
      img_name = uuid.uuid4()
      ext = img.name.split('.')[-1]
      img_url = f"/upload/{img_name}.{ext}"
      
      # 이미지 저장
      default_storage.save(img_url, img)
      
    
    Post(
      img_url = img_url,
      user = request.user,
      title = title,
      content = content,
    ).save()
    return redirect('board')
  
# 게시글 상세페이지
def post_detail(request, post_id):
    if request.method == "GET":
      print(post_id)
      post = Post.objects.get(id=post_id)
      context = {
            "post": post
      }
      return render(request, 'page/post_detail.html', context)
    
    if request.method == "POST":
      comment = request.POST['comment']
      Comment(
        post_id = post_id,
        content = comment,
      ).save()
      
      return redirect('post_detail', post_id)