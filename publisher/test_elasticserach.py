from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch
from typing import List

app = FastAPI()
es = Elasticsearch(["http://han-box.co.kr:9200"], basic_auth=("", ""))

@app.get("/search/products")
async def search_products(product_name: str):
    query = {
        "query": {
            "match": {
                "name": product_name
            }
        },
        "sort": [
            {"dateCreated": {"order": "desc"}}
        ],
        "size": 10
    }
    results = es.search(index="hot_deals", body=query)
    if not results['hits']['hits']:
        raise HTTPException(status_code=404, detail="No products found")
    return [hit['_source'] for hit in results['hits']['hits']]

@app.get("/search/product_with_price")
async def search_products_by_price(product_name: str, max_price: float):
    query = {
        "query": {
            "bool": {
                "must": [
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
    results = es.search(index="hot_deals", body=query)
    if not results['hits']['hits']:
        raise HTTPException(status_code=404, detail="No products found within the price range")
    return [hit['_source'] for hit in results['hits']['hits']]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)