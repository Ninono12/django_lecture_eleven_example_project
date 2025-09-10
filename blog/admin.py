from django.contrib import admin
from blog_app.models import BlogPost, BlogPostImage, Author, BannerImage

admin.site.register(BlogPostImage)
admin.site.register(Author)
admin.site.register(BannerImage)


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'deleted')
    list_filter = ('active', 'deleted')
    search_fields = ('title',)
    ordering = ('-create_date',)
    #list_per_page = 1
    date_hierarchy = 'create_date'
    #fields = ('title', 'active', 'deleted')
    #exclude = ['title',]
    # filter_vertical = ('authors',)
    filter_horizontal = ('authors',)



admin.site.register(BlogPost, BlogPostAdmin)
