import os
from embedchain import App

os.environ['OPENAI_API_KEY'] = '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'

app2 = App.from_config(config={
  "app": {
    "config": {
      # this will persist and load data from app1 session
      "id": "my-app",
    }
  }
})

#allow user to query the app from cli
while(True):
    user_query = input("What would you like to search for? ")
    response = app2.query(user_query)
    print(response)