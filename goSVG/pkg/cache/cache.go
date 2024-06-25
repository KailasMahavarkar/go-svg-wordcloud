package cache

import (
	"sync"
	"time"
)

type CacheEntry struct {
	Value      SearchRequest
	ExpiryTime time.Time
}

type Cache struct {
	cache map[string]CacheEntry
	mutex sync.RWMutex
}

type SearchRequest struct {
	Timeout int
	Links   []string
}

func NewURLCache() *Cache {
	return &Cache{
		cache: make(map[string]CacheEntry),
	}
}

func (c *Cache) Get(key string) (SearchRequest, bool) {
	c.mutex.RLock()
	entry, found := c.cache[key]
	c.mutex.RUnlock()

	if found && time.Now().Before(entry.ExpiryTime) {
		return entry.Value, true
	}

	return SearchRequest{
		Timeout: 0,
		Links:   []string{},
	}, false
}

func (c *Cache) Set(key string, value SearchRequest, expiry time.Time) {
	c.mutex.Lock()
	c.cache[key] = CacheEntry{
		Value:      value,
		ExpiryTime: expiry,
	}
	c.mutex.Unlock()
}

func (c *Cache) Clear() {
	c.mutex.Lock()
	for key, entry := range c.cache {
		if time.Now().After(entry.ExpiryTime) {
			delete(c.cache, key)
		}
	}
	c.mutex.Unlock()
}

func (c *Cache) Items() map[string]CacheEntry {
	c.mutex.RLock()
	defer c.mutex.RUnlock()
	return c.cache
}
