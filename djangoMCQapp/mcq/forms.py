from django import forms
from .models import Answer, Question, QuestionSet


# class QuestionForm(forms.ModelForm):
#     answers = forms.ModelMultipleChoiceField(queryset=Answer.objects.filter(question=self.question_id))
#     class Meta:
#         model = Question
#         fields = ['question']
#
#     def __init__(self,question_id):
#         self.question_id = question_id
#         super(QuestionForm).__init__()
