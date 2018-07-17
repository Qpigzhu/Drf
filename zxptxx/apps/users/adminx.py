# _*_ encoding:utf-8 _*_
__author__ = 'pig'
__data__ = '2018\7\15 0015 20:48'

import xadmin
from xadmin import views

from .models import EmailVerifRecord,Banner



class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True


# x admin 全局配置参数信息设置
class GlobalSettings(object):
    site_title = "慕课后台管理"
    site_footer = "慕课网"
    #收起菜单
    menu_style = "accordion"


# 创建admin的管理类,这里不再是继承admin，而是继承object
class EmailVerifRecordAdmin(object):
    #后台显示的列
    list_display = ['code', 'email','send_type', 'send_time']
    #搜索字段(时间搜索会报错，所以去掉时间字段)
    search_fields = ['code', 'email','send_type']
    # 配置筛选字段
    list_filter = ['code', 'email', 'send_type', 'send_time']

xadmin.site.register(EmailVerifRecord,EmailVerifRecordAdmin)


class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']

xadmin.site.register(Banner,BannerAdmin)
# 将开启主题功能注册
xadmin.site.register(views.BaseAdminView,BaseSetting)
# 将头部与脚部信息进行注册:
xadmin.site.register(views.CommAdminView,GlobalSettings)
