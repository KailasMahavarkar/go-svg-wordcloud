package wordfilter

import (
	"fmt"
	"math"
	"strings"
)

func FilterWords(
	stopWordList []string,
	ignoreList []string,
	wordList []string,
	minLength int,
	maxLength int,
	minOccurrence int,
	shouldNormalize bool,
) map[string]int {
	finalStopwordsMap := make(map[string]bool)
	ignoreMap := make(map[string]bool)
	finalMap := make(map[string]int)

	for _, word := range ignoreList {
		ignoreMap[word] = true
	}

	stopBasic, err := ReadStopwordsFile("./stopwords/stopwords_basic.json")
	if err != nil {
		fmt.Println(err)
	}

	stopAll, err := ReadStopwordsFile("./stopwords/stopwords_all.json")
	if err != nil {
		fmt.Println(err)
	}

	stopNegative, err := ReadStopwordsFile("./stopwords/stopwords_negative.json")
	if err != nil {
		fmt.Println(err)
	}

	stopMaps := map[string]map[string]bool{
		"basic":    stopBasic,
		"all":      stopAll,
		"negative": stopNegative,
	}

	for _, stopType := range stopWordList {
		if stopMap, ok := stopMaps[stopType]; ok {
			for word := range stopMap {
				finalStopwordsMap[word] = true
			}
		}
	}

	// iterate through the wordList and check if the word is in the finalMap
	// if it is in the finalMap, print the word
	for _, word := range wordList {
		// convert the word to lowercase
		word = strings.ToLower(word)

		// trim any whitespace from the word
		word = strings.TrimSpace(word)

		// allow only ascii characters
		word = strings.Map(func(r rune) rune {
			if r > 31 && r < 127 {
				return r
			}
			return -1
		}, word)

		if len(word) < minLength || len(word) > maxLength {
			continue
		}

		if _, found := finalStopwordsMap[word]; found {
			continue
		} else {
			finalMap[word]++
		}
	}

	// check if the word occurs more than minOccurrence times
	for word, count := range finalMap {
		if count < minOccurrence {
			delete(finalMap, word)
		} else {
			if shouldNormalize {
				finalMap[word] = int(math.Log2(float64(count)))
			}
		}
	}

	return finalMap
}
