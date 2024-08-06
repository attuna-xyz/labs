from fasthtml.common import *
from claudette import *
from develyn_cook import chat_with_agent
# Set up the app, including daisyui and tailwind for the chat component
tlink = Script(src="https://cdn.tailwindcss.com"),
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")
app = FastHTML(hdrs=(tlink, dlink, picolink))

messages = []

# Chat message component, polling if message is still being generated
def ChatMessage(msg):
    try:
        bubble_class = "chat-bubble-primary" if msg['role']=='user' else 'chat-bubble-secondary'
    except:
        bubble_class = "chat-bubble-secondary"
    #bubble_class = "chat-bubble-primary" if msg['role']=='user' else 'chat-bubble-secondary'
    try:
        chat_class = "chat-end" if msg['role']=='user' else 'chat-start'
    except:
        chat_class = "chat-start"
    #chat_class = "chat-end" if msg['role']=='user' else 'chat-start'
    role=None
    try:
        role = msg['role']
    except:
        role = 'assistant'
    return Div(Div(role=role, cls="chat-header"),
               Div(msg['content'], cls=f"chat-bubble {bubble_class}"),
               cls=f"chat {chat_class}")


# The input field for the user message. Also used to clear the 
# input field after sending a message via an OOB swap
def ChatInput():
    return Input(type="text", name='msg', id='msg-input', 
                 placeholder="Type a message", 
                 cls="input input-bordered w-full", hx_swap_oob='true')

# The main screen
@app.route("/")
def get():
    page = Body(H1('On Demand Cookbook Generator for Julep AI'),
                Div(*[ChatMessage(msg) for msg in messages],
                    id="chatlist", cls="chat-box h-[73vh] overflow-y-auto"),
                Form(Group(ChatInput(), Button("Send", cls="btn btn-primary")),
                    hx_post="/", hx_target="#chatlist", hx_swap="beforeend",
                    cls="flex space-x-2 mt-2",
                ), cls="p-4 max-w-lg mx-auto")
    return Title('On Demand Cookbook Generator for Julep AI'), page

# def chatbot_to_code(chatbot_msg):
#     title = "Generated Code"
#     md = Div(f"""### Usage:
# ```python
# {chatbot_msg}
# ```""", cls='marked')
#     return Title(title), Main(H1(title), md, cls='container')

@app.post("/")
def post(msg:str):
    messages.append({"role":"user", "content":msg})
    r=chat_with_agent(msg)#agent_id='3ec7a0fa-8653-4d42-b776-8fcb6ce25c52'
    messages.append({"role":"assistant", "content":r})
    return (ChatMessage(messages[-2]), # The user's message
            ChatMessage(messages[-1]), # The chatbot's response
            ChatInput()) # And clear the input field via an OOB swap

if __name__ == '__main__': uvicorn.run("polling:app", host='0.0.0.0', port=8000, reload=True)
