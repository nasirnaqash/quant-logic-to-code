import hashlib
import json
import redis
from config.settings import REDIS_HOST, REDIS_PORT


class Cache:
    def __init__(self):
        try:
            self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
            self.redis.ping()  # Test connection
            self.connected = True
        except redis.ConnectionError:
            print("Warning: Redis not connected. Caching disabled.")
            self.connected = False
    
    def normalize(self, yaml_data: dict) -> str:
        # Convert YAML data to consistent JSON string
        return json.dumps(yaml_data, sort_keys=True)
    
    def get_hash(self, yaml_data: dict) -> str:
        # Create unique hash for this YAML
        normalized = self.normalize(yaml_data)
        return hashlib.sha256(normalized.encode()).hexdigest()
    
    def get(self, yaml_data: dict) -> str | None:
        # Get cached code if exists
        if not self.connected:
            return None
        
        key = self.get_hash(yaml_data)
        cached = self.redis.get(f"code:{key}")
        
        if cached:
            print(f"Cache HIT: {key[:16]}...")
            return cached.decode()
        
        print(f"Cache MISS: {key[:16]}...")
        return None
    
    def set(self, yaml_data: dict, code: str) -> None:
        # Store generated code in cache
        if not self.connected:
            return
        
        key = self.get_hash(yaml_data)
        self.redis.set(f"code:{key}", code)
        print(f"Cached: {key[:16]}...")


# Test it
if __name__ == "__main__":
    cache = Cache()
    
    test_data = {"metadata": {"logic_id": "test"}}
    
    # Test hash
    print(f"Hash: {cache.get_hash(test_data)}")
    
    # Test get (should be None)
    result = cache.get(test_data)
    print(f"Get: {result}")
    
    # Test set
    if cache.connected:
        cache.set(test_data, "def test(): pass")
        result = cache.get(test_data)
        print(f"After set: {result}")