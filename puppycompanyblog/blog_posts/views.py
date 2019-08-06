from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from puppycompanyblog import db
from puppycompanyblog.models import BlogPost
from puppycompanyblog.blog_posts.forms import BlogPostForm
from puppycompanyblog.blog_posts.blogimagehandler import add_blog_pic, create_thumbnail

blog_posts = Blueprint('blog_posts',__name__)

@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        if form.blog_image.data:

            pic = add_blog_pic(form.blog_image.data)
            pic_thumbnail = create_thumbnail(form.blog_image.data)
            BlogPost.blog_image = pic

            blog_post = BlogPost(title=form.title.data,
                                 text=form.text.data,
                                 category = form.category.data,
                                 user_id=current_user.id,
                                 blog_image=pic,
                                 blog_thumbnail = pic_thumbnail
                                 )
        else:
            blog_post = BlogPost(title=form.title.data,
                                 text=form.text.data,
                                 category = form.category.data,
                                 user_id=current_user.id,
                                  blog_image='c1.jpg',
                                  blog_thumbnail = 'stories1.jpg'
                                 )

        db.session.add(blog_post)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for('core.index'))

    return render_template('create_post.html',form=form)


# int: makes sure that the blog_post_id gets passed as in integer
# instead of a string so we can look it up later.
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    # grab the requested blog post by id number or return 404
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=8)
    latest_posts =BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)
    top_posts =BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)


    return render_template('readblog.html',title=blog_post.title,
                            date=blog_post.date,post=blog_post, blog_posts=blog_posts, latest_posts=latest_posts, top_posts=top_posts
    )

@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    return render_template('create_post.html', title='Update',
                           form=form)


@blog_posts.route("/<int:blog_post_id>/delete", methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))
