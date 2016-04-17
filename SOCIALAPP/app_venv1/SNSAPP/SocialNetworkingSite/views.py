import os
import bson
import json
from bson.objectid import ObjectId
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import User, Post, Comment, Chat, Notifications
from django.contrib.auth.hashers import *
from datetime import datetime
from django.shortcuts import redirect
from django.core.files.base import ContentFile
from django.utils.encoding import smart_str
from django.core.files.base import File
from django.views.generic import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from SNSAPP.settings import CLIENT_SECRET
import requests

path = 'D:\\MAJOR PROJECT\\SOCIALAPP\\app_venv1\\SNSAPP\\SocialNetworkingSite\\static\\img'

video_path = 'D:\\MAJOR PROJECT\\SOCIALAPP\\app_venv1\\SNSAPP\\SocialNetworkingSite\\static\\videos\\posted_videos\\'

html_path = 'D:\\MAJOR PROJECT\\SOCIALAPP\\app_venv1\\SNSAPP\\SocialNetworkingSite\\static\\challenges-htm\\hackerearth-challenges.htm'

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  BASIC SITE OPERATIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def home(request):

    """
    :param request: The request comes from the user to load landing page.
    :return:        The landing page home.html is rendered to the user.
    """
    return render(request, 'home.html')


def register(request):

    """
     :param request:The request comes from the user if he wish to register by filling the form
     :return:       The POSTS page is rendered to the user, on successful registration
    """
    _email = request.POST['email']
    _password1 = request.POST['password1']
    _password2 = request.POST['password2']

    if User.objects(email=_email):
        context = {
            "message_register": "Account already in use"
        }
        return render(request, 'home.html', context)

    if _password1 != _password2:
        context = {
            "message_register": "Confirm with same Password"
        }
        return render(request, 'home.html', context)

    _password = make_password(_password1, salt=None, hasher='bcrypt_sha256')
    user = User()
    user.email = _email
    user.password = _password
    user.first_name = request.POST['first_name']
    user.sur_name = request.POST['last_name']
    user.phone_number = request.POST['telephone']
    user.birthday = request.POST['date']
    user.account_created_time = datetime.now()
    user.gender = request.POST.get('gender',)
    user.save()
    request.session['member_id'] = _email
    return redirect('view_all_posts/' + str(user.id))


def login(request):

    """
    :param request: User trying to login from the second time
    :return:  On successful login render the POSTS page to the user
    """
    _email = request.POST['email']
    _password = request.POST['password']
    if User.objects(email=_email):
        user = User.objects(email=_email)
        if check_password(password=_password, encoded=user[0].password):
            request.session['member_id'] = _email    # creating a session using email id of the user.
            return redirect('/view_all_posts/'+str(user[0].id))
        else:
            context = {
                 "message": "Invalid EmailId or Password",
            }
            return render(request, 'home.html', context)
    else:
        context = {
            "message": "No User Found"
        }
        return render(request, 'home.html', context)


def logout(request, user_id):

    """
    :param request:  This def invokes when user tries to logout from the site.
    :param user_id:  The user id of the user comes in as a parameter to register last logged out time.
    :return:  Redirecting to the landing home.html page or session expired page.
    """
    if is_logged_in(request):
        try:
            del request.session['member_id']
            User.objects.filter(id=user_id).update(set__last_logged_out_time=datetime.now())
        except KeyError:
            pass
    else:
        return render(request, 'session_expired.html')

    return redirect('/')


"""""""""""""""""""""""""""""""""""""""""""""
  SOCIAL NETWORKING SITE OPERATIONS
"""""""""""""""""""""""""""""""""""""""""""""


'''''''''''''''''''''''''USERS CODE COMPILATION & RUN'''''''''''''''''''''''''''''''''


def code_page(request, user_id):
    if is_logged_in(request):
        return render(request, 'code_here.html', context={"id": user_id})
    else:
        return render(request, 'session_expired.html')


COMPILE_URL = u'https://api.hackerearth.com/v3/code/compile/'

