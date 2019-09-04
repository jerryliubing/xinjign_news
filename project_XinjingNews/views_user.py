import re

from flask import Blueprint, render_template, session, make_response, request, jsonify
from models import UserInfo, db
from utils.captcha.captcha import captcha
from utils.ytx_sdk.ytx_send import sendTemplateSMS
import random

user_blueprint = Blueprint("user", __name__, url_prefix="/user")


# 图片验证码
@user_blueprint.route('/image_code', methods=['GET'])
def image_code():
    # 调用captcha第三方包,生成验证码数据
    name, text, str_val = captcha.generate_captcha()
    print("--------注册图片验证码为: %s" % text)
    # 保存到session中,用于后续对比
    session['image_code'] = text
    # 创建响应对象,响应体为图片数据
    response = make_response(str_val)
    # 设置相应数据的类型为图片
    response.content_type = 'image/png'
    # 返回
    return response


# 短信验证码
@user_blueprint.route('/sms_code')
def sms_code():
    # 接收:手机号,图形验证码
    mobile = request.args.get("mobile")
    img_code = request.args.get("img_code")

    # 验证
    if not all([mobile, img_code]):
        return jsonify(result=1)                    # 1 --> 手机号,图形验证码均不能为空
    session_image_code = session.get("image_code")
    if not session_image_code:
        return jsonify(result=2)
    if img_code != session_image_code:              # 2 --> 请获取短信验证码
        return jsonify(result=3)                    # 3 --> 图形验证码不正确
    # 验证完后强制删除图形验证码,防止用户不断尝试
    del session['image_code']

    # 处理
    # 生成随机6为数字验证码,不够位添零
    str_sms_code = str(random.randint(0, 999999)).zfill(6)
    print("--------注册短信验证码为: %s" % str_sms_code)
    # 保存数字验证码,用于后续验证
    session["sms_code"] = str_sms_code
    # 调用云通讯,发送短信验证码
    # sendTemplateSMS(mobile, [str_sms_code, '10'], 1)  # 功能已实现,控制台打印sms_code方便调试

    # 响应
    return jsonify(result=4)                        # 4 --> 短信验证码发送成功


@user_blueprint.route('/register', methods=["POST"])
def register():
    # 接收:手机号,密码,短信验证码
    mobile = request.form.get("mobile")
    password = request.form.get("password")
    rg_sms_code = request.form.get("smscode")

    # 验证
    # 非空
    if not all([mobile, password, rg_sms_code]):
        return jsonify(result=1)                    # 1 --> 注册信息不全
    # 短信验证码是否存在
    session_sms_code = session.get("sms_code")
    if not session_sms_code:
        return jsonify(result=2)                    # 2 --> 短信验证码错误
    # 强制删除session中的短信验证码,防止用户反复重试
    del session["sms_code"]
    # 对比短信验证码
    if session_sms_code != rg_sms_code:
        return jsonify(result=2)
    # 密码正则匹配
    if not re.match(r'^[a-zA-Z0-9!@$#^&*,.?:-=+_/]{6,20}$', password):
        return jsonify(result=3)                    # 3 --> 密码不合规
    # 手机号是否已注册
    if UserInfo.query.filter_by(mobile=mobile).count() > 0:
        return jsonify(result=4)                    # 4 --> 该手机号已经注册

    # 处理
    user = UserInfo()
    user.mobile = mobile
    user.nick_name = mobile
    # 使用property装饰器,将方法像属性一样使用
    user.password = password
    # 提交数据库
    db.session.add(user)
    db.session.commit()

    # 响应
    return jsonify(result=5)                        # 5 --> 注册成功

















































