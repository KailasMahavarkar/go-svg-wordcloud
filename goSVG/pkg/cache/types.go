package cache

import (
	"sync"
	"time"
)

type Cache struct {
	cache map[string]CacheEntry
	mutex sync.RWMutex
}

type CacheEntry struct {
	Value      string
	ExpiryTime time.Time
}
