from state.state import MemoryAgentState
from prompts.response_prompt import response_prompt
from storage.memory_store import get_memories
from llm import llm

chain = response_prompt | llm

def response(state: MemoryAgentState):
    user_id = state.user_id
    messages = state.messages[-1].content
    saved_memories = get_memories(user_id=user_id)
    response = chain.invoke({
        "memories":saved_memories,
        "user_message":messages
    })

    return {"final_response":response.content}

