# Interface to sql.py

from flask import escape
from bbs.sql import *
from icecream import ic
from flask_login import current_user, logout_user

def get_all_boards():
    tuples = get_types()
    boards = [{
        'id': b[0],
        'name': b[1]
        }
        for b in tuples
    ]
    return boards

def get_user_by_id(id):
    usr = get_usr_info_by_id(id)
    if not usr:
        return None
    usr['username'] = usr['name']
    usr['password'] = usr['pswd']
    usr['avatar'] = usr['photo_location']
    return usr

def get_userid_by_name(username):
    return get_id_from_name(username)

def add_user(name, password):
    if not register_usr_name_and_pswd(name, password):
        return False
    update_userinfo(usr_name=name, usr_photo_location='avatar/avatar.jpeg', usr_nickname=name)
    return True

def update_userinfo(usr_name, usr_photo_location=None, usr_nickname=None,
    usr_email=None, usr_gender=None, usr_phone_num=None, usr_school=None, usr_age=None):
    update_usr_info(usr_name=usr_name, usr_age=usr_age, usr_email=usr_email,
    usr_gender=usr_gender, usr_nickname=usr_nickname, usr_phone_num=usr_phone_num,
    usr_photo_location=usr_photo_location, usr_school=usr_school)


def get_board_by_bid(bid):
    tuples = get_types()
    boards = [{
        'id': b[0],
        'name': b[1]
        }
        for b in tuples
    ]
    return [b for b in boards if b['id'] == bid][0]

def get_thread_and_comments_by_threadid(threadid):
    tuples = get_full_post_from_post_id(threadid)
    thread = post_tuple_to_dict(tuples[0])
    comments = [post_tuple_to_dict(tuples[i]['content']) for i in range(1, len(tuples))]
    for i, comment in enumerate (comments):
        comment['target_content'] = escape(tuples[i+1]['reference_content'][5])
    return thread, comments

def post_tuple_to_dict(t):
    post = {
        'id': t[0],
        'user_id': t[1],
        'title': escape(t[4]),
        'content': escape(t[5]),
        'comment_id': t[6],
        'bid': t[7],
        'time': t[8],
        'post-count': t[10],
    }
    post['author'] = get_user_by_id(post['user_id'])
    post['like'], post['dislike'] = get_like_numbers(post['id'])
    if current_user.is_authenticated:
        stars = get_stars_from_usr_id(current_user.get_id())
        if stars:
            stars = [star[0] for star in stars]
            if post['id'] in stars:
                post['favorate'] = True
        liked, disliked = get_like(current_user.get_id(), post['id'])
        post['liked_by_user'] = liked
        post['disliked_by_user'] = disliked
    return post

def get_threadlist_by_bid(bid):
    tuples = get_post_from_type(bid)
    threads = [post_tuple_to_dict(t) for t in tuples]
    return threads

def get_threadlist_by_userid(userid):
    tids = get_post_ids_from_id(userid) # [(id,), (id,), ]
    tids = [id[0] for id in tids]
    tids = [id for id in tids if get_reference_id_from_post_id(id) == -1]
    
    threads = [get_post_content_from_post_id(id) for id in tids]
    threads = [post_tuple_to_dict(t) for t in threads]
    return threads

threaddb = {}
def query_top10():
    threads = get_top_ten_posts()
    return [post_tuple_to_dict(t) for t in threads]

def query_recent10():
    threads = get_current_ten_posts()
    return [post_tuple_to_dict(t) for t in threads]

def get_all_threads_comment_num():
    return {tid:value['post-count'] for tid, value in threaddb.items()}

def toggle_like(userid, likes, postid):
    like(userid, likes, postid)

def toggle_favorate(userid, postid):
    star(userid, postid)

def query_favorate(userid):
    postids = get_stars_from_usr_id(userid)
    if not postids:
        return []
    posts = [post_tuple_to_dict(get_post_content_from_post_id(postid[0])) for postid in postids]
    return posts