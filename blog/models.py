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
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(default=now)

class BlogPostImage(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="blog_images/")

class BannerImage(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='banners')
    image = models.ImageField(upload_to="banner_images/", default='banner_images/default.jpg')