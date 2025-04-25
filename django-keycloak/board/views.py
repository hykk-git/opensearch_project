from pathlib import Path

import os

from django.shortcuts import render, redirect

from .models import *
from .forms import PostForm
from search.documents import PostDocument  # Elasticsearch 색인 정보
from django.shortcuts import get_object_or_404

# .env 파일을 읽어서 현재 환경 변수로 로드하는 패키지
from dotenv import load_dotenv

# .env 파일에 있는 값들을 os.environ 딕셔너리에 추가
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent.parent

OIDC_OP_DOMAIN = os.getenv("OIDC_OP_DOMAIN")
OIDC_RP_CLIENT_ID = os.getenv("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = os.getenv("OIDC_RP_CLIENT_SECRET")

# 브라우저에서 Keycloak 로그인 페이지로 리디렉션할 때 사용할 주소
KEYCLOAK_BROWSER_DOMAIN = os.environ.get("KEYCLOAK_BROWSER_DOMAIN")  # ex: http://localhost:8080/realms/myrealm

#  Django 서버(Docker 컨테이너)에서 Keycloak과 통신할 때 사용할 주소
KEYCLOAK_INTERNAL_DOMAIN = os.environ.get("KEYCLOAK_INTERNAL_DOMAIN")  # ex: http://keycloak:8080/realms/myrealm

# 리디렉션용 (브라우저)
OIDC_OP_AUTHORIZATION_ENDPOINT = f"{KEYCLOAK_BROWSER_DOMAIN}/protocol/openid-connect/auth"
OIDC_OP_LOGOUT_ENDPOINT = f"{KEYCLOAK_BROWSER_DOMAIN}/protocol/openid-connect/logout"

# 서버용 (Django 컨테이너 내부에서 Keycloak에 요청)
OIDC_OP_TOKEN_ENDPOINT = f"{KEYCLOAK_INTERNAL_DOMAIN}/protocol/openid-connect/token"
OIDC_OP_USER_ENDPOINT = f"{KEYCLOAK_INTERNAL_DOMAIN}/protocol/openid-connect/userinfo"
OIDC_OP_JWKS_ENDPOINT = f"{KEYCLOAK_INTERNAL_DOMAIN}/protocol/openid-connect/certs"

# 메인화면
def main_view(request):
    return render(request, 'main.html')

# 게시판
def board_view(request):
    query = request.GET.get('q', '')
    # 모든 게시글 가져옴
    posts = Post.objects.all().order_by('-created_at')

    search_results = []
    if query:
        # PostDocument에서 키워드 검색
        search_result = PostDocument.search().query("match", keyword=query)

        # 키워드를 포함하는 게시글 id 저장
        post_ids = [int(hit.meta.id) for hit in search_result]
        
        # 검색 페이지 리턴
        search_results = Post.objects.filter(id__in=post_ids).order_by('-created_at')

    return render(request, 'board.html', {
        'posts': posts,
        'search_results': search_results,
        'query': query,
    })

# 게시글 작성 페이지
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            # 로그인된 사용자만 작성 가능
            post.author = request.user
            post.save()

            # 글 작성 후 목록으로 이동
            return redirect('board:board')
    else:
        # 글 양식이 뭔가 빠졌거나 재작성 필요
        form = PostForm()

    return render(request, 'post.html', {'form': form})

# 게시글 내용 열람 기능
def post_detail_view(request, pk):
    # 게시글 구분용 pk
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

# 본인 게시글 삭제 기능
def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 삭제 권한 확인
    if request.user != post.author:
        return redirect('board:post_detail', pk=pk)

    post.delete()
    return redirect('board:board')
