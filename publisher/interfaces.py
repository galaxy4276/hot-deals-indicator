from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

class ProductSearchService(ABC):
    @abstractmethod
    async def search_products(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

class NotificationService(ABC):
    @abstractmethod
    async def send_notification(self, session_id: str, products: List[Dict[str, Any]]):
        pass

class MonitoringLogger:
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)

    def log_search(self, session_id: str, results: List[Dict[str, Any]]):
        self.logger.info(f"Search for session {session_id}: {len(results)} products found")

    def log_error(self, session_id: str, error: Exception):
        self.logger.error(f"Error in session {session_id}: {str(error)}")
