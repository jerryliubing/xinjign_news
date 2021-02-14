from .CCPRestSDK import REST

# 主帐号
accountSid = '8a216da864f9f15b01650a6f33bb0bc8'

# 主帐号Token
accountToken = 'b3f4b22a07e24489a17117b2dcce2c94'

# 应用Id
appId = '8a216da864f9f15b01650a6f34190bcf'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'

# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为列表 例如：[验证码，以分为单位的有效时间]
# @param $tempId 模板Id


def sendTemplateSMS(to, datas, tempId):

    # 初始化REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    return result.get('statusCode')