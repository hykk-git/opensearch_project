# search/utils.py
from search.documents import PostDocument

def search_posts(search_type, search_text):
    if search_type == "keyword":
        fields = ["keyword"]
    elif search_type == "content":
        fields = ["content"]
    else:
        fields = ["keyword", "content"] 

    query = {
        "multi_match": {
            "query": search_text,
            "fields": fields
        }
    }

    search = PostDocument.search().query(query)
    response = search.execute()

    post_ids = [int(hit.meta.id) for hit in response]
    return post_ids