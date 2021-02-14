from flask import Blueprint, render_template, session, make_response

news_blueprint = Blueprint("news", __name__)


# 展示新闻主页面
@news_blueprint.route('/')
def index():
    return render_template("news/index.html")














