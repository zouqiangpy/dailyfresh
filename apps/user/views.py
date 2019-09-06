from django.shortcuts import render,redirect,reverse
from .models import User
from django.views.generic import View
import re
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.
def login(request):
    '''用户登录处理'''
    if request.method == 'GET':
        #显示登录页面
        return render(request,'login.html')
    else:
        #用户登录业务处理
        username = request.POST['username']
        password = request.POST['pwd']
        user = User.objects.get(username=username)
        if user:
            if password == user.password:
                #用户登录成功
                return redirect(reverse('goods:index'))
            else:
                #密码错误
                return render(request,'login.html',{'user': user})
        else:
            return render(request, 'login.html', )

class RegisterView(View):

    '''注册视图类'''

    def get(self, request):

        '''显示注册页面'''

        return render(request,'register.html')

    def post(self, request):

        '''注册处理'''

        username = request.POST['user_name']
        password = request.POST['pwd']
        email = request.POST['email']
        allow = request.POST['allow']
        # 数据校验

        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        if not re.match('^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            # 不是合法邮箱
            return render(request, 'register.html', {'errmsg': '不是合法邮箱'})
        if allow != 'on':
            # 没有同意协议
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})
        user = User.objects.create(username=username, password=password, email=email)
        user.is_active = 0
        user.save()
        #发送激活邮件
        #1.激活链接,用户id加密
        serializer = Serializer(settings.SECRET_KEY,3600)
        token = serializer.dumps({'confirm': user.id}).decode()
        #2.发邮件
        subject = '天天生鲜欢迎信息'
        message = '邮件正文'
        sender = settings.EMAIL_FROM
        reciver = ['513123423@qq.com']
        send_mail(subject,message,sender,reciver,html_message='http://127.0.0.1:8000/user/active/%s' %token)

        return redirect(reverse('goods:index'))


class ActiveView(View):
    '''用户邮箱激活处理'''
    def get(self, request,id):
        serializer = Serializer(settings.SECRET_KEY,3600)
        try:
            user_id = serializer.loads(id)
            user_id = user_id['confirm']
            user = User.objects.get(id = user_id)
            user.is_active = 1
            user.save()
            return redirect(reverse('user:login'))
        except SignatureExpired:
            return HttpResponse('激活链接已过期')



