
# Project Information
COMPANY = "Langchain"
PROJECT = "Langgraph"
PROJECT_DESCRIPTION = """
Prompt Learner is designed to make prompts modular. This enables easy tuning, quick experimentation, 
and frictionless maintenance. A prompt is composed of distinct modules where each module can be 
optimized & modified both on its own, and as a part of the complete system. Some modules are - 
The task type The task description A few examples Custom Prompt Technique specific Instructions 
Instructions for output format.
"""

# Document URLs
DOCUMENT_URL = "https://python.langchain.com/v0.2/docs/concepts/#langchain-expression-language-lcel"
# Retry Configuration
MAX_RETRIES = 3
flag = "do not reflect"

# Agent Configuration
AGENT_NAME = "Develyn"
AGENT_MODEL = "gpt-4o"
AGENT_SITUATION = "You are Develyn. You are an expert Developer Relations Engineer and you create high quality cookbooks and tutorials for OSS projects."

# Task Configuration
TASK = """
Use Prompt Learner to engineer prompts for an interesting extreme classification task which is a 
multi-label classification task with a large number of classes and is related to developers, maybe 
tagging incoming github issues into different categories.
"""

# File Configuration
OUTPUT_FILE = "extreme_classification_github_demo.py"
BRANCH_NAME = "add-new-guide-julep"