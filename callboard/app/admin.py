from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from django.db import models
# Register your models here.
from .models import Post, Response, Category, PostCategory

class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostCategoryInline,)

class SomeModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'

admin.site.register(Post, SomeModelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Response)