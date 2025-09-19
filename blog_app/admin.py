from django.contrib import admin
from blog_app.models import BlogPost, BlogPostImage, Author, BannerImage, BlogPostImageDescription
from nested_admin import NestedTabularInline, NestedModelAdmin

@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    raw_id_fields = ('blog_post',)

class MembershipInline(admin.StackedInline):
    model = BlogPost.authors.through

class BlogPostImageDescriptionInline(NestedTabularInline):
    model = BlogPostImageDescription
    fk_name = 'blog_post_image'
    extra = 1

class BlogPostImageInline(NestedTabularInline):
    model = BlogPostImage
    inlines = [BlogPostImageDescriptionInline]
    extra = 4
    ordering = ['order']

@admin.register(BlogPost)
class BlogPostAdmin(NestedModelAdmin):
    inlines = [BlogPostImageInline]  # MembershipInline ამოღებული
    list_display = ('title', 'active', 'deleted', 'order')
    ordering = ('order',)
    list_filter = ('active', 'deleted')
    search_fields = ('title',)
    filter_horizontal = ('authors',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(active=True)