from elasticsearch import Elasticsearch

es = Elasticsearch(["http://han-box.co.kr:9200"], basic_auth=("id", "password"))

async def search_products(product_name, max_price):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"name": product_name}},
                    {"range": {"price": {"lte": max_price}}}
                ]
            }
        }
    }
    results = es.search(index="hot_deals", body=query)
    return results