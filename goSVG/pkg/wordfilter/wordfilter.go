package wordfilter

import (
	"fmt"
	"github.com/wk8/go-ordered-map/v2"
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
) *orderedmap.OrderedMap[string, int] {
	finalStopwordsMap := make(map[string]bool)
	ignoreMap := make(map[string]bool)

	om := orderedmap.New[string, int]()

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

	// iterate through the wordList and check if the word is in the tempMap
	// if it is in the tempMap, print the word
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
			// get previous count of the word
			// if the word is not in the map, the count will be 0
			count, _ := om.Get(word)

			// increment the count of the word by 1
			om.Set(word, count+1)
		}
	}

	// check if the word occurs more than minOccurrence times
	// for word, count := range tempMap {
	// 	if count < minOccurrence {
	// 		delete(tempMap, word)
	// 	} else {
	// 		if shouldNormalize {
	// 			tempMap[word] = int(math.Log2(float64(count)))
	// 		}
	// 	}
	// }

	return om
}