RUN_URL = u'https://api.hackerearth.com/v3/code/run/'


def compile_code(request, user_id):
    if is_logged_in(request):
        source_code = request.POST['code']
        language = request.POST.get('language',)
        data = {
           'client_secret': CLIENT_SECRET,
           'async': 0,
           'source': source_code,
           'lang': language,
           'time_limit': 5,
           'memory_limit': 262144,
        }
        r = requests.post(RUN_URL, data=data)
        payload = r.json()
        json_obj = payload['run_status']

        output_html = None
        stderr = None
        output = None
        status = None
        status_detail = None
        try:
            output_html = json_obj['output_html']
        except KeyError:
            pass

        try:
            stderr = json_obj['stderr']
        except KeyError:
            pass

        try:
            output = json_obj['output']
        except KeyError:
            pass

        try:
            status = json_obj['status']
        except KeyError:
            pass

        try:
            status_detail = json_obj['status_detail']
        except KeyError:
            pass

        result = {
             "output_html": output_html,
             "stderr": stderr,
             "output": output,
             "status": status,
             "status_detail": status_detail,
        }

        data = {
            "source_code": source_code,
            "option": language,
        }

        return render(request, 'code_here.html', context={"id": user_id, "result": result, "data": data})
    else:
        return render(request, 'session_expired.html')

"""""""""""""""""""""""""""""""""""HACKEREARTH CHALLENGES"""""""""""""""""""""""""""""""""

import BeautifulSoup
import codecs

def hackerearthchallenges(request, user_id):
    if is_logged_in(request):
        file_open = codecs.open(html_path, 'r').read()
        dom = BeautifulSoup.BeautifulSoup(file_open)

        events = dom.findAll('div', {'id': 'live-challenges'})
        dom_1 = BeautifulSoup.BeautifulSoup(str(events[0]))
        live_event_links = []
        for link in dom_1.findAll('a'):
            href = link.get('href')
            name = link.string
            if name is None:
                name = link.span.string
                # img = link.img.get('src')
                live_event_links.append({
                    "name": name,
                    "link": href
                })

        upcoming_events = dom.findAll('div', {'id': 'upcoming-challenges'})
        dom_2 = BeautifulSoup.BeautifulSoup(str(upcoming_events[0]))
        upcoming_events_links = []
        for link in dom_2.findAll('a'):
            href = link.get('href')
            name = link.string
            if name is None:
                name = link.span.string
                upcoming_events_links.append({
                    "name": name,
                    "link": href
                })

        return render(request, 'challenges.html', context={"id": user_id, "live_events": live_event_links,
                                                           "upcoming_events": upcoming_events_links})

    else:
        return render(request, 'session_expired.html')


"""""""""""""""""""""""""""""""""""""PROFILE OPERATIONS"""""""""""""""""""""""""""""""""


class Profile(View):

        def get(self, request,  *args, **kwargs):

            if is_logged_in(request):
                user_id = kwargs['user_id']
                user = User.objects.filter(id=user_id)
                posts = Post.objects.filter(id_of_posted_user=user_id).order_by('-post_time')
                context = {
                   "user": user[0],
                   "posts": posts,
                   "id": user_id,
                }
                return render(request, 'profile.html', context)
            else:
                return render(request, 'session_expired.html')

        def post(self, request, *args, **kwargs):

            return HttpResponseRedirect('/')


"""""""""""""""""""""""POST OPERATIONS(Text Post, Image Post, Video Post, Upload a file)"""""""""""""""""""""""""""""


def add_a_text_post(request, user_id):
    """
    :param request: The request from user is to add a text post on to his page.
    :param user_id: The user is identified by his user id.
    :return: Redirected to view all posts from here.
    """
    if is_logged_in(request):
        post = Post()
        post.id_of_posted_user = user_id
        post.name_of_posted_user = User.objects(id=user_id)[0].first_name
        post.posted_text = request.POST['textarea']
        post.post_time = datetime.now()
        post.save()
        user = User.objects(id=user_id)
        User.objects.filter(id=user_id).update(set__no_of_posts=(user[0].no_of_posts+1))
        return redirect('/view_all_posts/'+str(user_id))
    else:
        return render(request, 'session_expired.html')


