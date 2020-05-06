from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    show_in_menu = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Like(models.Model):
    visitor_ip = models.CharField(max_length=100, null=True, blank=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.visitor_ip


class Newspaper(models.Model):
    name = models.CharField(max_length=200, unique=True)
    website = models.URLField()
    logo = models.ImageField(upload_to='newspaper')

    def __str__(self):
        return self.name

    def site_logo(self):
        from django.utils.html import escape
        return u'<img src="%s" />' % escape(self.logo)


class Fact(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=False)
    image = models.ImageField(blank=True)
    show_in_homepage = models.BooleanField(default=False)
    like = GenericRelation(Like, related_query_name='post')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Facts'


class Post(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.SET_NULL, null=True, blank=False, related_name="fact")
    newspaper = models.ForeignKey(Newspaper, on_delete=models.SET_NULL, null=True, blank=False)
    title = models.CharField(max_length=200)
    body = models.TextField()
    reference = models.URLField()
    image_link = models.CharField(max_length=200, null=True, blank=True)
    like = GenericRelation(Like, related_query_name='newspaper_post')
    show_in_homepage = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Advertisement(models.Model):
    name = models.CharField(max_length=200)
    advertise_code = models.TextField()
    active = models.BooleanField(default=False)
