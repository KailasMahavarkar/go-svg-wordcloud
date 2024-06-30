package main

import (
	"context"
	"fmt"
	"sync"
	"time"

	"gosvg/pkg/cache"
	"gosvg/pkg/scraper"

	"github.com/labstack/echo/v4"

	googlesearch "github.com/rocketlaunchr/google-search"
)

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

func getWebLinks(searchTerm string) ([]string, error) {
	ctx := context.Background()
	results, err := googlesearch.Search(ctx, searchTerm, googlesearch.SearchOptions{
		Limit:     10,
		OverLimit: false,
	})
	if err != nil {
		return nil, err
	}

	var urls []string
	for _, result := range results {
		urls = append(urls, result.URL)
	}

	return urls, nil
}

func main() {
	e := echo.New()
	e.HideBanner = true
	e.HidePort = true

	weblinks, _ := scraper.ScrapeGoogleLinks("naruto")

	// if len(weblinks) == 0 {
	// 	fmt.Println("No links found")
	// }

	for count, link := range weblinks {
		fmt.Println(count, link)
	}

	// words, _ := scraper.MultipleFetchWebsite(weblinks, 3*time.Second)

	// for word, count := range words {
	// 	fmt.Println(word, count)
	// }

	// // var filteredWords *orderedmap.OrderedMap[string, int]
	// filteredWords := wordfilter.FilterWords(
	// 	[]string{"basic", "all", "negative"},
	// 	[]string{},
	// 	words,
	// 	2,
	// 	10,
	// 	2,
	// 	false,
	// )

	// for pair := filteredWords.Oldest(); pair != nil; pair = pair.Next() {
	// 	fmt.Printf("%s: %d\n", pair.Key, pair.Value)
	// }

	// for word, count := range words {
	// 	println(word, count)
	// }

	// Start server
	fmt.Println("Server started at http://localhost:8080")
	e.Logger.Fatal(e.Start(":8080"))
}
