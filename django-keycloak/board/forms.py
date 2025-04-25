from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'keyword', 'content', 'file']
        labels = {
            'title': '제목',
            'keyword': '키워드',
            'content': '내용',
            'file': '첨부 파일',
        }
