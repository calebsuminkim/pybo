from django import forms
from pybo.models import Question, Answer, Comment # 데이터베이스 연결

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content', 'image']

        labels = {
            'subject' : '제목',
            'content' : '내용',
            'image' : '이미지',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변 내용'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        labels = {
            'content' : '댓글 내용',
        }