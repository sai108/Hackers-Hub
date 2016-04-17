from mongoengine import *
from mongoengine.fields import *
from djangotoolbox.fields import *
from django.contrib.sessions.models import Session
from bson.objectid import ObjectId
# Create your models here.


class Notifications(EmbeddedDocument):

        status = IntField()
        id = ObjectIdField(required=True)
        time = DateTimeField()


class Chat(EmbeddedDocument):

        id = ObjectIdField(required=True)
        posted_by = IntField()    # 0- Message posted by User, 1- Message posted by Friend
        message = StringField(max_length=1000)
        time = DateTimeField()
        friends_id = ObjectIdField()


class User(Document):

        id = ObjectIdField()
        first_name = StringField(max_length=100, required=True)
        sur_name = StringField(max_length=100, required=True)
        email = EmailField(required=True)
        password = StringField(max_length=100, required=True)
        phone_number = IntField(required=True)
        birthday = StringField(required=True)
        gender = StringField(required=True)
        last_logged_out_time = DateTimeField(default=None)
        account_created_time = DateTimeField(required=True)
        no_of_posts = IntField(default=0)
        friends = SortedListField(ObjectIdField())   # to store id's of all friends.
        chat = SortedListField(EmbeddedDocumentField(Chat), ordering="time")
        notifications = SortedListField(EmbeddedDocumentField(Notifications), ordering='time')


class Comment(EmbeddedDocument):

        id = ObjectIdField(required=True, default=lambda: ObjectId())
        content = StringField()
        posted_user_id = ObjectIdField()
        likes = IntField(default=0)
        name = StringField(max_length=100)
        time = DateTimeField()


class Post(Document):

        id = ObjectIdField()
        id_of_posted_user = ObjectIdField()
        name_of_posted_user = StringField(max_length=100, required=True)
        imagePath = StringField(default=None)
        videoPath = StringField(default=None)
        uploaded_file_path = StringField(default=None)
        file_name = StringField(default=None)
        posted_text = StringField(default=None)
        post_time = DateTimeField(default=None)
        is_edited = BooleanField(default=False)
        likes = IntField(default=0)
        comments = SortedListField(EmbeddedDocumentField(Comment), ordering="time")
