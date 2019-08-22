from flask import Blueprint, render_template, session, make_response
from utils.captcha.captcha import captcha

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
