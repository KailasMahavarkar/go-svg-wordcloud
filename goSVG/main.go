package main

import (
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"

	"gosvg/pkg/cache"
	"gosvg/pkg/scraper"

	"github.com/labstack/echo/v4"
)

type SearchRequest struct {
	Timeout time.Duration `json:"timeout"`
	Links   []string      `json:"links"`
}

type SearchResult struct {
	URL    string `json:"url"`
	Result string `json:"result,omitempty"`
	Error  string `json:"error,omitempty"`
}

var (
	taskID   int
	taskLock sync.Mutex
	urlCache *cache.Cache
)

func init() {
	// Initialize URL cache
	urlCache = cache.NewURLCache()

	// Start a goroutine to clear the cache every 5 minutes
	go func() {
		for {
			time.Sleep(5 * time.Minute)
			urlCache.Clear()
		}
	}()
}

func produceTask(c echo.Context) error {
	req := new(SearchRequest)
	if err := c.Bind(req); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid request body")
	}

	if req.Timeout <= 0 || len(req.Links) == 0 {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid timeout or empty links")
	}

	taskLock.Lock()
	taskID++
	currentTaskID := taskID
	taskLock.Unlock()

	// Store the task in the cache
	urlCache.Set(
		fmt.Sprintf("task-%d", currentTaskID),
		// currentTaskID, to string
		string(req.Timeout),
		time.Now().Add(10*time.Minute), // Expire in 10 minutes
	)

	// Return task ID to client
	return c.JSON(http.StatusOK, map[string]interface{}{
		"message": "Task added to queue",
		"taskID":  currentTaskID,
	})
}

func consumeTasks() {
	for {
		for key, item := range urlCache.Items() {
			// Process only task keys
			if key[:5] == "task-" {
				// Get task from cache
				req, ok := item.Object.(*SearchRequest)
				if !ok {
					continue
				}

				// Process each URL in the task
				for _, url := range req.Links {
					result := SearchResult{
						URL: url,
					}

					text, err := scraper.FetchWebsite(url, req.Timeout)
					if err != nil {
						result.Error = err.Error()
					} else {
						result.Result = text
					}

					// Store or process the result (in real application, you might store it or send it somewhere)
					log.Printf("Scraped URL: %s\nResult: %s\nError: %v\n", result.URL, result.Result, result.Error)
				}

				// Delete the task from cache after processing
				urlCache.Delete(key)
			}
		}
		time.Sleep(1 * time.Second) // Polling interval
	}
}

func taskStatus(c echo.Context) error {
	taskID := c.Param("taskID")

	// Get task status from cache
	task, found := urlCache.Get(fmt.Sprintf("task-%s", taskID))
	if !found {
		return echo.NewHTTPError(http.StatusNotFound, "task not found")
	}

	// Cast to SearchRequest
	req := task.(*SearchRequest)
	return c.JSON(http.StatusOK, req)
}

func main() {
	go consumeTasks() // Start consumer in a separate goroutine

	e := echo.New()

	// Routes
	e.POST("/search", produceTask)
	e.GET("/status/:taskID", taskStatus)

	// Start server
	e.Logger.Fatal(e.Start(":8080"))
}
