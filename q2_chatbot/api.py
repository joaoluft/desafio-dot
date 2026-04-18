from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from graph import build_graph
from nodes import AgentState

sessions: dict[str, AgentState] = {}

# grafo instanciado uma vez no startup do módulo
graph = build_graph()

app = FastAPI(title="Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    state = sessions.get(req.session_id) or {"messages": [], "question": ""}

    state["question"] = req.message
    state["messages"] = state["messages"] + [HumanMessage(content=req.message)]

    result = graph.invoke(state)
    sessions[req.session_id] = result

    return ChatResponse(answer=result["messages"][-1].content)


@app.delete("/chat/{session_id}")
async def clear_session(session_id: str):
    sessions.pop(session_id, None)
    return {"status": "ok"}


@app.get("/health")
async def health():
    return {"status": "ok"}
