from django.contrib import admin
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin
from blog.resources import BlogPostResource
from blog_app.models import BlogPost, BlogPostImage, Author, BannerImage, BlogPostImageDescription
from nested_admin import NestedTabularInline, NestedModelAdmin, NestedStackedInline


@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    raw_id_fields = ('blog_post',)


class MembershipInline(NestedStackedInline):
    model = BlogPost.authors.through
    extra = 1


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
class BlogPostAdmin(NestedModelAdmin, ImportExportModelAdmin):
    inlines = [BlogPostImageInline, MembershipInline]
    list_display = ('title', 'active', 'deleted', 'order')
    ordering = ('order',)
    list_filter = ('active', 'deleted')
    search_fields = ('title',)
    actions = ['export_selected']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(active=True)

    def export_selected(self, request, queryset):
        resource = BlogPostResource()
        dataset = resource.export(queryset)
        response = HttpResponse(
            dataset.export('xlsx'),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="books.xlsx"'
        return response