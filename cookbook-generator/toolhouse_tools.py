from toolhouse import Toolhouse
from openai import OpenAI


class ToolHouseTools():
    def __init__(self):
        self.client = OpenAI()
        self.MODEL = 'gpt-4o'
        self.th = Toolhouse()
        self.th.set_metadata('timezone', -7)
    
    def call_tools(self, message: str):
        messages = [
                {
                    "role": "user",
                    "content": message,
                }
                ]
        which_tool_to_use = self.client.chat.completions.create(
                    model=self.MODEL,
                    messages=messages,
                    tools=self.th.get_tools(),
                    )
        tool_run = self.th.run_tools(which_tool_to_use)
        #tool output
        return tool_run[1]['content']