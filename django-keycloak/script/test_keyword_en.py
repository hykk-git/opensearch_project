import os
import sys
import django

# Django 설정 초기화
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import time
from django.db import connection
from board.models import Post  # 모델 import
from search.documents import PostDocument


# 1. DB 인덱스 검색
def test_db_index(keyword):
    start = time.time()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM board_post WHERE keyword = %s", [keyword])
        results = cursor.fetchall()
    end = time.time()
    ids = [r[0] for r in results]
    return end - start, ids


# 2. OpenSearch match 쿼리 (score 포함)
def test_opensearch(keyword):
    start = time.time()
    response = PostDocument.search().query("term", keyword=keyword).extra(size=10000).execute()
    results = [(int(hit.meta.id), hit.meta.score) for hit in response]
    end = time.time()
    return end - start, results

# 3. DB Full-Text 검색 (rank 점수 포함)
def test_db_fulltext(keyword_str):
    keywords = keyword_str.lower().split()
    tsquery = ' | '.join(keywords)

    start = time.time()
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, ts_rank(to_tsvector('english', keyword), to_tsquery('english', %s)) AS rank
            FROM board_post
            WHERE to_tsvector('english', keyword) @@ to_tsquery('english', %s)
            ORDER BY rank DESC
            """,
            [tsquery, tsquery]
        )
        results = cursor.fetchall()
    end = time.time()
    return end - start, results


# ID 목록으로 content와 keyword 조회
def get_post_data(post_score_pairs):
    ids = [pid for pid, _ in post_score_pairs]
    posts = Post.objects.filter(id__in=ids).values_list('id', 'content', 'keyword')
    post_map = {pid: (content, keyword) for pid, content, keyword in posts}
    return [(pid, score, post_map.get(pid, ("[No content]", "[No keyword]"))) for pid, score in post_score_pairs]


# 테스트 실행
if __name__ == "__main__":
    content = "learn"

    db_index_time, db_index_ids = test_db_index(content)
    opensearch_time, opensearch_results = test_opensearch(content)
    db_fulltext_time, db_fulltext_results = test_db_fulltext(content)

    # 출력
    print(f"\nDB 인덱스 검색 시간: {db_index_time:.6f}초, 결과 개수: {len(db_index_ids)}")
    print(f"OpenSearch 검색 시간: {opensearch_time:.6f}초, 결과 개수: {len(opensearch_results)}")
    print(f"DB Full-Text 검색 시간: {db_fulltext_time:.6f}초, 결과 개수: {len(db_fulltext_results)}")

    print("\n=== DB 인덱스 상위 10개 ===")
    db_index_posts = get_post_data([(pid, None) for pid in db_index_ids[:10]])
    for pid, _, (content, keyword) in db_index_posts:
        print(f"ID {pid} | keyword: {keyword} | content: {content[:70]}...")

    print("\n=== OpenSearch 상위 10개 (score 포함) ===")
    opensearch_posts = get_post_data(opensearch_results[:10])
    for pid, score, (content, keyword) in opensearch_posts:
        print(f"ID {pid} | score: {score:.4f} | keyword: {keyword} | content: {content[:70]}...")

    print("\n=== DB Full-Text 상위 10개 (rank 포함) ===")
    db_fulltext_posts = get_post_data(db_fulltext_results[:10])
    for pid, rank, (content, keyword) in db_fulltext_posts:
        print(f"ID {pid} | rank: {rank:.4f} | keyword: {keyword} | content: {content[:70]}...")
