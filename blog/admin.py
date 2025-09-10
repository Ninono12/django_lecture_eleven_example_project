from django.contrib import admin
from blog_app.models import BlogPost, BlogPostImage, Author, BannerImage

admin.site.register(BlogPostImage)
admin.site.register(Author)
admin.site.register(BannerImage)


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'deleted')  # Fields to display in list view
    list_filter = ('active', 'deleted')             # Fields to filter by
    search_fields = ('title',)           # Fields to search in
    ordering = ('-create_date',)                        # Default ordering

admin.site.register(BlogPost, BlogPostAdmin)
