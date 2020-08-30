from django.shortcuts import render, redirect,get_object_or_404
from .models import post,Comment,Voted
from .forms import PostForm,AddCommentForm
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def all_posts(request):
    posts=post.objects.all()
    return render(request, 'posts/allposts.html',{'posts':posts})

def post_detail(request,year,month,day,second):
    posts=get_object_or_404(post,created__year=year,created__month=month,created__day=day,created__second=second)
    comment = Comment.objects.filter(post=posts, is_reply=False)
    reply_form = AddCommentForm()
    can_like=False
    if request.user.is_authenticated:
        if posts.user_can_like(user=request.user):
            can_like=True
    if request.method =='POST':
        form=AddCommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.user=request.user
            new_comment.post=posts
            new_comment.save()
            messages.success(request,'your comment submit successfully','success')
    # else:
    form = AddCommentForm()
    return render(request,'posts/post_detail.html',{'posts':posts,'comments':comment,'form':form,'reply': reply_form ,'can_like':can_like})


@login_required
def add_post(request,user_id):
    if request.user.id==user_id:
        if request.method == 'POST':
            form=PostForm(request.POST)
            if form.is_valid():
                new_post=form.save(commit=False)
                new_post.user=request.user
                new_post.slug = slugify(form.cleaned_data['body'][:30])
                new_post.save()
                messages.success(request,'your post is submited','success')
                return redirect('account:dashboard',user_id)

        else:
            form=PostForm()
        return render(request,'posts/add_post.html',{'form':form})
    else:
        return redirect('account:dashboard',user_id)


#
# @login_required
# def comment_delete(request,commentid,userid):
#     if request.user.id==userid:
#         c=Comment.objects.get(pk=commentid)
#         c.delete()
#         messages.success(request,'your comment deleted successfully','success')
#         post=c.post
#         comment = Comment.objects.filter(post=post, is_reply=False)
#         form=AddCommentForm()
#         return redirect('posts:post_detail')



@login_required
def post_delete(request,userid,postid):
    if request.user.id==userid:
        post.objects.get(pk=postid).delete()
        messages.success(request,'your post was deleted successfully','success')
        return redirect('account:dashboard', userid)
    else:
        return redirect('posts:all_posts')


@login_required
def post_edit(request,userid,postid):
    if request.user.id == userid:
        form = get_object_or_404(post, pk=postid)
        if request.method =='POST':
            p=PostForm(request.POST, instance=form)
            if p.is_valid():
                pe=p.save(commit=False)
                pe.slug=slugify(p.cleaned_data['body'][:30])
                pe.save()
                messages.success(request,'your post edited successfully' ,'success')
                return redirect('account:dashboard',userid)
        else:
            f=PostForm(instance=form)
            return render(request,'posts/post_edit.html',{'f':f})
    else:
        return redirect('posts:all_posts')


@login_required
def add_reply(request,postid,commentid):
    p=post.objects.get(pk=postid)
    comment=Comment.objects.get(pk=commentid)
    if request.method=='POST':
        form=AddCommentForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.user=request.user
            f.post=p
            f.reply=comment
            f.is_reply=True
            f.save()
            messages.success(request,'you replyed successfully','success')
    return redirect('posts:post_detail',p.created.year,p.created.month,p.created.day,p.created.second )


def post_like(request,post_id):
    p=get_object_or_404(post,pk=post_id)
    # can_like=p.user_can_like(user=request.user)
    like=Voted(post=p,user=request.user)
    like.save()
    messages.success(request,'you like successfully','success')
    return redirect('posts:post_detail', p.created.year, p.created.month, p.created.day, p.created.second)

# Create your views here.
