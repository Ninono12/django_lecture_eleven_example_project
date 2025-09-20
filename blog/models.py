from typing import Any

from django.db import models
from django.utils.timezone import now

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        from datetime import date
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

class BlogPost(models.Model):
    title = models.CharField(verbose_name="სათაური", max_length=255)
    text = models.TextField(verbose_name="ტექსტი", null=True, blank=True)
    authors = models.ManyToManyField(Author)
    active = models.BooleanField(default=True, verbose_name="აქტიურია")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="განახლების თარიღი", auto_now=True, null=True)
    website = models.URLField(verbose_name='ვებ მისამართი', null=True)
    document = models.FileField(upload_to='blog_document/', null=True, blank=True)
    deleted = models.BooleanField(verbose_name='წაშლილია', default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

class BlogPostImage(models.Model):
    authors = models.ManyToManyField("Author", related_name="images")
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="blog_images/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Blog post image"
        verbose_name_plural = "Blog post images"
        ordering = ['order']

    def __str__(self):
        return f'{self.blog_post.title} - {self.id} image'

class BlogPostImageDescription(models.Model):
    blog_post = models.ForeignKey(
        to='blog_app.BlogPostImage',
        on_delete=models.CASCADE,
        related_name='descriptions',
        verbose_name='Blog post image'
    )
    text = models.TextField(verbose_name='Text')

    class Meta:
        verbose_name = "Blog post image Description"
        verbose_name_plural = "Blog post images Descriptions"

    def __str__(self):
        return f'{self.blog_post.blog_post.title} - {self.id} image'


# ------------------ BannerImage Model ------------------

class BannerImage(models.Model):
    blog_post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name="banners",
        verbose_name="Blog post"
    )
    image = models.ImageField(upload_to="banner_images/", verbose_name="ბანერის სურათი")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Banner image"
        verbose_name_plural = "Banner images"
        ordering = ['order']

    def __str__(self):
        return f'{self.blog_post.title} - Banner {self.id}'
