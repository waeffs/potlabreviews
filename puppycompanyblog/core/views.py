from flask import render_template,request,Blueprint
from puppycompanyblog.models import BlogPost

core = Blueprint('core',__name__)

@core.route('/')
def index():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=8)
    latest_posts =BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)
    top_posts =BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)
    return render_template('index.html',blog_posts=blog_posts, latest_posts=latest_posts, top_posts=top_posts)


@core.route('/info')
def info():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    return render_template('info.html')

@core.route('/car_parts')
def politics():

    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.filter_by(category='politics').order_by(BlogPost.date.desc()).paginate(page=page, per_page=8)
    latest_posts =BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)
    top_posts =BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)
    return render_template('politics.html',blog_posts=blog_posts, latest_posts=latest_posts, top_posts=top_posts)

@core.route('/electronics')
def lifestyle():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.filter_by(category='lifestyle').order_by(BlogPost.date.desc()).paginate(page=page, per_page=8)
    latest_posts =BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)
    top_posts =BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)
    return render_template('lifestyle.html',blog_posts=blog_posts, latest_posts=latest_posts, top_posts=top_posts)

@core.route('/smartphones')
def business():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.filter_by(category = 'business').order_by(BlogPost.date.desc()).paginate(page=page, per_page=8)
    latest_posts =BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)
    top_posts =BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)
    return render_template('business.html',blog_posts=blog_posts, latest_posts=latest_posts, top_posts=top_posts)

@core.route('/computers')
def sports():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.filter_by(category = 'sports').order_by(BlogPost.date.desc()).paginate(page=page, per_page=8)
    latest_posts =BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)
    top_posts =BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)
    return render_template('sports.html',blog_posts=blog_posts, latest_posts=latest_posts, top_posts=top_posts)

@core.route('/player')
def player():
    contentid=""
    return render_template('player.html')
