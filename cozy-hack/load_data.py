import json
with open('substrate_guides.json', 'r') as file:
    data = json.load(file)
print(len(data))
print(data[0]['content'])
all_docs = ""
for doc in data:
    all_docs += doc['content']
with open('substrate_docs_clean.txt', 'w') as file:
    file.write(all_docs)