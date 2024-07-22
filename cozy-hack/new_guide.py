# Cell 1: Import necessary libraries 
from prompt_learner.tasks.classification import ClassificationTask
from prompt_learner.examples.example import Example
from prompt_learner.prompts.prompt import Prompt
from prompt_learner.prompts.cot import CoT
from prompt_learner.templates.markdown import MarkdownTemplate
from prompt_learner.selectors.random_sampler import RandomSampler
from prompt_learner.evals.metrics.accuracy import Accuracy

# Cell 2: Define the classification task for tagging GitHub issues
task_description = "Classify incoming GitHub issues into various categories."
allowed_labels = ["bug", "enhancement", "question", "documentation", "duplicate", "invalid", "wontfix"]
classification_task = ClassificationTask(description=task_description, allowed_labels=allowed_labels)

# Cell 3: Add example issues to the classification task
classification_task.add_example(Example(text="The app crashes on startup.", label="bug"))
classification_task.add_example(Example(text="Please add a dark mode feature.", label="enhancement"))
classification_task.add_example(Example(text="How do I install the package?", label="question"))
classification_task.add_example(Example(text="This documentation is outdated.", label="documentation"))
classification_task.add_example(Example(text="Issue #123 is a duplicate of this issue.", label="duplicate"))
classification_task.add_example(Example(text="This report does not describe a real issue.", label="invalid"))
classification_task.add_example(Example(text="I don't want you to work on this anymore.", label="wontfix"))

# Cell 4: Create a Markdown template for the prompt
template = MarkdownTemplate(task=classification_task)

# Cell 5: Select examples using a random sampler
sampler = RandomSampler(num_samples=3, task=classification_task)
sampler.select_examples()

# Cell 6: Assemble the prompt using CoT
gpt_prompt = CoT(template=template)
gpt_prompt.assemble_prompt()
print(gpt_prompt.prompt)  # Display the assembled prompt

# Cell 7: Compute accuracy on the classification task
acc, num_total_samplers = Accuracy(classification_task).compute(gpt_prompt, OpenAI())
print("Validation accuracy: ", acc, " with ", num_total_samplers, " eval samples")

# Cell 8: Add more example issues for testing
classification_task.add_example(Example(text="Add a feature to support user-defined shortcuts.", label="enhancement"))
classification_task.add_example(Example(text="I don't understand how to use this function.", label="question"))

# Cell 9: Reassemble the prompt with the new examples
sampler = RandomSampler(num_samples=3, task=classification_task)
sampler.select_examples()

gpt_prompt = CoT(template=template)
gpt_prompt.assemble_prompt()
print(gpt_prompt.prompt)  # Display the reassembled prompt

# Cell 10: Compute test accuracy
acc, num_total_samplers = Accuracy(classification_task).compute(gpt_prompt, OpenAI(), test=True)
print("Test accuracy: ", acc, " with ", num_total_samplers, " eval samples")

# Cell 11: Add inference for a new issue to classify
gpt_prompt.add_inference("The sorting function does not work as expected.")
answer = classification_task.predict(OpenAI(), gpt_prompt.prompt)
print("Predicted label for new issue:", answer)