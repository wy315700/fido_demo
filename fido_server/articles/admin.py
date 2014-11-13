from django.contrib import admin
from articles.models import Essay, Comment, BaseCategory
# Register your models here.
admin.site.register(Essay)
admin.site.register(Comment)
admin.site.register(BaseCategory)