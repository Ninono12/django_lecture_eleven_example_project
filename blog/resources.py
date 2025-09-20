from import_export import resources
from blog_app.models import BlogPost


class BlogPostResource(resources.ModelResource):
    class Meta:
        model = BlogPost
        # Optional: Control which fields are included
        fields = ('id', 'title', 'author', 'published_date')
