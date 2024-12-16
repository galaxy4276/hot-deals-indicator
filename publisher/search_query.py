import asyncio
from elasticsearch import AsyncElasticsearch
from interfaces import ProductSearchService
from settings import AppSettings

class ElasticsearchProductSearchService(ProductSearchService):
    def __init__(self, settings: AppSettings):
        self.settings = settings
        self.es = AsyncElasticsearch(
            self.settings.ELASTICSEARCH_HOST, 
            basic_auth=(
                self.settings.ELASTICSEARCH_USERNAME, 
                self.settings.ELASTICSEARCH_PASSWORD
            )
        )

    async def search_products(self, info: dict) -> list:
        must_clauses = [
            {"match": {"name": info.get('product_name')}},
            {"range": {"price": {"lte": info.get('max_price', float('inf'))}}}
        ]
        
        category = info.get('category')
        if category and category != "모든 카테고리":
            must_clauses.append({"match": {"category": category}})
    

        query = {
            "query": {
                "bool": {
                    "must": must_clauses
                }
            },
            "sort": [{"dateCreated": {"order": "desc"}}],
            "size": self.settings.MAX_RESULTS_PER_SEARCH
        }
        
        try:
            results = await self.es.search(index="hot_deals", body=query)
            return [
                {
                    "name": hit["_source"]["name"],
                    "price": hit["_source"]["price"],
                    "link": hit["_source"]["link"]
                }
                for hit in results["hits"]["hits"]
            ]
        except Exception as e:
            raise RuntimeError(f"Elasticsearch search failed: {str(e)}")