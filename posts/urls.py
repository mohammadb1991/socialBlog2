from django.urls import path
from . import views

app_name='posts'
urlpatterns=[
    path('',views.all_posts ,name='all_posts'),
    path('<int:year>/<int:month>/<int:day>/<int:second>/',views.post_detail,name='post_detail'),
    path('add_post/<int:user_id>/',views.add_post, name='add_post'),
    path('post_delete/<int:userid>/<int:postid>',views.post_delete ,name='post_delete'),
    path('post_edit/<int:userid>/<int:postid>',views.post_edit , name='post_edit'),
    path('add_reply/<int:postid>/<int:commentid>',views.add_reply, name='add_reply'),
    path('like/<int:post_id>',views.post_like,name='post_like'),

    # path('comment_delete/<int:commentid>/<int:userid>',views.comment_delete, name='comment_delete')

]