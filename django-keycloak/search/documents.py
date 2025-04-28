from django_opensearch_dsl import Document, fields
from django_opensearch_dsl.registries import registry
from board.models import Post

@registry.register_document
class PostDocument(Document):
    keyword = fields.TextField(
        analyzer="korean",
        fields={
            "raw": fields.KeywordField()
        }
    )
    content = fields.TextField(
        analyzer="korean",
    )

    class Index:
        name = 'posts'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'analysis': {
                'tokenizer': {
                    'nori_custom_tokenizer': {
                        'type': 'nori_tokenizer',
                        'decompound_mode': 'mixed'
                    }
                },
                'analyzer': {
                    'korean': {
                        'type': 'custom',
                        'tokenizer': 'nori_custom_tokenizer',
                        'filter': [
                            'lowercase',
                        ]
                    }
                }
            }
        }

    class Django:
        model = Post
        fields = ['id', 'title', 'created_at']