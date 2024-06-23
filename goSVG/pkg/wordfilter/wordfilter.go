package wordfilter

import (
	"math"
	"strings"
)

func WordFilter(
	words []string,
	minLength int,
	maxLength int,
	minOccurrence int,
	stopTypes []string,
) map[string]int {

	// make use of the getStopwords function to get the stopwords
	// based on the stop types provided by the user
	stopwords := getStopwords(stopTypes)

	ignoreList := make(map[string]bool)

	// Populate ignore list based on stop types
	for _, word := range words {
		word = strings.ToLower(word)
		if len(word) < minLength || len(word) > maxLength {
			continue
		}
		if stopwords[word] {
			continue
		}
		if _, found := ignoreList[word]; found {
			continue
		}
		ignoreList[word] = true
	}

	// Count occurrences of filtered words
	for word := range ignoreList {
		if len(word) < minLength || len(word) > maxLength {
			continue
		}
		if _, found := ignoreList[word]; found {
			continue
		}

		ignoreList[word] = true
	}

	// Apply min occurrence filter and logarithmic scaling as int(math.Log2(float64(count)))
	filteredResult := make(map[string]int)

	for word := range ignoreList {
		if ignoreList[word] {
			count := strings.Count(strings.Join(words, " "), word)
			if count >= minOccurrence {
				filteredResult[word] = int(math.Log2(float64(count)))
			}
		}
	}

	return filteredResult
}
