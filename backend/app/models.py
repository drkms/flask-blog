#!/usr/bin/env python3.4
import datetime

import pytz
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(db.Model):
    """
    The user class is the basic user class with username, mail, a password.

    It has a foreign key for posts (one-to-many)

    User:
    =====
    id: primary key
    username: Str, 30, unique, index
    email: Str, 60, unique, index
    password: Str, 120 *The pass is hashed and can not be accessed directly
    is_admin: Bool
    posts: the query object for posts
    permissions: TODO
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True, index=True)
    email = db.Column(db.String(50), nullable=True, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    @property
    def password(self):
        """
        Prevents direct access to the password.
        """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
        Creates the password hash using Werkzeug's security features.
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Compares the entered password with the hash.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        Representation of a single User instance.
        """
        return '<User {0}, is admin {1}">'.format(self.username, self.is_admin)


class Post(db.Model):
    """
    A single blog entry.

    It has a many-to-one relation with User ('author') and

    Post:
    =====
    id: primary key
    title: Str, 120, unique, index
    summary: Text * The first paragraph of a post and the preview of the post
    body: Text
    created: default now
    modified: now on change
    pub_date: Date, nullable
    username: Int, foreign key
    slug: Str
    """
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, index=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now())
    modified = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    pub_date = db.Column(db.DateTime, nullable=True)
    summary = db.Column(db.Text, nullable=False, index=True)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    slug = db.Column(db.String(120))

    def is_visible(self):
        """
        Checks if a post has a pub_date.
        """
        return bool(self.pub_date) and self.pub_date <= datetime.datetime.now()

    def __repr__(self):
        """
        The representation for a  post.
        """
        return '<Entry for: {0}>'.format(self.title)


class Page(db.Model):
    """
    The pages class lets you add and edit static pages, like links and about me.

    The Pages class is the database model for pages.

    Page:
    ====
    id: primary key
    title: Str, 120, unique, index
    text: Text
    created: default now
    modified: now on change
    """
    __tablename__ = 'Pages'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now())
    modified = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """
        The representation of a page instance.
        """
        return '<{0}>'.format(self.title)
