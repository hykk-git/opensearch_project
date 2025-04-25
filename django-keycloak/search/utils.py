from .opensearch_client import client

def search_posts(keyword):
    query = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["keyword", "content"]
            }
        }
    }

    result = client.search(index="posts", body=query)
    
    hits = result['hits']['hits']
    return [hit['_source'] for hit in hits]