AGI House July 13

[] Use Attuna Tagging APIs
[] Use Langgraph
[] Think of an interesting data source (whatsapp business, discord)
[] Inbound from data source, categorize, and then given tag and inbound ask agent to perform a set of actions
[] actually attuna can be an agent
[] it uses tagger apis for transform layer
[] and then has tools for the action layer (maybe its an overkill)


[] now make it agent
[] add another bot that replies based on tag
[] also show hitl, can i reply using my own profile too automated?
[] migrate attuna internal to together
[] tag a dev if its a dev related message
[] tag a sales person if sales related
[] use llamaindex discord messages as example
[] add_tag can optionally send whom to notify if tag is detected by doing an at on them
[] add_tag has an action param, if notify, then give at of person, if generate - then send tag
and message to llm and ask to respond
[] generate can use tool calling to fetch info from docs and then respond, an agent can come in here
[] agent can actually be given choice to either notify or generate if user chooses not to provide it explicitly

