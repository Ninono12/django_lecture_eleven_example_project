from django.contrib import admin
from blog_app.models import BlogPost, BlogPostImage, Author, BannerImage
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin


@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    raw_id_fields = ('blog_post',)


#@admin.register(Author)
#class AuthorAdmin(admin.ModelAdmin):
    #list_display = ('full_name', 'age')

class MembershipInline(admin.StackedInline):
    model = BlogPostImage.authors.through
    extra = 1

class BlogPostImageInline(SortableInlineAdminMixin, admin.StackedInline):
    model = BlogPostImage
    extra = 4
    ordering = ['order']


@admin.register(BlogPost)
class BlogPostAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [BlogPostImageInline]
    list_display = ('title', 'active', 'deleted', 'order')  # reorder გამოჩნდება აქ
    ordering = ('order',)  # ასევე დაჯგუფება list view-ში
    list_filter = ('active', 'deleted')
    search_fields = ('title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(active=True)