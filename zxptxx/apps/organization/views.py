# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg,CityDict

# Create your views here.
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger



class OrgView(View):
    def get(self,request):
        all_org = CourseOrg.objects.all()
        all_city = CityDict.objects.all()

        #筛选城市
        city_id = request.GET.get('city',"")
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))

        #筛选机构类别
        category = request.GET.get('ct',"")
        if category:
            all_org = all_org.filter(catego=category)

        # 热门机构,如果不加负号会是有小到大。
        hot_orgs = all_org.order_by("-click_nums")[:3]

        #进行课程和学习人数排序
        sort = request.GET.get('sort',"")
        if sort:
            if sort == "students":
                all_org = all_org.order_by('-students')
            elif sort == "courses":
                all_org = all_org.order_by('-course_nums')

        # 分页功能
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        #参数一是分页对象，参数二是：一页多少个数据
        p = Paginator(all_org,3,request=request)

        #获取当前页数的数据
        orgs = p.page(page)

        #获取一共多少家机构
        org_number = all_org.count()


        return render(request,'org-list.html',{
            'all_org':orgs,
            'all_city':all_city,
            'org_number':org_number,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort,

        })