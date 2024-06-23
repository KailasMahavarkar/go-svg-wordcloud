import requests
import json


def get_svgs(query: str):
    try:
        URL = f'https://api.svgapi.com/v1/Ty5WcDa63E/list/?search={query}&limit=10'
        response = requests.get(URL)
        content = response.text
        return json.loads(content)
    except Exception as e:
        return {}


# {
# 	"term": "apple black",
# 	"count": 6,
# 	"limit": 10,
# 	"start": 0,
# 	"response_time": 0.51138496398926,
# 	"icons": [{
# 		"id": "23820",
# 		"slug": "apple-black-shape",
# 		"title": "Apple black shape",
# 		"url": "https://cdn.svgapi.com/vector/23820/apple-black-shape.svg"
# 	}, {
# 		"id": "105671",
# 		"slug": "apple-black-shape",
# 		"title": "Apple black shape",
# 		"url": "https://cdn.svgapi.com/vector/105671/apple-black-shape.svg"
# 	}, {
# 		"id": "167525",
# 		"slug": "apple-black-fruit-shape",
# 		"title": "Apple black fruit shape",
# 		"url": "https://cdn.svgapi.com/vector/167525/apple-black-fruit-shape.svg"
# 	}, {
# 		"id": "41911",
# 		"slug": "apple-black-silhouette-with-a-leaf",
# 		"title": "Apple black silhouette with a leaf",
# 		"url": "https://cdn.svgapi.com/vector/41911/apple-black-silhouette-with-a-leaf.svg"
# 	}, {
# 		"id": "97893",
# 		"slug": "apple-black-silhouette-with-a-leaf",
# 		"title": "Apple black silhouette with a leaf",
# 		"url": "https://cdn.svgapi.com/vector/97893/apple-black-silhouette-with-a-leaf.svg"
# 	}, {
# 		"id": "87076",
# 		"slug": "apple-black-shape-logo-with-a-bite-hole",
# 		"title": "Apple black shape logo with a bite hole",
# 		"url": "https://cdn.svgapi.com/vector/87076/apple-black-shape-logo-with-a-bite-hole.svg"
# 	}],
# 	"next": null
# }

ans = get_svgs("apple black")
icons = ans.get('icons')

if icons:
    print(icons)