def delete_post(request, user_id, post_id):
    """
    :param request:  Request from user is to delete a particular post.
    :param user_id:  The user id of person who requested for delete that post.
    :param post_id:  The id of the post.
    :return:  Redirected to view all the posts.
    """
    if is_logged_in(request):
        post = Post.objects.filter(id=post_id)
        if str(post[0].id_of_posted_user) == str(user_id):

            if post[0].imagePath:
                delete_path = 'D:\\MAJOR PROJECT\\SOCIALAPP\\app_venv1\\SNSAPP\\SocialNetworkingSite'+post[0].imagePath
                os.remove(delete_path)

            if post[0].videoPath:
                delete_path = 'D:\\MAJOR PROJECT\\SOCIALAPP\\app_venv1\\SNSAPP\\SocialNetworkingSite'+post[0].videoPath
                os.remove(delete_path)

            if post[0].uploaded_file_path:
                delete_path = 'D:\\MAJOR PROJECT\\SOCIALAPP\\app_venv1\\SNSAPP\\SocialNetworkingSite'+post[0].uploaded_file_path
                os.remove(delete_path)

            user = User.objects(id=user_id)
            User.objects.filter(id=user_id).update(set__no_of_posts=user[0].no_of_posts-1)
            Post.objects(id=post_id).delete()
            return redirect('/view_all_posts/'+str(user_id))
        else:
            return HttpResponse("You can't Delete others posts")
    else:
        return render(request, 'session_expired.html')


def get_posts(request, user_id):
    """
    :param request: Request from user to view all the post.
    :param user_id: User id is the unique id of the user.
    :return: Returns all the posts to the UI.
    """
    if is_logged_in(request):
        # posts = Post.objects.filter(id_of_posted_user=user_id).order_by('-post_time')
        friends = User.objects(id=user_id)[0].friends
        my_list = []
        for friend in friends:
            my_list.append(unicode(str(friend), 'utf-8'))

        my_list.append(user_id)
        print my_list

        posts = Post.objects.filter(id_of_posted_user__in=my_list).order_by('-post_time')
        context = {
            "posts": posts,
            "id": user_id,
            "obj_id": ObjectId(user_id)
        }

        return render(request, 'posts.html', context)
    else:
        return render(request, 'session_expired.html')


def edit_text_post(request, user_id, post_id):
    """
    :param request:  Request from the user to edit certain post.
    :param user_id:  User id of the user who requested to edit.
    :param post_id:  The Id of the post which should be edited.
    :return:   Redirect to view all the posts.
    """
    if is_logged_in(request):
        post = Post.objects.filter(id=post_id)
        if str(post[0].id_of_posted_user) == str(user_id):
            edit_text = request.POST['textarea']
            Post.objects.filter(id=post_id).update(set__posted_text=edit_text,
                                                   set__post_time=datetime.now(), set__is_edited=True)
            return redirect('/view_all_posts/'+user_id)
        else:
            return HttpResponse("You can't Edit others posts")
    else:
        return render(request, 'session_expired.html')


