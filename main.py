from fastapi import FastAPI, HTTPException

app = FastAPI()
from fakenewslogic import is_fake_news; 

# Example usage
text_from_client = ""

@app.post("/check_fake_news")
def check_fake_news(message: dict):
    global text_from_client
    text_from_client = message.get("text", "")
    if not text_from_client:
        raise HTTPException(status_code=400, detail="Text is required in the request.")
    result = is_fake_news(text_from_client)
    return result
