from django.contrib import admin
from .models import Question, Answer, QuestionSet
# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    pass


class AnswerAdmin(admin.ModelAdmin):
    pass


class QuestionSetAdmin(admin.ModelAdmin):
    pass


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(Answer, AnswerAdmin)