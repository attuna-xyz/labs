from substrate import Substrate, ComputeText, sb, Box
import os
API_KEY = os.getenv('API_KEY')
substrate = Substrate(api_key=API_KEY)

story = ComputeText(prompt="tell me a story")
summary = ComputeText(prompt=sb.concat("summarize this story in one sentence: ", story.future.text))
response = substrate.run(summary)
summary_out = response.get(summary)
print(summary_out.text)

box = Box(
  value={
    "story": story.future.text,
    "summary": summary.future.text,
  }
)
res = substrate.run(box)
print("final res,",res)