from django.test import TestCase

# Create your tests here.
import itsdangerous
from django.conf import settings

salt=settings.SECRET_KEY#加盐，指定一个盐值，别让别人知道哦，否则就可以解密出来了
t=itsdangerous.TimedJSONWebSignatureSerializer(salt,expires_in=3600)#过期时间600秒

# ==============如何加密==================
res=t.dumps({'confirm':2})# 在t中加入传输的数据
token=res.decode()#指定编码格式
print(token)

# ======================加密的数据如何解析=================
res=t.loads(token)
print(res)
