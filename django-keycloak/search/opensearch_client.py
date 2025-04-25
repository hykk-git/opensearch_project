# opensearch_client.py
from django.conf import settings
from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{
        "host": settings.OPENSEARCH["HOST"],
        "port": settings.OPENSEARCH["PORT"]
    }],
    http_auth=(settings.OPENSEARCH["USER"], settings.OPENSEARCH["PASSWORD"]),
    http_compress=True,
    use_ssl=False,
    verify_certs=False,
)