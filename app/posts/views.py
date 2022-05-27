from json import JSONDecodeError
import logging
from os import abort
from flask import Blueprint, render_template, request
from app.posts.dao.posts_dao import PostsDAO
from app.posts.dao.comments_dao import CommentsDao

posts_blueprint = Blueprint("posts_blueprint",__name__,template_folder="templates")
posts_dao = PostsDAO("data/posts.json")
comments_dao = CommentsDao("data/comments.json")

logger = logging.getLogger ("basic")


@posts_blueprint.route("/")
def posts_all ():
    logger.debug ("Запрошены все посты")
    try:
        posts = posts_dao.get_all()
        return render_template("index.html", posts = posts)
    except:
        return "что то пошло не так"


@posts_blueprint.route("/post/<int:post_pk>")
def posts_one (post_pk):
    logger.debug ("Запрошен пост {post_pk}")
    try:
        post = posts_dao.get_by_pk(post_pk)
        comments = comments_dao.get_by_post_pk(post_pk)
    except JSONDecodeError as error:
        return render_template("error.html", error= error)
    else:
        if post is None:
            abort(404)
        namber_of_comments = len(comments)
        text_len= len(post["content"])
        return render_template("post.html", post=post, comments=comments, namber_of_comments=namber_of_comments, text_len=text_len )


@posts_blueprint.route("/search")
def posts_search ():
    logging.info ("Обработка поискового запроса")
    query = request.args.get("query", "")
    try:
        posts=posts_dao.search(query) 
    except:
        logging.error("Проблема с открытием файла")
        return "Проблема с открытием файла"
    return render_template("search.html", posts=posts, search=query)
    

@posts_blueprint.route("/users/<username>")
def posts_by_user (username):

    posts = posts_dao.get_by_user(username)
   

    return render_template ("user-feed.html", posts=posts)


@posts_blueprint.errorhandler(404)
def post_error(error):
    return "Тайкой пост не найден"