# _*_ encoding:utf-8 _*_
__author__ = 'pig'
__data__ = '2018\7\15 0015 21:13$'

import xadmin
from .models import Course, Lesson, Video, CourseResource

class CourseAdmin(object):
    list_display = [
        'name',
        'desc',
        'datail',
        'degree',
        'learn_time',
        'student']
    search_fields = ['name', 'desc', 'datail', 'degree', 'students']
    list_filter = [
        'name',
        'desc',
        'datail',
        'degree',
        'learn_time',
        'student']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']

    # __name代表使用外键中name字段
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    # __name代表使用外键中name字段
    list_filter = ['course__name', 'name', 'download', 'add_time']


# 将管理器与model进行注册关联
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
