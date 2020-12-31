from django.db import models


class Users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    user_id = models.ForeignKey(Users, related_name="messages", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user_id = models.ForeignKey(Users, related_name="user_comments", on_delete=models.CASCADE)
    messege_id = models.ForeignKey(Message, related_name="message_comments", on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def insert_new_user(first_name, last_name, email, password):
    user = Users.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)
    return user


def is_duplicate_email(email):
    users = Users.objects.filter(email=email).values()
    if len(users):
        return True
    return False


def get_user(email, passwd):
    users = Users.objects.filter(email=email, password=passwd)
    if not len(users):
        return None
    return users[0]


def get_all_mesgs():
    all_mesgs = Message.objects.all().order_by("created_at")
    return all_mesgs


def insert_mesg(user_id, body):
    user = Users.objects.get(id=user_id)
    mesg = Message.objects.create(user_id=user, message=body)
    return mesg


def get_comments(mesg_id):
    mesg = Message.objects.get(id=mesg_id)
    comments = Comment.objects.filter(messege_id=mesg).order_by("created_at")
    return comments


def insert_comment(user_id, body, mesg_id):
    mesg = Message.objects.get(id=mesg_id)
    user = Users.objects.get(id=user_id)
    comment = Comment.objects.create(user_id=user, messege_id=mesg, comment=body)
    return comment