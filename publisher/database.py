from elasticsearch import Elasticsearch

es = Elasticsearch(["http://han-box.co.kr:9200"], basic_auth=("", ""))

async def search_products(product_name, max_price):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match_all": {}},
                    {
                        "script": {
                            "script": {
                                "source": """
                                    def price_str = doc['price.keyword'].value;
                                    if (price_str == null || price_str.empty) return false;
                                    def price_num = price_str.replace(',', '');
                                    return Double.parseDouble(price_num) <= params.max_price;
                                """,
                                "params": {
                                    "max_price": float(max_price)
                                }
                            }
                        }
                    }
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

