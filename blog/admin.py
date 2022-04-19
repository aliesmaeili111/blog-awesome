from django.contrib import admin
from . models import Article,Category,IPAddress
from account.models import User 
# admin header change 
admin.site.site_header = 'مدیریت وبلاگ'


# convert article to publish action
def make_published(modeladmin,request,queryset):
    rows_updated = queryset.update(status='p') 
    if rows_updated == 1 :
        message_bit = "منتشر شد"
    else:
        message_bit = " منتشر شدند"
    modeladmin.message_user(request,"{} مقاله {} .".format(rows_updated,message_bit))

make_published.short_description = "انتشار مقالات انتخاب شده"

# convert article to draft action
def make_draft(modeladmin,request,queryset):
    rows_updated = queryset.update(status='d')
    if rows_updated == 1 :
        message_bit = "پیش نویس شد"
    else:
        message_bit = " پیش نویس شدند"
    modeladmin.message_user(request,"{} مقاله {} .".format(rows_updated,message_bit))

make_draft.short_description = "پیش نویس شدن مقالات انتخاب شده"


def make_category_false(modeladmin,request,queryset):
    rows_updated = queryset.update(status=False)
    if rows_updated == 1 :
        message_bit = "این دسته بندی نمایش داده نمی شود"
    else:
        message_bit = "   دسته بندی ها  نمایش داده نمی شود"
    modeladmin.message_user(request,"{} {} .".format(rows_updated,message_bit))

make_category_false.short_description = "  نمایش ندادن دسته بندی ها "


def make_category_true(modeladmin,request,queryset):
    rows_updated = queryset.update(status=True)
    if rows_updated == 1 :
        message_bit = "این دسته بندی نمایش داده می شود"
    else:
        message_bit = "   دسته بندی ها  نمایش داده می شود"
    modeladmin.message_user(request,"{} {} .".format(rows_updated,message_bit))

make_category_true.short_description = "  نمایش دادن دسته بندی ها "
# end actions

# Category admin customize
class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ('position','title','slug','status')
    list_filter = (['status'])
    search_fields = ('title','slug')
    prepopulated_fields = {'slug':('title',)}
    actions=[make_category_true,make_category_false]
    
admin.site.register(Category,CategoryAdmin)


#Articel admin customize
class ArticleAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    list_display = ('title','thumbnail_tag','slug','author','jpublish','is_special','status','category_to_str')
    list_filter = ('publish','status','author')
    search_fields = ('title','description')
    prepopulated_fields = {'slug':('title',)}
    ordering = ['-status','-publish']
    actions=[make_published,make_draft]
    

admin.site.register(Article,ArticleAdmin)
admin.site.register(IPAddress)