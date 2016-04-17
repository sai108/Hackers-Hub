"""SNSAPP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import url
from django.conf.urls.static import static
from SocialNetworkingSite.views import *

urlpatterns = [

    url(r'^$', home),
    url(r'^login', login),
    url(r'^register', register),
    url(r'^code/(?P<user_id>([0-9]|[a-z])*)', code_page),
    url(r'^compile/(?P<user_id>([0-9]|[a-z])*)', compile_code),
    url(r'^view_all_posts/(?P<user_id>([0-9]|[a-z])*)', get_posts),
    url(r'^logout/(?P<user_id>([0-9]|[a-z])*)', logout),
    url(r'^profile/(?P<user_id>([0-9]|[a-z])*)', Profile.as_view()),
    url(r'^post/(?P<user_id>([0-9]|[a-z])*)', add_a_text_post),
    url(r'^delete/(?P<user_id>([0-9]|[a-z])*)/(?P<post_id>([0-9]|[a-z])*)', delete_post),
    url(r'^edit_post/(?P<user_id>([0-9]|[a-z])*)/(?P<post_id>([0-9]|[a-z])*)', edit_text_post),
    url(r'^post_image/(?P<user_id>([0-9]|[a-z])*)', post_image),
    url(r'^edit_image_post/(?P<user_id>([0-9]|[a-z])*)/(?P<post_id>([0-9]|[a-z])*)', edit_image_post),
    url(r'^post_video/(?P<user_id>([0-9]|[a-z])*)', post_video),
    url(r'^edit_video_post/(?P<user_id>([0-9]|[a-z])*)/(?P<post_id>([0-9]|[a-z])*)', edit_video_post),
    url(r'^attach_file/(?P<user_id>([0-9]|[a-z])*)', post_file),
    url(r'^download_file/(?P<post_id>([0-9]|[a-z])*)', download_file),
    url(r'^edit_file_post/(?P<user_id>([0-9]|[a-z])*)/(?P<post_id>([0-9]|[a-z])*)', edit_file_post),
    url(r'^add_a_comment/(?P<user_id>([0-9]|[a-z])*)/(?P<post_id>([0-9]|[a-z])*)', Comments.as_view()),
    url(r'^delete_comment/(?P<user_id>([0-9]|[a-z])*)/(?P<post_id>([0-9]|[a-z])*)/(?P<comment_id>([0-9]|[a-z])*)',
        delete_comment),

    url(r'^notifications/(?P<user_id>([0-9]|[a-z])*)', Notify.as_view()),
    url(r'^friend_request/(?P<friend_id>([0-9]|[a-z])*)/(?P<user_id>([0-9]|[a-z])*)', post_friend_requests),
    url(r'^accept_request/(?P<friend_id>([0-9]|[a-z])*)/(?P<user_id>([0-9]|[a-z])*)', accept_friend_request),
    url(r'^find_all_friends/(?P<user_id>([0-9]|[a-z])*)', get_all_users),
    url(r'^chat/(?P<user_id>([0-9]|[a-z])*)', get_chat_friends),
    url(r'^chat_box/(?P<user_id>([0-9]|[a-z])*)/(?P<friend_id>([0-9]|[a-z])*)', get_chat),
    url(r'^post_chat/(?P<user_id>([0-9]|[a-z])*)/(?P<friend_id>([0-9]|[a-z])*)', post_chat),
    url(r'^message/(?P<user_id>([0-9]|[a-z])*)/(?P<friend_id>([0-9]|[a-z])*)', message),
    url(r'^delete_msg/(?P<user_id>([0-9]|[a-z])*)/(?P<friend_id>([0-9]|[a-z])*)/(?P<msg_id>([0-9]|[a-z])*)', delete_msg),
    url(r'^challenges-hackerearth/(?P<user_id>([0-9]|[a-z])*)', hackerearthchallenges),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
