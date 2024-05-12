import markdown
import re
import shutil

from flask import current_app, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
import sqlalchemy as sa

from app import db, turnstile
from app.blog.blogpage import bp
from app.blog.forms import *
from app.models import *
import app.util as util
from app.markdown_ext.myextensions import MyExtensions

import markdown_grid_tables
import re


def get_blog_id(blueprint_name) -> str:
    return blueprint_name.split('.')[-1]


# Markdown tweaks round 2: non-custom-syntax stuff easier from here than from JQuery in round 3, like regex replaces
# Changes:
#   Remove extra <p> tags generated by 3rd-party extension "markdown_grid_tables" that mess up table spacing
def additional_markdown_processing(s) -> str:
    s = s.replace("</center></p>", "</center>") \
            .replace("</pre></p>", "</pre>")
    # using regex to not take chances here with attributes and stuff
    s = re.sub(r"<p><center([\S\s]*?)>", r"<center\1>", s)
    s = re.sub(r"<p><pre([\S\s]*?)>", r"<pre\1>", s)

    return s


@bp.route("/")
def index():
    blog_id = get_blog_id(request.blueprint)
    
    # require login to access private blogs
    if blog_id in current_app.config["PRIVATE_BLOG_IDS"]:
        result = util.custom_unauthorized(request)
        if result:
            return result


    page = request.args.get("page", 1, type=int) # should automatically redirect non-int to page 1
    if page <= 0: # prevent funny query string shenanigans
        return "", 204
    posts = None
    all_posts = False

    if blog_id == current_app.config["ALL_POSTS_BLOG_ID"]:
        all_posts = True
        posts = db.paginate(db.session.query(Post).filter(Post.blog_id \
                .notin_(current_app.config["PRIVATE_BLOG_IDS"])).order_by(sa.desc(Post.timestamp)),
                page=page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False)
    else:
        all_posts = False
        posts = db.paginate(db.session.query(Post).filter_by(blog_id=blog_id).order_by(sa.desc(Post.timestamp)),
                page=page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False)

    if posts is None or (page > posts.pages and posts.pages > 0): # prevent funny query string shenanigans, 2.0
        return "", 204
    next_page_url = url_for(f"blog.{blog_id}.index", page=posts.next_num) if posts.has_next else None
    prev_page_url = url_for(f"blog.{blog_id}.index", page=posts.prev_num) if posts.has_prev else None
    return render_template("blog/blogpage/index.html",
            blog_id=blog_id, unpublished_blog_id=blog_id if blog_id.startswith('-') else "-"+blog_id,
            page=page, total_pages=posts.pages, all_posts=all_posts,
            title=current_app.config["BLOG_ID_TO_TITLE"][blog_id],
            subtitle=current_app.config["BLOG_ID_TO_SUBTITLE"].get(blog_id, ""),
            posts=posts, next_page_url=next_page_url, prev_page_url=prev_page_url,
            get_comment_count=Post.get_comment_count)


@bp.route("/<string:post_sanitized_title>")
def post(post_sanitized_title):
    blog_id = get_blog_id(request.blueprint)

    # require login to access private blogs
    if blog_id in current_app.config["PRIVATE_BLOG_IDS"]:
        result = util.custom_unauthorized(request)
        if result:
            return result

    add_comment_form = AddCommentForm()
    reply_comment_button = ReplyCommentButton()
    delete_comment_button = DeleteCommentButton()
    post = db.session.query(Post).filter(Post.sanitized_title == post_sanitized_title).first()
    if post is None:
        return redirect(url_for(f"{request.blueprint}.index",
                flash=util.encode_URI_component("That post doesn't exist.")))

    extensions = ["extra", "markdown_grid_tables", MyExtensions()]
    post.content = markdown.markdown(post.content, extensions=extensions)
    post.content = additional_markdown_processing(post.content)

    comments_query = post.comments.select().order_by(sa.desc(Comment.timestamp))
    comments = db.session.scalars(comments_query).all()
    for comment in comments:
        comment.content = markdown.markdown(comment.content, extensions=extensions)
        comment.content = additional_markdown_processing(comment.content)

    return render_template("blog/blogpage/post.html",
            blog_id=blog_id, blog_title=current_app.config["BLOG_ID_TO_TITLE"][blog_id],
            post=post, comments=comments, add_comment_form=add_comment_form,
            reply_comment_button = reply_comment_button,
            delete_comment_button = delete_comment_button,
            get_comment_count=Post.get_comment_count,
            get_descendants_list=Comment.get_descendants_list)
