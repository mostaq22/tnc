from django.contrib import admin
# To overwrite the admin form fields
from django import forms
# Editor Code Base
from tinymce.widgets import TinyMCE
# Register your models here.
from django.utils.safestring import mark_safe
# import models
from .models import Category, Newspaper, Fact, Post, Like


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'show_in_menu']


admin.site.register(Category, CategoryAdmin)


class NewsPaperAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'site_logo']

    def site_logo(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.logo.url,
            width='100',
            height='75',
        )
        )


admin.site.register(Newspaper, NewsPaperAdmin)


class NewsPaperPostInline(admin.TabularInline):
    model = Post
    extra = 1


class PostForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'body_content', 'category', 'image', 'show_in_homepage', 'likes']
    inlines = [NewsPaperPostInline, ]
    form = PostForm

    def image(self, obj):
        return mark_safe(f'<img height="50" width="50" src="{obj.image}"')

    def body_content(self, obj):
        return obj.body[:25] + " .."

    def likes(self, obj):
        return obj.like.all().count()


admin.site.register(Fact, PostAdmin)


class NewsPaperPostForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))


class NewsPaperPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'fact', 'body_content', 'newspaper', 'show_in_homepage', 'likes']
    form = NewsPaperPostForm

    def body_content(self, obj):
        return mark_safe(obj.body[:25] + " ..")

    def likes(self, obj):
        return obj.like.all().count()


admin.site.register(Post, NewsPaperPostAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = ['visitor_ip', 'content_type',
                    'post_url'
                    ]

    def post_url(self, obj):
        from django.urls import reverse
        app_name = "admin:" + str(obj.content_type).replace(" | ", "_").replace(' ', '') + "_change"
        change_url = reverse(app_name, args=(obj.object_id,))
        return mark_safe('<a href="%s"> %s</a>' % (change_url, obj.object_id))


admin.site.register(Like, LikeAdmin)
