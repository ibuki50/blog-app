from django.contrib import admin
from .models import Post, Category

# Register your models here.
class Check_listAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_display_links = ('id', 'name',)
admin.site.register(Post)
admin.site.register(Category)