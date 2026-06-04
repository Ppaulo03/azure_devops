from fastapi import FastAPI, Request
import uvicorn
from notifier import send_whatsapp_message

app = FastAPI()

@app.post("/webhook/pr")
async def pr_webhook(request: Request):
    payload = await request.json()
    resource = payload.get("resource", {})
    message_text = payload.get("message", {}).get("text", "Nova atualização de PR")
    
    pr_id = resource.get("pullRequestId", "?")
    status = resource.get("status", "?")
    title = resource.get("title", "Sem título")
    created_by = resource.get("createdBy", {}).get("displayName", "Desconhecido")
    
    msg = (
        f"🚀 *Pull Request Atualizado*\n"
        f"ID: #{pr_id}\n"
        f"Título: {title}\n"
        f"Status: *{status.upper()}*\n"
        f"Autor: {created_by}\n"
        f"\n_{message_text}_"
    )
    
    await send_whatsapp_message(msg)
    return {"status": "ok"}

@app.post("/webhook/build")
async def build_webhook(request: Request):
    payload = await request.json()
    resource = payload.get("resource", {})
    message_text = payload.get("message", {}).get("text", "Status da Build")
    
    build_number = resource.get("buildNumber", "?")
    status = resource.get("status", "?")
    result = resource.get("result", "?") 
    definition_name = resource.get("definition", {}).get("name", "Pipeline")
    
    emoji = "✅" if result == "succeeded" else "❌" if result == "failed" else "⏳"
    
    msg = (
        f"{emoji} *Build Finalizada*\n"
        f"Pipeline: {definition_name}\n"
        f"Build: #{build_number}\n"
        f"Status: {status}\n"
        f"Resultado: *{result.upper()}*\n"
        f"\n_{message_text}_"
    )
    
    await send_whatsapp_message(msg)
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)