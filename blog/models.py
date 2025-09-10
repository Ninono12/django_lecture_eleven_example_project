from datetime import date

from django.db import models
from django.db.models.query import QuerySet

class Author(models.Model):
    first_name = models.CharField(verbose_name='სახელი', max_length=100)
    last_name = models.CharField(verbose_name='გვარი', max_length=100)
    birth_date = models.DateField(verbose_name='დაბადების თარიღი', null=True)

    @property
    def age(self):
        if not self.birth_date:  # თუ არ აქვს დაბადების თარიღი
            return None
        today = date.today()
        return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def get_blog_posts(self) -> QuerySet["BlogPost"]:
        return self.blog_posts.all()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class BlogPost(models.Model):
    title = models.CharField(verbose_name="სათაური", max_length=255)
    text = models.CharField(verbose_name="ტექსტი")
    active = models.BooleanField(default=True, verbose_name='აქტიურია')
    create_date = models.DateTimeField(verbose_name='შექმნის თარიღი', null=True)
    update_date = models.DateTimeField(verbose_name="განახლების თარიღი", null=True)
    website = models.URLField(verbose_name='ვებ მისამართი', null=True, blank=True)
    document = models.FileField(upload_to='blog_document/', null=True, blank=True)
    authors = models.ManyToManyField('blog_app.Author', related_name='blog_posts', blank=True)
    deleted = models.BooleanField(verbose_name="წაშლილია", default=False)

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['title']
        unique_together = [['title', 'text']]

    def get_images(self) -> QuerySet['BlogPostImage']:
        return BlogPostImage.objects.filter(blog_post=self)

    def __str__(self) -> str:
        return self.title


class BannerImage(models.Model):
    blog_post = models.OneToOneField(
        'blog_app.BlogPost',
        related_name='banner_image',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='banner_image/', null=True, blank=True)

    class Meta:
        verbose_name = "Banner Image"
        verbose_name_plural = "Banner Images"
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.blog_post.title} - {self.id} image'


class BlogPostImage(models.Model):
    image = models.ImageField(upload_to='blog_image/')
    blog_post = models.ForeignKey('blog_app.BlogPost', on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = "Blog Post Image"
        verbose_name_plural = "Blog Post Images"
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.blog_post.title} - {self.id} image'