package scraper

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"github.com/PuerkitoBio/goquery"
)

// FetchWebsite fetches the website content given a URL and a timeout
func FetchWebsite(url string, timeout time.Duration) (string, error) {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		return "", fmt.Errorf("failed to create request: %v", err)
	}

	client := http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return "", fmt.Errorf("failed to fetch URL %s: %v", url, err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("unexpected status code %d for URL %s", resp.StatusCode, url)
	}

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		return "", fmt.Errorf("failed to parse HTML from %s: %v", url, err)
	}

	var text string
	doc.Find("p").Each(func(i int, s *goquery.Selection) {
		text += s.Text() + "\n"
	})

	return text, nil
}

func MultipleFetchWebsite(urls []string, timeout time.Duration) ([]string, []error) {
	var results []string
	var errors []error
	for _, url := range urls {
		text, err := FetchWebsite(url, timeout)
		if err != nil {
			errors = append(errors, err)
		} else {
			results = append(results, text)
		}
	}
	return results, errors
}
