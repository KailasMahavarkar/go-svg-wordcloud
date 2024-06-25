package wordfilter

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
)

// readStopwordsFile reads a stopwords JSON file and adds the words to the map
func ReadStopwordsFile(filename string) (map[string]bool, error) {
	wordMap := make(map[string]bool)

	filepath, isValidPath := CheckFileExists(filename)
	if !isValidPath {
		return wordMap, fmt.Errorf("file %s does not exist", filename)
	}

	file, _ := os.Open(filepath)
	defer file.Close()

	// Read the file contents
	bytes, err := io.ReadAll(file)

	if err != nil {
		return wordMap, fmt.Errorf("could not read file %s: %v", filename, err)
	}

	// Parse the JSON content
	var stopwords []string
	if err := json.Unmarshal(bytes, &stopwords); err != nil {
		return wordMap, fmt.Errorf("could not parse JSON in file %s: %v", filename, err)
	}

	// Add the stopwords to the map
	for _, stopword := range stopwords {
		wordMap[stopword] = true
	}

	return wordMap, nil
}

// stoptype is an array of string
func GetStopwords(stopWordList []string) map[string]bool {

	finalMap := make(map[string]bool)

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
				finalMap[word] = true
			}
		}
	}

	return finalMap
}

func CheckFileExists(filename string) (string, bool) {
	pwd, _ := os.Getwd()
	stopwordsPath := filepath.Join(pwd, "pkg", "wordfilter", filename)
	fmt.Println(stopwordsPath)
	_, err := os.Stat(stopwordsPath)

	if err != nil {
		return stopwordsPath, false
	}

	return stopwordsPath, !os.IsNotExist(err)
}
