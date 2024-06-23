package cache

import (
	"time"
)

func NewURLCache() *Cache {
	return &Cache{
		cache: make(map[string]CacheEntry),
	}
}

func (c *Cache) Get(key string) (string, bool) {
	c.mutex.RLock()
	entry, found := c.cache[key]
	c.mutex.RUnlock()

	if found && time.Now().Before(entry.ExpiryTime) {
		return entry.Value, true
	}

	return "", false
}

func (c *Cache) Set(key string, value string, expiry time.Time) {
	c.mutex.Lock()
	c.cache[key] = CacheEntry{
		Value:      value,
		ExpiryTime: expiry,
	}

	c.mutex.Unlock()
}

// run a cron job to clear the cache every "T" minutes
func (c *Cache) Clear() {
	c.mutex.Lock()
	for key, entry := range c.cache {
		if time.Now().After(entry.ExpiryTime) {
			delete(c.cache, key)
		}
	}
	c.mutex.Unlock()
}

// get all items in the cache
func (c *Cache) Items() map[string]CacheEntry {
	return c.cache
}
