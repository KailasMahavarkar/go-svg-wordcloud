package scraper

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"

	"github.com/PuerkitoBio/goquery"
	"golang.org/x/net/html"
)

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
	var globalWordList []string

	var errors []error
	for _, url := range urls {
		text, err := FetchWebsite(url, timeout)

		fmt.Println("text: ", url)

		if err != nil {
			errors = append(errors, err)
			continue
		}

		// Series.[127] -> should be Series -> so replace all special characters with space and split words then take 1st word
		localWords := strings.Fields(text)

		for i := 0; i < len(localWords); i++ {
			globalWordList = append(globalWordList, localWords[i])
		}

		// for i := 0; i < len(localWords); i++ {
		// 	currentWord := localWords[i]
		// 	// replace all non-alphanumeric characters with space
		// 	// split the string into words and trim spaces from each word

		// 	replace := func(r rune) rune {
		// 		if r >= 'a' && r <= 'z' {
		// 			return r
		// 		}
		// 		if r >= 'A' && r <= 'Z' {
		// 			return r
		// 		}
		// 		if r >= '0' && r <= '9' {
		// 			return r
		// 		}
		// 		return ' '
		// 	}

		// 	currentWord = strings.Map(replace, currentWord)

		// 	// split the string by space and take the first word only
		// 	wordList := strings.Fields(currentWord)
		// 	if len(wordList) > 0 {
		// 		wordList = wordList[:1]
		// 	}

		// 	if len(wordList) > 0 {
		// 		globalWordList = append(globalWordList, wordList[0])
		// 	}
		// }

	}
	return globalWordList, errors
}

func MultipleFetchWebsiteAsync(urls []string, timeout time.Duration) ([]string, []error) {
	type result struct {
		text string
		err  error
	}

	resultsCh := make(chan result)
	for _, url := range urls {
		go func(url string) {
			text, err := FetchWebsite(url, timeout)
			resultsCh <- result{text, err}
		}(url)
	}

	var results []string
	var errors []error
	for range urls {
		res := <-resultsCh
		if res.err != nil {
			errors = append(errors, res.err)
		} else {
			results = append(results, res.text)
		}
	}
	return results, errors
}

func ScrapeGoogleLinks(searchTerm string) ([]string, error) {
	url := fmt.Sprintf("https://www.google.com/search?q=%s", searchTerm)
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("HTTP request failed with status code %d", resp.StatusCode)
	}

	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	links := ExtractLinks(string(bodyBytes))
	return links, nil
}

func ExtractLinks(htmlString string) []string {
	var links []string

	z := html.NewTokenizer(strings.NewReader(htmlString))

	for {
		tokenType := z.Next()

		switch {
		case tokenType == html.ErrorToken:
			return links
		case tokenType == html.StartTagToken:
			token := z.Token()
			if token.Data == "a" {
				for _, attr := range token.Attr {
					if attr.Key == "href" {
						// check if it starts with /url?q=
						if strings.HasPrefix(attr.Val, "/url?q=") {
							attr.Val = strings.TrimPrefix(attr.Val, "/url?q=")

							// check if it's a valid URL (starts with http)
							if strings.HasPrefix(attr.Val, "http") {
								fmt.Println(attr)
								links = append(links, attr.Val)
							}

						}
					}
				}
			}
		}
	}
}
