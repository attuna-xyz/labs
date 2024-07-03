import os
from embedchain import App
import pickle

# Replace this with your OpenAI key
os.environ["OPENAI_API_KEY"] = "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"

app = App.from_config(config={
  "app": {
    "config": {
      "id": "my-app",
    }
  }
})
#load list of urls
with open('urls.pkl', 'rb') as f:
    urls = pickle.load(f)
    print(urls)
# add urls to app
for url in urls:
    app.add(f"https://news.ycombinator.com/item?id={url}")

