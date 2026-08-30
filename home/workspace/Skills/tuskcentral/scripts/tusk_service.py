from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import json
import os

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str
    model: str | None = None
    model_id: str | None = None
    option: str | None = None
    tone: str | None = None
    chat_id: str | None = None
    new: bool = False

class ChatResponse(BaseModel):
    text: str
    html: str
    model: str
    model_id: str
    chat_id: str | None
    elapsed_sec: float
    error: str | None

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    args = ["python3", "tusk.py", "chat", req.prompt, "--json"]
    if req.model:
        args.append(f"--model={req.model}")
    if req.model_id:
        args.append(f"--model-id={req.model_id}")
    if req.option:
        args.append(f"--option={req.option}")
    if req.tone:
        args.append(f"--tone={req.tone}")
    if req.chat_id:
        args.append(f"--chat-id={req.chat_id}")
    if req.new:
        args.append("--new")

    try:
        result = subprocess.run(
            args,
            cwd="/home/workspace/Skills/tuskcentral/scripts",
            capture_output=True,
            text=True,
            timeout=130,
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="TuskCentral request timed out")

    if result.returncode != 0:
        raise HTTPException(
            status_code=502,
            detail=f"wrapper_failed: {result.stderr.strip() or result.stdout.strip()}",
        )

    try:
        data = json.loads(result.stdout)
        return ChatResponse(
            text=data.get("text", ""),
            html=data.get("html", ""),
            model=data.get("model", ""),
            model_id=data.get("model_id", ""),
            chat_id=data.get("chat_id"),
            elapsed_sec=data.get("elapsed_sec", 0.0),
            error=data.get("error"),
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail=f"invalid response: {result.stdout[:200]}")

@app.get("/models")
def models():
    result = subprocess.run(
        ["python3", "tusk.py", "models", "--json"],
        cwd="/home/workspace/Skills/tuskcentral/scripts",
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise HTTPException(status_code=502, detail=result.stderr)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail=result.stdout[:200])

@app.get("/health")
def health():
    return {"status": "ok"}
