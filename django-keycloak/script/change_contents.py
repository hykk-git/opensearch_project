import os
import sys
import django

# path 명시
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from board.models import Post

sample_sentences = [
    "This is a great place to visit.",
    "You should share this post with friends.",
    "Traveling is a wonderful experience.",
    "Learning English can be fun and exciting.",
    "Let's plan a new trip together."
]

sample_keywords = ["travel", "visit", "experience", "enjoy", "learn"]

# post content 일괄 변경
for idx, post in enumerate(Post.objects.all()):
    # post.content = sample_sentences[idx % len(sample_sentences)]
    post.keyword = sample_keywords[idx % len(sample_keywords)]
    post.save()