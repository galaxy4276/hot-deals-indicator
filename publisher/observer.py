import asyncio
from typing import Dict, Any
from interfaces import ProductSearchService, NotificationService, MonitoringLogger
from settings import AppSettings

class PerformanceTracker:
    @staticmethod
    def track_performance(func):
        async def wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                # 여기에 성능 메트릭스 수집 로직 추가 가능
                return result
            finally:
                end_time = time.time()
                print(f"Method {func.__name__} took {end_time - start_time:.4f} seconds")
        return wrapper

class ElasticsearchObserver:
    def __init__(
        self, 
        search_service: ProductSearchService, 
        notification_service: NotificationService,
        monitoring_logger: MonitoringLogger,
        settings: AppSettings
    ):
        self._search_service = search_service
        self._notification_service = notification_service
        self._monitoring_logger = monitoring_logger
        self._settings = settings
        self.observers: Dict[str, Dict[str, Any]] = {}

    def register(self, session_id: str, user_data: dict):
        self.observers[session_id] = user_data

    def unregister(self, session_id: str):
        if session_id in self.observers:
            del self.observers[session_id]

    @PerformanceTracker.track_performance
    async def notify(self, search_strategy=None):
        while True:
            try:
                for session_id, user_data in self.observers.items():
                    
                    results = await self._search_service.search_products(user_data)
                    
                    if results:
                        await self._notification_service.send_notification(session_id, results)
                        self._monitoring_logger.log_search(session_id, results)
                
                print("모니터링 진행중")
                await asyncio.sleep(self._settings.MONITORING_INTERVAL)
            
            except Exception as e:
                self._monitoring_logger.log_error("global", e)
                await asyncio.sleep(self._settings.MONITORING_INTERVAL)
