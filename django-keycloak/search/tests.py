from django.test import TestCase
import time
from django.db import connection
from search.documents import PostDocument  

# 1. DB 인덱스 검색
def test_db_index(keyword):
    start = time.time()
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM post WHERE keyword = %s", [keyword]
        )
        results = cursor.fetchall()
    end = time.time()
    return end - start, results

# 2. OpenSearch 역색인 검색
def test_opensearch(keyword):
    start = time.time()
    search = PostDocument.search().query("match", keyword=keyword)
    response = search.execute()
    ids = [int(hit.meta.id) for hit in response]
    end = time.time()
    return end - start, ids

# 3. DB full-text search 검색
def test_db_fulltext(keyword):
    start = time.time()
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM post WHERE search_vector @@ plainto_tsquery('simple', %s)", [keyword]
        )
        results = cursor.fetchall()
    end = time.time()
    return end - start, results

# 테스트 실행
if __name__ == "__main__":
    keyword = "여행"

    db_index_time, db_index_results = test_db_index(keyword)
    opensearch_time, opensearch_results = test_opensearch(keyword)
    db_fulltext_time, db_fulltext_results = test_db_fulltext(keyword)

    print(f"DB 인덱스 검색 시간: {db_index_time:.6f}초, 결과 개수: {len(db_index_results)}")
    print(f"OpenSearch 검색 시간: {opensearch_time:.6f}초, 결과 개수: {len(opensearch_results)}")
    print(f"DB Full-Text 검색 시간: {db_fulltext_time:.6f}초, 결과 개수: {len(db_fulltext_results)}")
