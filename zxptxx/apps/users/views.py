# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from users.models import UserProfile,EmailVerifRecord
from django.views.generic import View
from django.contrib.auth.hashers import make_password
# 并集查询
from django.db.models import Q
# Create your views here.


from .forms import LoginForm,RegisterForm,ForgetpwdForm,ReserPwdForm
from utils.email_send import send_register_email


# 继承ModelBackend类，因为它有方法authenticate，可点进源码查看
# 重写验证用户密码的函数，使得可以使用邮箱登录
class CustomBackend(ModelBackend):
    #重载authenticate方法
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


#激活的逻辑
class ActiveUserView(View):
    def get(self,request,active_code):
        #查询邮箱验证是否存在记录
        all_record = EmailVerifRecord.objects.filter(code = active_code)
        if all_record:
            for record in all_record:
                #获取对应的邮箱
                email = record.email
                #查找邮箱对应的User
                user = UserProfile.objects.get(email = email)
                user.is_active = True
                user.save()
                return render(request, "login.html")
        else:
            return render(request, "register.html", {"msg": "您的激活链接无效"})


#注册的逻辑
class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email","")
            pass_word = request.POST.get("password","")

            #判断否是相同邮箱
            email = UserProfile.objects.filter(email=user_name)
            if email:
                return render(request, "register.html", {'msg': "邮箱已被注册"})
            else:
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.is_active = False
                # 加密password进行保存
                user_profile.password = make_password(pass_word)
                user_profile.save()


                send_register_email(user_name,"register")

                return render(request, "login.html")
        else:
            return render(request, "register.html", {'register_form': register_form})



#继承了django的View类
class LoginView(View):
    def get(self,request):
        return render(request, 'login.html', {})
    def post(self,request):
        #创建表单对象，参数是request.POST
        login_form = LoginForm(request.POST)

        #验证表单合法性，验证成功返回Ture，否则Flase
        if login_form.is_valid():
            if request.method == 'POST':
                user_name = request.POST.get('username', "")
                password = request.POST.get("password", "")

                # 验证用户是否匹配，匹配成功返回user对象，否则为空
                user = authenticate(username=user_name, password=password)
                if user is not None:

                    if user.is_active:
                        login(request, user)
                        return render(request, 'index.html')
                    else:
                        return render(request, 'login.html',{"msg": "用户未激活"})

                else:
                    return render(request, 'login.html', {"msg": "用户或密码错误"})
        else:
            return render(request, 'login.html', {"login_form": login_form})


#忘记密码发送邮箱逻辑
class ForgetPwdView(View):
    def get(self,request):
        forege_pwd_form = ForgetpwdForm()
        return render(request,'forgetpwd.html',{'forege_pwd_form':forege_pwd_form})
    def post(self,request):
        forege_pwd_form = ForgetpwdForm(request.POST)
        if forege_pwd_form.is_valid():
            email = request.POST.get("email","")
            send_register_email(email,'forget')
            return render(request, "login.html", {"msg": "重置密码邮件已发送,请注意查收"})
        else:
            return render(request, "forgetpwd.html", {'forege_pwd_form':forege_pwd_form})


#返回重置密码页面逻辑
class ResetView(View):
    def get(self,request,active_code):
        all_record = EmailVerifRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
            return render(request,'password_reset.html',{'email':email})
        else:
            forege_pwd_form = ForgetpwdForm()
            return render(request, "forgetpwd.html", {"msg": "您的链接无效","forege_pwd_form":forege_pwd_form})


#处理重置密码逻辑
class ResetPwdView(View):
    def post(self,request):
        reser_pwd_form = ReserPwdForm(request.POST)
        email = request.POST.get("email", "")
        if reser_pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return render(request,'reset_pwd_msg.html',{email:'email','msg':"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            EmailVerifRecord.objects.filter(email=email).delete()
            return render(request,'login.html',{'msg':'密码设置成功，请登录'})
        else:
            email = request.POST.get("email", "")
            return render(request,'reset_pwd_msg.html',{email:'email','msg':"密码字符不能少于5","reser_pwd_form":reser_pwd_form})


