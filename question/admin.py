from django.contrib import admin
from question.models import Question,Tag,Owner
# Register your models here.

admin.site.register(Owner)

admin.site.register(Tag)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_name', 'search_term')
    list_filter = ('last_activity_date', 'score')
    search_fields = ('title',)

