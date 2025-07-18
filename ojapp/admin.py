from django.contrib import admin
from django.contrib import admin
from .models import Question, Choice, Problems

# Optional: Show choices inline when editing a question
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

# Customize how Question appears in admin
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'author')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    inlines = [ChoiceInline]  # Show choices in the question edit page

# Register models with custom admin
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Problems)

# Register your models here.
