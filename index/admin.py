from django.contrib import admin

# Register your models here.
from index.models import *

# 定义高级管理类
class GoodsAdmin(admin.ModelAdmin):
    # 定义搜索字段
    search_fields = ('title',)
    # 定义过滤器
    list_filter = ('goodsType',)
    # 定义在列表页中显示的字段们
    list_display = ('title','price','spec')


admin.site.register(GoodsType)
admin.site.register(Goods,GoodsAdmin)