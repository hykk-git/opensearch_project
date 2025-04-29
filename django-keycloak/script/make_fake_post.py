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

# 한글 기반
fake = Faker('ko_KR')
User = get_user_model()

# 임시로 첫 번째 유저 사용
author = User.objects.first()

# 랜덤 한글 키워드 리스트
keywords = ['여행', '해외여행', '맛집', '운동', '영화', '공부', '독서', '요리', '사진', '기술', '자연']

# Post 생성
for _ in range(200):
    Post.objects.create(
        title=fake.catch_phrase(),
        keyword=random.choice(keywords),
        content=fake.catch_phrase(),
        author=author
    )