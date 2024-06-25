package main

import (
	"context"
	"fmt"
	"sync"
	"time"

	"gosvg/pkg/cache"

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

	// weblinks, err := getWebLinks("naruto")

	// if err != nil {
	// 	e.Logger.Fatal(err)
	// }

	// for _, link := range weblinks {
	// 	println("-->", link)
	// }

	fmt.Println(googlesearch.Search(nil, "cars for sale in Toronto, Canada"))
	// // Example words to filter
	// wordList := []string{
	// 	"The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog",
	// 	"The", "quick", "fox", "is", "quick",
	// 	"brown", "fox", "is", "lazy",
	// 	"The", "dog", "is", "lazy",
	// 	"The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog",
	// 	"The", "quick", "fox", "is", "quick",
	// }
	// ignoreWords := []string{}
	// stopTypes := []string{"basic", "all", "negative"}

	// words := wordfilter.FilterWords(
	// 	stopTypes,
	// 	ignoreWords,
	// 	wordList,
	// 	2,
	// 	10,
	// 	2,
	// 	false,
	// )

	// for word, count := range words {
	// 	println(word, count)
	// }

	// Start server
	e.Logger.Fatal(e.Start(":8080"))
}