def post_image(request, user_id):
    """
    :param request: User requesting to post an image.
    :param user_id: The users unique id.
    :return:  The posts page is returned.
    """
    if is_logged_in(request):
        photo_path = path+'\\posted_photos\\'

        if not os.path.exists(photo_path+user_id):
            os.makedirs(photo_path+user_id)

        post = Post()
        uploaded_filename = request.FILES['file'].name     # print(request.FILES.keys())
        extension = uploaded_filename.split(".")[-1]
        full_filename = os.path.join(photo_path, str(user_id), str(datetime.now().strftime("%Y%m%d-%H%M%S"))+'.'+
                                     extension)
        post.post_time = datetime.now()

        try:
            f_out = open(full_filename, 'wb+')
            file_content = ContentFile(request.FILES['file'].read())
        except IOError:
            pass

        try:
            for chunk in file_content.chunks():
                f_out.write(chunk)
            f_out.close()
        except EOFError:
            pass

        post.id_of_posted_user = user_id
        post.name_of_posted_user = User.objects(id=user_id)[0].first_name
        post.imagePath = '/static/img/posted_photos/'+str(user_id)+'/'+full_filename[-19:]
        post.posted_text = request.POST['textarea']
        post.save()
        user = User.objects(id=user_id)
        User.objects.filter(id=user_id).update(set__no_of_posts=user[0].no_of_posts+1)
        return redirect('/view_all_posts/'+user_id)

    else:
        return render(request, 'session_expired.html')


def edit_image_post(request, user_id, post_id):
    """
    :param request: The User requesting to edit his Image post.
    :param user_id: The user_id of the user to uniquely identify.
    :param post_id: The post id of the post.
    :return: Redirects to view all the posts page.
    """
    if is_logged_in(request):
        post = Post.objects.filter(id=post_id)
        if str(post[0].id_of_posted_user) == str(user_id):
            if request.FILES.keys():
                delete_path = 'D:\\MAJOR PROJECT\\SOCIALAPP\\app_venv1\\SNSAPP\\SocialNetworkingSite'+post[0].imagePath
                os.remove(delete_path)

                photo_path = path+'\\posted_photos\\'
                uploaded_filename = request.FILES['file'].name
                extension = uploaded_filename.split(".")[-1]
                full_filename = os.path.join(photo_path, str(user_id), str(datetime.now().strftime("%Y%m%d-%H%M%S")) +
                                             '.'+extension)

                try:
                    f_out = open(full_filename, 'wb+')
                    file_content = ContentFile(request.FILES['file'].read())
                except IOError:
                    pass

                try:
                    for chunk in file_content.chunks():
                        f_out.write(chunk)
                    f_out.close()
                except EOFError:
                        pass

                image_path = '/static/img/posted_photos/'+str(user_id)+'/'+full_filename[-19:]
                Post.objects.filter(id=post_id).update(set__imagePath=image_path)

            if request.POST['textarea']:
                Post.objects.filter(id=post_id).update(set__posted_text=request.POST['textarea'])

            Post.objects.filter(id=post_id).update(set__post_time=datetime.now(), set__is_edited=True)
        else:
            return HttpResponse("You can't Edit the posts")
        return redirect('/view_all_posts/'+user_id)
    else:
        return render(request, 'session_expired.html')


def post_video(request, user_id):
    """
    :param request: User requesting to upload a video.
    :param user_id: The user is identified by his user_id.
    :return: The posts page will be returned.
    """
    if is_logged_in(request):
        if not os.path.exists(video_path+user_id):
            os.makedirs(video_path+user_id)

        post = Post()
        uploaded_filename = request.FILES['file'].name     # print(request.FILES.keys())
        extension = uploaded_filename.split(".")[-1]
        full_filename = os.path.join(video_path, str(user_id), str(datetime.now().strftime("%Y%m%d-%H%M%S"))+'.'+extension)
        post.post_time = datetime.now()

        try:
            f_out = open(full_filename, 'wb+')
            file_content = ContentFile(request.FILES['file'].read())
        except IOError:
            pass

        try:
            for chunk in file_content.chunks():
                f_out.write(chunk)
            f_out.close()
        except EOFError:
            pass

        post.id_of_posted_user = user_id
        post.name_of_posted_user = User.objects(id=user_id)[0].first_name
        post.videoPath = '/static/videos/posted_videos/'+str(user_id)+'/'+full_filename[-19:]
        post.posted_text = request.POST['textarea']
        post.save()
        user = User.objects(id=user_id)
        User.objects.filter(id=user_id).update(set__no_of_posts=user[0].no_of_posts+1)

        return redirect('/view_all_posts/'+user_id)
    else:
        return render(request, 'session_expired.html')


