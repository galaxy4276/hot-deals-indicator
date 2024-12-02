from elasticsearch import AsyncElasticsearch

es = AsyncElasticsearch(["http://han-box.co.kr:9200"], basic_auth=("", ""))

async def search_products(product_name, max_price):
    query = {
        "query": {
            "bool": {
                "must": [
                    # {"match_all": {}}, # for test
                    {"match": {"name": product_name}},

                    {"range": {"price": {"lte": max_price}}}

                ]
            }
        },
        "sort": [
            {"dateCreated": {"order": "desc"}}
        ],
        "size": 10
    }
    results = await es.search(index="hot_deals", body=query)
    return results

