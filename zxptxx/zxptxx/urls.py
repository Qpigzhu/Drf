# _*_ encoding:utf-8 _*_
"""zxptxx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin
from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ResetPwdView
from organization.views import OrgView
from settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^$',TemplateView.as_view(template_name="index.html"),name="index"),
    url(r'^login/$',LoginView.as_view(),name="login"),
    url(r'^register/$',RegisterView.as_view(),name="register"),
    url(r"^active/(?P<active_code>.*)/$",ActiveUserView.as_view(),name="active"),
    url(r'^forgent/$', ForgetPwdView.as_view(), name="forgent_pwd"),
    url(r'reset/(?P<active_code>.*)/$',ResetView.as_view(),name='reset_pwd'),
    url(r'resetpwd/',ResetPwdView.as_view(),name='reset_pwd_datil'),

    # 课程机构首页url
    url(r'^org_list/$',OrgView.as_view(),name="org_list"),

    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),
]
