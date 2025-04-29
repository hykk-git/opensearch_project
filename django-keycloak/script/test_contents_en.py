import os
import sys
import django

# path 명시
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import time
from django.db import connection
from search.documents import PostDocument

# 1. DB 인덱스 검색
def test_db_index(keyword):
    start = time.time()
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM board_post WHERE keyword = %s", [keyword]
        )
        results = cursor.fetchall()
    end = time.time()
    return end - start, results

# 2. OpenSearch 역색인 검색
def test_opensearch(keyword):
    start = time.time()
    search = PostDocument.search().query("match", content=content)
    response = search.execute()
    ids = [int(hit.meta.id) for hit in response]
    end = time.time()
    return end - start, ids

# 3. DB full-text search 검색- AND
# def test_db_fulltext(keyword):
#     start = time.time()
#     with connection.cursor() as cursor:
#         cursor.execute(
#             "SELECT id FROM board_post WHERE to_tsvector('english', content) @@ to_tsquery('english', %s)", [keyword]
#         )
#         results = cursor.fetchall()
#     end = time.time()
#     return end - start, results

# DB full-text search 검색- OR
def test_db_fulltext(keyword_str):
    # 공백으로 나눈 단어들을 OR 연산자로 연결
    keywords = keyword_str.lower().split()
    tsquery = ' | '.join(keywords)

    start = time.time()
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM board_post WHERE to_tsvector('english', content) @@ to_tsquery('english', %s)", [tsquery]
        )
        results = cursor.fetchall()
    end = time.time()
    return end - start, results

# 테스트 실행
if __name__ == "__main__":
    content = "Greens physicals stages asks suggests writes"

    db_index_time, db_index_results = test_db_index(content)
    opensearch_time, opensearch_results = test_opensearch(content)
    db_fulltext_time, db_fulltext_results = test_db_fulltext(content)

    print(f"DB 인덱스 검색 시간: {db_index_time:.6f}초, 결과 개수: {len(db_index_results)}")
    print(f"OpenSearch 검색 시간: {opensearch_time:.6f}초, 결과 개수: {len(opensearch_results)}")
    print(f"DB Full-Text 검색 시간: {db_fulltext_time:.6f}초, 결과 개수: {len(db_fulltext_results)}")
