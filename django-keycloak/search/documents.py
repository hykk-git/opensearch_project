from django_opensearch_dsl import Document, fields
from django_opensearch_dsl.registries import registry
from board.models import Post

@registry.register_document
class PostDocument(Document):
    keyword = fields.TextField(
        analyzer="english",  
        fields={
            "raw": fields.KeywordField()
        }
    )
    content = fields.TextField(
        analyzer="english"  
    )

    class Index:
        name = 'posts'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Post
        fields = ['id', 'title', 'created_at']
