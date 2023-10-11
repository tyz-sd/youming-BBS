from flask import render_template, request, url_for, redirect, flash, escape, abort
from  bbs import app, db
from bbs.auth import User
from bbs.config import Config
from icecream import ic
from flask_login import current_user, login_required

@app.route('/')
def index():
    if request.method == 'GET':
        boards = db.get_all_boards()
        top10 = db.query_top10()
        recent10 = db.query_recent10()
        return render_template('index.html.jinja', boards=boards, top10 = top10, recent10=recent10)


@app.route('/search', methods = ['POST'])
def search():
    # https://www.bing.com/search?ensearch=1&q=some+site:pku.edu.cn&mkt=zh-CN
    keyword = request.form['search_keyword']
    if not keyword:
        return redirect(url_for('index'))
    domain_name = r'https://www.bing.com/search?ensearch=1&q=' + keyword + '+site:' + Config.domain_name + '&mkt=zh-CN'
    ic(domain_name)
    return redirect(domain_name)

# 版面
@app.route('/thread')
def thread():
    bid = request.args.get('bid', type=int)
    page = request.args.get('page', 1, type=int) - 1

    board = db.get_board_by_bid(bid)
    thread_list = db.get_threadlist_by_bid(bid)
    displayed_threads = thread_list[page * Config.thread_per_page: (page + 1) * Config.thread_per_page]
    if len(displayed_threads) == 0 and page > 0:
        abort(404)
    return render_template('thread.html.jinja', board=board, threads=displayed_threads)


@app.route('/post-read')
def post_read():
    # bid = request.args.get('bid', type=int)
    threadid = request.args.get('threadid', type=int)
    page = request.args.get('page', 1, type=int)
    thread, comments = db.get_thread_and_comments_by_threadid(threadid)
    bid = thread['bid']
    board = db.get_board_by_bid(bid)

    return render_template('post-read.html.jinja', board=board, thread=thread, comments=comments)

@app.route('/top-ten')
def top_ten():
    board = {
        'id': 'top-ten',
        'name': '全站十大'
    }

    threads = db.query_top10()
    return render_template('thread.html.jinja', board=board, threads=threads)

@app.route('/recent-ten')
def recent_ten():
    board = {
        'id': 'recent-ten',
        'name': '最新帖子'
    }

    threads = db.query_recent10()
    return render_template('thread.html.jinja', board=board, threads=threads)

@app.route('/favorate')
@login_required
def favorate():
    board = {
        'id': 'favorate',
        'name': '我的收藏'
    }

    threads = db.query_favorate(current_user.get_id())
    return render_template('thread.html.jinja', board=board, threads=threads)

@app.route('/myinfo')
@login_required
def myinfo():
    posted_threads = db.get_threadlist_by_userid(current_user.get_id())
    return render_template('myinfo.html.jinja', posted_threads=posted_threads)
    
@app.route('/update-myinfo', methods=['post'])
@login_required
def update_myinfo():
    nickname = request.form.get('myname')
    if request.form.get('gender'):
        gender = request.form.get('gender')
    age = request.form.get('age')
    phone = request.form.get('phone')
    email = request.form.get('email')
    school = request.form.get('school')
    db.update_userinfo(usr_name=current_user.username, usr_gender=gender, usr_phone_num=phone,
    usr_nickname=nickname, usr_school=school, usr_age=age,usr_email=email)
    return redirect('myinfo')

@app.route('/update_avatar', methods=['post'])
def update_avatar():
    avatar = request.files.get('newAvatar')
    if not avatar:
        return redirect('myinfo')
    ext_name = avatar.filename[avatar.filename.rfind('.'):]
    location = 'bbs/static/avatar/'+current_user.username + ext_name
    avatar.save(location)
    db.update_userinfo(usr_name=current_user.username, usr_photo_location='avatar/' + current_user.username + ext_name)
    return redirect('myinfo')

@app.route('/add_thread', methods=['post'])
@login_required
def add_thread():
    bid = request.form.get('bid')
    topic = request.form.get('topic')
    content = request.form.get('content')
    userid = current_user.get_id()

    if not topic:
        return redirect(url_for('thread', bid=bid))

    db.add_new_post(userid, topic, content, bid)
    return redirect(url_for('thread', bid=bid))

@app.route('/add_comment', methods=['post'])
@login_required
def add_comment():
    bid = request.form.get('bid')
    threadid = request.form.get('threadid')
    content = request.form.get('content')
    userid = current_user.get_id()
    reference_id = request.form.get('reference_id')

    if not content:
        return redirect(url_for('post_read', bid=bid, threadid=threadid))

    db.add_new_comment(threadid, userid, content, reference_id)
    return redirect(url_for('post_read', bid=bid, threadid=threadid))

@app.route('/like')
@login_required
def like():
    bid = request.args.get('bid')
    threadid = request.args.get('threadid')
    postid = request.args.get('postid')
    like = int(request.args.get('like'))

    db.toggle_like(current_user.get_id(), like, postid)
    return redirect(url_for('post_read', bid=bid, threadid=threadid))

@app.route('/add_favorate')
@login_required
def add_favorate():
    bid = request.args.get('bid')
    threadid = request.args.get('threadid')

    db.toggle_favorate(current_user.get_id(), threadid)
    return redirect(url_for('post_read', bid=bid, threadid=threadid))