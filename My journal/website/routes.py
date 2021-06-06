from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import *
from . import db

routes = Blueprint(__name__, 'routes')


def get_liked_posts():
    posts = Like.query.filter_by(user_id=current_user.id).all()
    ret = []
    for post in posts:
        ret.append(Note.query.filter_by(id=post.post_id).first())
    return ret

def get_saved_posts():
    posts = Save.query.filter_by(user_id=current_user.id).all()
    ret = []
    for post in posts:
        ret.append(Note.query.filter_by(id=post.post_id).first())
    return ret

def get_posts_from_folowing(user):
    follows = Follow.query.filter_by(follower=user.username).all()
    notes = []
    for follow in follows:
        user = User.query.filter_by(username=follow.unfollower).first()
        for note in user.get_notes():
            notes.append(note)
    ids = []
    for note in notes:
        ids.append(note.id)
    notes = []    
    for i in ids:
        notes.append(Note.query.filter_by(id=i).first())
    return notes

def clean(note):
    code = []
    final = []
    for i in note.split('\n'):
        code.append(f'{i}<br>')
    for i in code:
        final.append(i.replace('\r', ""))
    return ("".join(final))


@routes.route('/')
@login_required
def home():
    notes = get_posts_from_folowing(current_user)
    return render_template('home.html', user=current_user, notes=notes)

@routes.route('/notifications')
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).all()
    return render_template('notifications.html', user=current_user, notifications=notifications)


@routes.route('/new-note', methods=['GET', 'POST'])
@login_required
def new_note():
    if request.method == 'POST':
        note = (request.form.get('note'))
        title = request.form.get('title')
        tags = request.form.get('tags')

        code = clean(note)

        new = Note(code=code, name=title, tags=tags,
                   user_id=current_user.id, user_name=current_user.username)
        db.session.add(new)
        db.session.commit()

    return render_template('new-note.html', user=current_user)


@routes.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        bio = request.form.get('bio')
        add = clean(bio)

        user = User.query.filter_by(username=current_user.username).first()
        user.bio = add
        db.session.commit()
        return redirect(url_for('website.routes.profile'))

    return render_template('profile.html', user=current_user)


@routes.route('/explore')
def explore():
    return render_template('explore.html', liked = get_liked_posts(), save=get_saved_posts())

@routes.route('/profile/notes')
@login_required
def profile_notes():
    return render_template('profile-notes.html', user=current_user)


@routes.route('/note/<id>/', methods=['GET', 'POST'])
@login_required
def note(id):
    note = (Note.query.filter_by(id=id).first())
    comments = Comment.query.filter_by(post_id=id).all()
    like = 'F'
    save = 'F'

    f = Like.query.filter_by(post_id=id, user_id=current_user.id).first()
    l = Save.query.filter_by(post_id=id, user_id=current_user.id).first()

    if f:
        like = 'T'
    if l:
        save = 'T'
    if request.method == 'POST':

        comment = request.form.get('comment')

        new = Comment(comment=comment, post_id=id,
                      user_name=current_user.username)
        db.session.add(new)
        db.session.commit()

        new_notification = Notification(
            user_id=note.user_id, message=f'{current_user.username} commented "{comment}" at your note, "{note.name}"')
        db.session.add(new_notification)
        db.session.commit()

    return render_template('note.html', user=current_user, note=note, comments=comments, like=like, save=save)

@routes.route('/note/<id>/like')
@login_required
def like(id):
    note = Note.query.filter_by(id=id).first()
    f = Like.query.filter_by(post_id=id, user_id=current_user.id).first()
    if not f:
        new = Like(post_id=id, user_id=current_user.id)
        db.session.add(new)
        db.session.commit()

        new_notification = Notification(
            user_id=note.user_id, message=f'{current_user.username} liked your note, "{note.name}"')
        db.session.add(new_notification)
        db.session.commit()

    else:
        new = Like.query.filter_by(post_id=id, user_id=current_user.id).first()
        db.session.delete(new)
        db.session.commit()
    
    return redirect(url_for('website.routes.note', id=id))

@routes.route('/note/<id>/save')
@login_required
def save( id):
    note = Note.query.filter_by(id=id).first()
    l = Save.query.filter_by(post_id=id, user_id=current_user.id).first()
    if not l:
        new = Save(post_id=id, user_id=current_user.id)
        db.session.add(new)
        db.session.commit()

        new_notification = Notification(
            user_id=note.user_id, message=f'{current_user.username} saved your note, "{note.name}"')
        db.session.add(new_notification)
        db.session.commit()

    else:
        new = Save.query.filter_by(post_id=id, user_id=current_user.id).first()
        db.session.delete(new)
        db.session.commit()
    
    return redirect(url_for('website.routes.note', id=id))

@routes.route('profile/<username>', methods=['GET','POST'])
def person(username):
    user = User.query.filter_by(username=username).first()
    follow = Follow.query.filter_by(follower=current_user.username, unfollower=user.username).first()
    if request.method == 'POST':
        if follow:
            db.session.delete(follow)
            db.session.commit()
        else:
            new = Follow(follower=current_user.username, unfollower=user.username)
            db.session.add(new)
            db.session.commit()
        return redirect(url_for('website.routes.person', username=user.username))

    f='F'
    if follow:
        f = 'T'

    return render_template('person.html', user=current_user, profile=user, follow=f)