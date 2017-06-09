import requests
import hmac
import hashlib
import mod_config

# appKey和签名串

appKey = mod_config.getConfig("aliexpressAPI", "appKey")
appSercet = mod_config.getConfig("aliexpressAPI", "appSercet")

data = 'client_id{}redirect_uriurn:ietf:wg:oauth:2.0:oobsitealiexpress'.format(
    appKey)
# 转成bytes形式
data = data.encode(encoding='utf-8')
Token = appSercet.encode(encoding='utf-8')

# 构建签名
Signature = hmac.new(Token, data, hashlib.sha1).hexdigest().upper()
print(Signature)

# 参数
params = {
    'client_id': appKey,
    'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
    'site': 'aliexpress',
    '_aop_signature': Signature
}


api = 'http://authhz.alibaba.com/auth/authorize.htm'
re = requests.get(api, params=params)
print(re.headers)
print(re.text)
print(re.status_code)
