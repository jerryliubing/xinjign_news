from qiniu import Auth, put_data


def upload(f1):
    access_key = 'WoMYMqbk8od1wnu72AHjF5tAiO7Bk9K6g7jQ3xLU'
    secret_key = 'iqECwe9OY6bXAZQKhdon2yMAtGc5Z5yBuh9A0vk_'
    # 空间名称
    bucket_name = 'jerry-liubing'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 生成上传 Token
    token = q.upload_token(bucket_name)
    # 上传文件数据，ret是字典，键为hash、key，值为新文件名，info是response对象
    ret, info = put_data(token, None, f1.read())

    return ret.get("key")


