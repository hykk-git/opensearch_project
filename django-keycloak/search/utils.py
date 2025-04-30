from search.documents import PostDocument
from typing import Any, Dict, List, Union

class SearchStrategy:
    def build_query(self, search_text: Union[str, List[str]]) -> Dict[str, Any]:
        pass

# Keyword 검색- term query
class KeywordSearchStrategy(SearchStrategy):
    def build_query(self, search_text):
        return {
            "terms": {
                "keyword.raw": search_text if isinstance(search_text, list) else [search_text]
            }
        }

# Content 검색- multi_match query
class ContentSearchStrategy(SearchStrategy):
    def build_query(self, search_text):
        return {
            "match": {
                "content": search_text
            }
        }

# 전체 검색- multi_match query
class CombinedSearchStrategy(SearchStrategy):
    def build_query(self, search_text):
        return {
           "multi_match": {
                "query": search_text,
                "fields": ["keyword", "content"]
            }
        }

TYPE = {
    "keyword": KeywordSearchStrategy(),
    "content": ContentSearchStrategy(),
    "all": CombinedSearchStrategy(),
}

# 검색 쿼리를 날리는 함수
def search_posts(search_type: str, search_text: Union[str, List[str]]) -> List[int]:
    strategy = TYPE.get(search_type, TYPE["all"])
    query = strategy.build_query(search_text)

    search = PostDocument.search().query(query)
    response = search.execute()
    return [int(hit.meta.id) for hit in response]