from django.contrib import admin
from cms.models import Article, Tag, Category

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'create_time', 'view')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_time', 'update_time')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_time', 'update_time')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)