def edit_video_post(request, user_id, post_id):
    """
    :param request: User requests to update his post.
    :param user_id: The unique id of the user.
    :param post_id: The id of his post.
    :return: Redirects to view all posts.
    """
    if is_logged_in(request):
        post = Post.objects.filter(id=post_id)
        if str(post[0].id_of_posted_user) == str(user_id):
            if request.FILES.keys():
                delete_path = 'D:\\MAJOR PROJECT\\SOCIALAPP\\app_venv1\\SNSAPP\\SocialNetworkingSite'+post[0].videoPath
                os.remove(delete_path)

                uploaded_filename = request.FILES['file'].name
                extension = uploaded_filename.split(".")[-1]
                full_filename = os.path.join(video_path, str(user_id), str(datetime.now().strftime("%Y%m%d-%H%M%S")) +
                                             '.' + extension)

                try:
                    f_out = open(full_filename, 'wb+')
                    file_content = ContentFile(request.FILES['file'].read())
                except IOError:
                    pass

                try:
                    for chunk in file_content.chunks():
                        f_out.write(chunk)
                    f_out.close()
                except EOFError:
                        pass

                new_video_path = '/static/videos/posted_videos/'+str(user_id)+'/'+full_filename[-19:]
                Post.objects.filter(id=post_id).update(set__videoPath=new_video_path)

            if request.POST['textarea']:
                Post.objects.filter(id=post_id).update(set__posted_text=request.POST['textarea'])

            Post.objects.filter(id=post_id).update(set__post_time=datetime.now(), set__is_edited=True)

        else:
            return HttpResponse('You cant edit others post')
        return redirect('/view_all_posts/'+user_id)
    else:
        return render(request, 'session_expired.html')


def post_file(request, user_id):
    """
    :param request: Request from user to post the file.
    :param user_id: User id of the user who is trying to post.
    :return: Redirects to view all the posts that are been posted.
    """
    if is_logged_in(request):
        path_for_files = 'D:\\MAJOR PROJECT\\SOCIALAPP\\app_venv1\\SNSAPP\\SocialNetworkingSite\\static\\other_files\\'
        if not os.path.exists(path_for_files+user_id):
            os.makedirs(path_for_files+user_id)

        post = Post()
        uploaded_filename = request.FILES['file'].name     # print(request.FILES.keys())
        post.file_name = uploaded_filename
        extension = uploaded_filename.split(".")[-1]
        full_filename = os.path.join(path_for_files, str(user_id), uploaded_filename.split(".")[0] +
                                     str(datetime.now().strftime("%Y%m%d-%H%M%S")) + '.' + extension)
        post.post_time = datetime.now()

        try:
            f_out = open(full_filename, 'wb+')
            file_content = ContentFile(request.FILES['file'].read())
        except IOError:
            pass

        try:
            for chunk in file_content.chunks():
                f_out.write(chunk)
            f_out.close()
        except EOFError:
            pass

        post.id_of_posted_user = user_id
        post.name_of_posted_user = User.objects(id=user_id)[0].first_name
        post.uploaded_file_path = '/static/other_files/'+str(user_id)+'/'+full_filename.split("\\")[-1]
        post.posted_text = request.POST['textarea']
        post.save()
        user = User.objects(id=user_id)
        User.objects.filter(id=user_id).update(set__no_of_posts=user[0].no_of_posts+1)

        return redirect('/view_all_posts/'+user_id)
    else:
        return render(request, 'session_expired.html')


