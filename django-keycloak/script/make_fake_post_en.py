import sys
import os
import django
import random
from faker import Faker

# Django 셋업
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from board.models import Post
from django.contrib.auth import get_user_model

fake = Faker('en_US')
User = get_user_model()

# 임시로 첫 번째 유저 사용
author = User.objects.first()

# 검색 키워드 리스트 (테스트용)
keywords = ["travel", "visit", "experience", "enjoy", "learn"]

# Post 대량 생성
bulk_posts = []
for _ in range(10000): 
    random_content = fake.paragraph(nb_sentences=3) 
    
    # 10% 확률로 검색 키워드 추가
    if random.random() < 0.1:
        random_content += " " + random.choice(keywords)
    
    post = Post(
        title=fake.catch_phrase(),
        keyword="sample",  
        content=random_content,
        author=author
    )
    bulk_posts.append(post)

# bulk insert
Post.objects.bulk_create(bulk_posts)
