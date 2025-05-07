import sys
import os
import django
import random
from faker import Faker

# path 명시
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from board.models import Post
from django.contrib.auth import get_user_model

# 영어 기반
fake = Faker('en_US')
User = get_user_model()

# 임시로 첫 번째 유저 사용
author = User.objects.first()

# 랜덤 영어 키워드 리스트
keywords = ["travel", "visit", "experience", "enjoy", "learn"]

posts = []
for _ in range(100000): 
    random_content = fake.paragraph(nb_sentences=3) 
    
    post = Post(
        title=fake.catch_phrase(),
        keyword="sample",  
        content=random_content,
        author=author
    )
    posts.append(post)

# bulk로 한 번에 DB에 저장, default=all
Post.objects.bulk_create(posts)