def edit_file_post(request, user_id, post_id):
    """
    :param request: Request form the user to edit his file uploaded post.
    :param user_id: User id of the user who is trying to edit it.
    :param post_id: The post id of the Post.
    :return: Redirects to view all posts page.
    """
    if is_logged_in(request):
        post = Post.objects.filter(id=post_id)
        if str(post[0].id_of_posted_user) == str(user_id):
            if request.FILES.keys():
                path_for_files = 'D:\\MAJOR PROJECT\\SOCIALAPP\\app_venv1\\SNSAPP\\SocialNetworkingSite\\static\\'+\
                                 'other_files'
                delete_path = 'D:\\MAJOR PROJECT\\SOCIALAPP\\app_venv1\\SNSAPP\\SocialNetworkingSite'\
                              + post[0].uploaded_file_path
                os.remove(delete_path)

                uploaded_filename = request.FILES['file'].name
                extension = uploaded_filename.split(".")[-1]
                full_filename = os.path.join(path_for_files, str(user_id), uploaded_filename.split(".")[0] +
                                             str(datetime.now().strftime("%Y%m%d-%H%M%S")) + '.' + extension)

                try:
                    f_out = open(full_filename, 'wb+')
                    file_content = ContentFile(request.FILES['file'].read())
                except IOError:
                    pass

                try:
                    for chunk in file_content.chunks():
                        f_out.write(chunk)
                    f_out.close()
                except EOFError:
                        pass

                new_path = '/static/other_files/'+str(user_id)+'/'+full_filename.split("\\")[-1]
                Post.objects.filter(id=post_id).update(set__uploaded_file_path=new_path,
                                                       set__file_name=uploaded_filename)

            if request.POST['textarea']:
                Post.objects.filter(id=post_id).update(set__posted_text=request.POST['textarea'])

            Post.objects.filter(id=post_id).update(set__post_time=datetime.now(), set__is_edited=True)

        else:
            return HttpResponse("You cant edit")

        return redirect('/view_all_posts/'+user_id)

    else:
        return render(request, 'session_expired.html')


def download_file(request, post_id):
    """
    :param request: User request to download a file from the post.
    :param post_id: The id of the post comes in url.
    :return:  Starts download of the file which user selected.
    """
    if is_logged_in(request):
        _path = 'D:\\MAJOR PROJECT\\SOCIALAPP\\app_venv1\\SNSAPP\\SocialNetworkingSite'
        post = Post.objects(id=post_id)
        path_to_file = _path + post[0].uploaded_file_path
        file_name = post[0].file_name
        f_open = open(path_to_file, 'r')
        response = HttpResponse(File(f_open), content_type='*/*')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
        response['X-Sendfile'] = smart_str(path_to_file)
        response['Content-Length'] = os.path.getsize(path_to_file)
        return response
    else:
        return render(request, 'session_expired.html')


"""""""""""""""""""""""""""""""""COMMENT OPERATIONS"""""""""""""""""""""""""""""""""""


def delete_comment(request, user_id, post_id, comment_id):
    """
    :param request: User requesting to Delete the comment.
    :param user_id: User id by which user is uniquely identified.
    :param post_id: The id of the post to which current comment belong to.
    :param comment_id: The id of comment, which need to be deleted.
    """
    if is_logged_in(request):
        post = Post.objects(id=post_id)
        for comment in post[0].comments:
            if str(comment_id) == str(comment.id):
                if str(user_id) == str(comment.posted_user_id):
                    Post.objects.filter(id=post_id).update_one(pull__comments={"id": ObjectId(comment_id)})
                    return redirect('/view_all_posts/' + user_id)
                else:
                    return HttpResponse("You Cant Delete Others Comment")
    else:
        return render(request, 'session_expired.html')

    return HttpResponse("Invalid comment")


class Comments(View):

        def get(self, request,  *args, **kwargs):
            pass

        def post(self, request, *args, **kwargs):
            if is_logged_in(request):
                user_id = kwargs['user_id']
                post_id = kwargs['post_id']
                post = Post.objects.filter(id=post_id).first()
                _comment = Comment()
                _comment.time = datetime.now()
                _comment.content = request.POST['textarea']
                _comment.name = User.objects.filter(id=user_id)[0].first_name
                _comment.posted_user_id = user_id
                post.comments.append(_comment)
                post.save()
                return redirect('/view_all_posts/' + user_id)
            else:
                return render(request, 'session_expired.html')


