import requests
import pickle

def fetch_stories():
    # Fetch the latest stories; you can change this to `newstories` or `beststories`
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    response = requests.get(url)
    story_ids = response.json()
    return story_ids

def fetch_story_details(story_id):
    # Fetch details of a specific story
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
    response = requests.get(url)
    story_details = response.json()
    return story_details

def search_stories(keywords):
    # Fetch IDs of the latest stories
    story_ids = fetch_stories()
    filtered_urls = []

    # Check each story for the keyword in its title
    for story_id in story_ids[:100]:  # Limit to the first 100 stories for brevity
        details = fetch_story_details(story_id)
        if details and 'title' in details:
            for keyword in keywords:
                if keyword.lower() in details['title'].lower():
                    filtered_urls.append(details['id'])
                    break

    return filtered_urls

# Example usage
keywords = ["llm","agents","evals","rag"]  # Specify your keyword here
urls = search_stories(keywords)
#save list of urls as a pickle , file may not exist
with open('urls.pkl', 'wb') as f:
    pickle.dump(urls, f)

