"""Memory management for AI agents."""
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
import json


@dataclass 
class MemoryItem:
    """A single memory item."""
    key: str
    value: Any
    created_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    last_accessed: Optional[datetime] = None


class VectorMemory:
    """Simple key-value memory with access tracking."""

    def __init__(self, max_items: int = 1000):
        self.items: Dict[str, MemoryItem] = {}
        self.max_items = max_items

    def store(self, key: str, value: Any) -> None:
        """Store a memory item."""
        self.items[key] = MemoryItem(key=key, value=value)
        
        # Evict if over capacity
        if len(self.items) > self.max_items:
            oldest = min(self.items.values(), key=lambda x: x.created_at)
            del self.items[oldest.key]

    def retrieve(self, key: str, increment_access: bool = True) -> Any:
        """Retrieve a memory item."""
        if key not in self.items:
            return None
        
        item = self.items[key]
        if increment_access:
            item.access_count += 1
            item.last_accessed = datetime.now()
        
        return item.value

    def search(self, query: str) -> List[Dict]:
        """Simple keyword search in memories."""
        results = []
        query_lower = query.lower()
        
        for key, item in self.items.items():
            if query_lower in key.lower() or query_lower in str(item.value).lower():
                results.append({
                    "key": key,
                    "value": item.value,
                    "relevance": item.access_count
                })
        
        return sorted(results, key=lambda x: x["relevance"], reverse=True)

    def forget(self, key: str) -> bool:
        """Forget a specific memory."""
        if key in self.items:
            del self.items[key]
            return True
        return False

    def clear(self) -> None:
        """Clear all memories."""
        self.items.clear()

    def get_stats(self) -> Dict:
        """Get memory statistics."""
        total_accesses = sum(i.access_count for i in self.items.values())
        return {
            "total_memories": len(self.items),
            "total_accesses": total_accesses,
            "avg_accesses": total_accesses / len(self.items) if self.items else 0
        }