"""""""""""""""""""""""""""""""""""""NOTIFICATIONS SECTION"""""""""""""""""""""""""""""""


class Notify(View):

        def get(self, request, *args, **kwargs):
            if is_logged_in(request):
                user_id = kwargs['user_id']
                list_of_notifications = []
                user = User.objects.filter(id=user_id).first()

                for notifications in user.notifications:
                    notif = Notifications()
                    notif.name = User.objects(id=notifications.id)[0].first_name
                    notif.id = notifications.id
                    notif.time = notifications.time
                    notif.status = notifications.status
                    list_of_notifications.append(notif)

                context = {
                     "id": user_id,
                     "notifications": list_of_notifications
                }

                return render(request, 'Notifications.html', context)
            else:
                return render(request, 'session_expired.html')

        def post(self, request, *args, **kwargs):
            pass


def accept_friend_request(request, friend_id, user_id):
    """
    :param request: Request from the use to accept friends request.
    :param friend_id: The id of friend that user want to accept.
    :param user_id: The user id of user trying to accept friends request.
    :return: Returns json object to the ajax call.
    """
    if is_logged_in(request):
        User.objects.filter(id=user_id, notifications__id=ObjectId(friend_id)).update(set__notifications__S__status=10)
        User.objects.filter(id=friend_id, notifications__id=ObjectId(user_id)).update(set__notifications__S__status=5)

        user = User.objects(id=user_id).first()
        user.friends.append(ObjectId(friend_id))
        user.save()

        friend = User.objects(id=friend_id).first()
        friend.friends.append(ObjectId(user_id))
        friend.save()

        return JsonResponse({"msg": "success"})
    else:
        return render(request, 'session_expired.html')


def post_friend_requests(request, friend_id, user_id):
    """
    :param request: User requests to send a request to his friends.
    :param friend_id:  The id of his friend.
    :param user_id: The id of the current user.
    :return: Returns a json object as Request sent.
    """
    if is_logged_in(request):

        friend = User.objects(id=friend_id).first()
        notification = Notifications()
        notification.status = 1
        notification.id = user_id
        notification.time = datetime.now()
        friend.notifications.append(notification)
        friend.save()

        user = User.objects(id=user_id).first()
        user_notification = Notifications()
        user_notification.status = 2
        user_notification.id = friend_id
        user_notification.time = datetime.now()
        user.notifications.append(user_notification)
        user.save()
        return JsonResponse({"stat": "Request Sent"})
    else:
        return render(request, 'session_expired.html')


def get_all_users(request, user_id):
    """
    :param request: User requesting to find friends.
    :param user_id: The user id of the user.
    :returns: Returns the view that shows the list of users.
    """
    if is_logged_in(request):
        user = User.objects(id=user_id).first()
        list_of_ids = []
        my_list = []

        for record in user.notifications:
            if record.status not in [5, 10]:
                list_of_ids.append(record.id)

        for friend in user.friends:
            my_list.append(friend)

        others = User.objects(id__nin=list_of_ids+my_list, id__ne=user_id)
        already_sent_request_to = User.objects(id__in=list_of_ids)

        context = {
            "id": user_id,
            "already_sent_request_to": already_sent_request_to,
            "others": others,
        }

        return render(request, 'users.html', context)
    else:
        return render(request, 'session_expired.html')


"""""""""""""""""""""""""""""""""""""""""CHAT APPLICATION"""""""""""""""""""""""""""""""""""


def get_chat_friends(request, user_id):
    """
    :param request: Request by user trying to find the chat friends.
    :param user_id: The id of the user.
    :return: Return a template showing the  list of friends.
    """
    if is_logged_in(request):
        user = User.objects(id=user_id).first()
        friends_list = []
        for friend in user.friends:
            user = User.objects(id=friend).first()
            records = {
                "id": friend,
                "name": user.first_name,
            }
            friends_list.append(records)

        context = {
            "id": user_id,
            "friends": friends_list,
        }

        return render(request, 'chat_friends.html', context)
    else:
        return render(request, 'session_expired.html')


