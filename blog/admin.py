from django.contrib import admin
from blog_app.models import BlogPost, BlogPostImage, Author, BannerImage


@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    raw_id_fields = ('blog_post',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'age')


class BlogPostImageInline(admin.TabularInline):
    model = BlogPostImage
    extra = 4


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    inlines = [BlogPostImageInline]
    list_display = ('title', 'active', 'deleted')
    list_filter = ('active', 'deleted')
    search_fields = ('title',)
    ordering = ('-create_date',)
    date_hierarchy = 'create_date'
    filter_horizontal = ('authors',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(active=True)