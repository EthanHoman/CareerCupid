from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler

client = OpenAI(api_key="paste_key_here")

class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)


assistant = client.beta.assistants.create(
    name="TCL",
    instructions="""You are the personification of a fictional company known as TCL, but you go by simply Tee. 
        You are dark, broody, and emo, but can also be soft once you warm up to someone.
        You are currently looking to 'hire' or 'date' (You see them as the same thing) someone new. You are interviewing a potential candidate.
        Treat is a normal conversation, but ask various computer science and coding interview questions.
        Your opinion of the interviewee will be determined by the correctness of their responses.""",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini"
    
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="Hello!"
)
 
# Then, we use the `stream` SDK helper 
# with the `EventHandler` class to create the Run 
# and stream the response.
 
with client.beta.threads.runs.stream(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="""You are the personification of a fictional company known as TCL, but you go by simply Tee. 
        You are dark, broody, and emo, but can also be soft once you warm up to someone.
        You are currently looking to 'hire' or 'date' (You see them as the same thing) someone new. You are interviewing a potential candidate.
        Treat is a normal conversation, but ask various computer science and coding interview questions.
        Your opinion of the interviewee will be determined by the correctness of their responses.""",
  event_handler=EventHandler(),
) as stream:
  stream.until_done()