def get_chat(request, user_id, friend_id):
    """
    :param request: Request from user to open chat panel of his friend.
    :param user_id:  The user id of the user.
    :param friend_id:  Friend id to whom the user want to chat.
    :return: Render a template with which user interacts with his friend.
    """
    if is_logged_in(request):
        user = User.objects(id=user_id, chat__friends_id=ObjectId(friend_id))
        friend_name = User.objects(id=friend_id)[0].first_name
        list_of_messages = []

        try:
            for chat in user[0].chat:
                if chat.friends_id == ObjectId(friend_id):
                    list_of_messages.append(chat)
        except IndexError:
            pass

        context = {
            "chat": list_of_messages,
            "id": user_id,
            "friend_id": friend_id,
            "friend_name": friend_name,
        }

        return render(request, 'chat_home.html', context)
    else:
        return render(request, 'session_expired.html')


@csrf_exempt
def post_chat(request, user_id, friend_id):
    """
    :param request: The users request to post a chat message to his friend.
    :param user_id: The user id of the user.
    :param friend_id: The id of the users friend to which user is in chat.
    :return: We return the Json response of message to the ajax call.
    """
    if is_logged_in(request):
            data = json.loads(request.body.decode('utf-8'))
            msg = data['msg_box']

            me = User.objects(id=user_id).first()
            c1 = Chat()
            c1.id = bson.objectid.ObjectId()
            c1.time = datetime.now()
            c1.friends_id = friend_id
            c1.message = msg
            c1.posted_by = 0
            me.chat.append(c1)
            me.save()

            friend = User.objects(id=friend_id).first()
            c2 = Chat()
            c2.id = bson.objectid.ObjectId()
            c2.time = c1.time
            c2.friends_id = user_id
            c2.message = msg
            c2.posted_by = 1
            friend.chat.append(c2)
            friend.save()

            return JsonResponse({"msg": msg})
    else:
        return render(request, 'session_expired.html')


def message(request, user_id, friend_id):
    """
    :param request: User requesting to get all messages.
    :param user_id: The id of the user to be identified with.
    :param friend_id: Id of the friend to which user is in chat with.
    :return: Sends back all messages.
    """
    if is_logged_in(request):
        user = User.objects(id=user_id, chat__friends_id=ObjectId(friend_id))
        list_of_messages = []

        try:
            for chat in user[0].chat:
                if chat.friends_id == ObjectId(friend_id):
                    list_of_messages.append(chat)
        except IndexError:
            pass

        return render(request, 'messages.html', {'chat': list_of_messages, "id": user_id})

    else:
        return render(request, 'session_expired.html')


def delete_msg(request, user_id, friend_id, msg_id):
    """
    :param request:  User requesting to delete his message.
    :param user_id: User id of the user.
    :param friend_id: Id of the friend.
    :param msg_id: Id of the message.
    :return : Redirect to the view which displays the chat messages.
    """
    if is_logged_in(request):
        User.objects.filter(id=user_id).update_one(pull__chat={"id": ObjectId(msg_id)})
        if request.is_ajax():
            return JsonResponse({"msg": "Deleted Successfully"})
        else:
            return redirect('/chat_box/' + user_id + '/' + friend_id)
    else:
        return render(request, 'session_expired.html')


"""""""""""""""""""""""""""""""""""""""""FIND FRIENDS"""""""""""""""""""""""""""""""""""


def search(request):
    if is_logged_in(request):
        pass
    else:
        return render(request, 'session_expired.html')


"""""""""""""""""""""""""""""""""""""""""""""""""""
HELPER FUNCTIONS SECTION, USED BY THE ABOVE VIEWS
"""""""""""""""""""""""""""""""""""""""""""""""""""


def is_logged_in(request):
    """
    :param request: This is the helper function to check if a user's session expired or not.
    :return: Return True if the user's session is not expired else return false.
    """
    try:
        if request.session['member_id']:
            return True
    except KeyError:
        return False
