from prompts import SYSTEM_PROMPT, PRE_GENERATION_PROMPT
from openai import OpenAI

with open("prompt_learner_docs.txt", "r") as file:
    prompt_learner_docs = file.read()
client = OpenAI()


company = "Attuna"
project = "Prompt Learner"
project_description = "Prompt Learner is designed to make prompts modular. This enables easy tuning, quick experimentation, and frictionless maintenance. A prompt is composed of distinct modules where each module can be optimized & modified both on its own, and as a part of the complete system. Some modules are - The task type The task description A few examples Custom Prompt Technique specific Instructions Instructions for output format."
task = "Use Prompt Learner to engineer prompts for an interesting extreme classification task which is a multi-label classification task with a large number of classes and is related to developers, maybe tagging incoming github issues into different categories."

system_prompt = SYSTEM_PROMPT.format(company=company, project=project, project_description=project_description)
pre_generation_prompt = PRE_GENERATION_PROMPT.format(project=project, task=task)

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[{"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_learner_docs},
            {"role": "assistant", "content": pre_generation_prompt}],
  stream=True,
)

for chunk in response:
    print(chunk.choices[0].delta.content or "", end="", flush=True)


#can ask agent to execute the code
#can send errors back to llm until code executes end to end
#can ask agent to upload a commit to github with the new guide
#can finally ask devrel/eng to review the guide and merge the PR