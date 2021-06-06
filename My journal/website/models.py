from re import template
from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    bio = db.Column(db.String(10000000))
    dp = db.Column(db.String(200000))
    
    def get_notes_num(object):
        return len(Note.query.filter_by(user_id=object.id).all())
    
    def get_notes(object):
        return (Note.query.filter_by(user_id=object.id).all())

    def get_followers_num(object,user):
        return len(Follow.query.filter_by(follower=user).all())

    def get_followers(object,user):
        return (Follow.query.filter_by(follower=user).all())

    def get_following_num(object,user):
        return len(Follow.query.filter_by(unfollower=user).all())

    def get_following(object,user):
        return (Follow.query.filter_by(unfollower=user).all())

    def get_notifications_num(object,user):
        return len(Notification.query.filter_by(user_id=user).all())

    def get_notifications(object,user):
        return (Notification.query.filter_by(user_id=user).all())

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    code = db.Column(db.String(10000000))
    tags = db.Column(db.String(1000))
    
    def get_tags(note):
        return list(str(note.tags).split(','))

    def get_likes_num(object,post):
        return len(Like.query.filter_by(post_id=post).all())

    def get_saves_num(object,post):
        return len(Save.query.filter_by(post_id=post).all())

    def get_comments_num(object,post):
        return len(Comment.query.filter_by(post_id=post).all())

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower = db.Column(db.String(100))
    unfollower = db.Column(db.String(100))

class Save(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    comment = db.Column(db.String(10000))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100))
    user_id = db.Column(db.Integer)

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    template = db.Column(db.Integer)
    text = db.Column(db.String(100))