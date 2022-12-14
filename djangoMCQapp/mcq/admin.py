from django.contrib import admin
from .models import Question, Answer, QuestionSet, UserAnswer, TestResult
# Register your models here.

class QuestionInline(admin.StackedInline):
    model = Question

class AnswerInline(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


class AnswerAdmin(admin.ModelAdmin):
    pass

class UserAnswerAdmin(admin.ModelAdmin):
    pass

class QuestionSetAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class TestResultAdmin(admin.ModelAdmin):
    pass


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(TestResult, TestResultAdmin)