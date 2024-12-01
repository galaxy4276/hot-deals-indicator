import asyncio
import json
import traceback
from database import search_products
from websocket_manager import manager

class ElasticsearchObserver:
    def __init__(self):
        self.observers = {}

    def register(self, session_id, user_data):
        self.observers[session_id] = user_data

    def unregister(self, session_id):
        if session_id in self.observers:
            del self.observers[session_id]

    async def notify(self):
        while True:
            try:
                for session_id, user_data in self.observers.items():
                    try:
                        results = await search_products(user_data["product_name"], user_data["max_price"])
                        if results["hits"]["total"]["value"] > 0:
                            matching_products = [
                                {
                                    "name": hit["_source"]["name"],
                                    "price": hit["_source"]["price"],
                                    "link": hit["_source"]["link"]
                                }
                                for hit in results["hits"]["hits"]
                            ]
                            await manager.send_personal_message(json.dumps(matching_products), session_id)
                    except Exception as e:
                        print(f"세션 {session_id}에 대한 처리 중 오류 발생: {str(e)}")
                        print(traceback.format_exc())
                print("모니터링 진행중")
            except Exception as e:
                print(f"notify 메서드에서 오류 발생: {str(e)}")
                print(traceback.format_exc())
            finally:
                await asyncio.sleep(10)

elasticsearch_observer = ElasticsearchObserver()