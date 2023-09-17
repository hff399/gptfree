from typing import Literal, List, Annotated

from fastapi import FastAPI, Body, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import StreamingResponse

from pydantic import BaseModel

import g4f

from plugin.plugin import Plugin, BrowserPlugin, SmmPlugin, ConversationPlugin, TOVPlugin
from plugin.message import Message


api_keys = [
    'API_KEY'
]  # This is encrypted in the database

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token")  # use token authentication


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "example"}


class QueryModel(BaseModel):
    query: str
    plugins: List[Literal["browser", "smm", "tov", "conversation"]] | None = None
    url: str | None = None
    tov: str | None = None
    roles: List[Literal["user", "assistant", "system"]]
    accent: Literal['vk', 'article', 'header', 'ideas']
    content: List[str]

@app.post("/ask", dependencies=[Depends(api_key_auth)])
async def ask(q: QueryModel):
    messages = []

    if q.plugins:
        for plugin in q.plugins:
            match plugin:
                case "browser":
                    messages.append(BrowserPlugin("parse").setParseParameters(str(q.url)).generateMessage())
                case "smm":
                    messages.append(SmmPlugin(q.accent).generateMessage())
                case "tov":
                    messages.append(TOVPlugin(str(q.tov)).generateMessage())
                case "conversation":
                    conversationMessages = ConversationPlugin(q.roles, q.content).generateMessages()
                    
                    messages = messages + conversationMessages

    prompt = Message("user", q.query)
    messages.append(prompt.getMessage())

    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
        provider=g4f.Provider.DeepAi
    )

    def messages_generator():
        for message in response:
            # TODO: Remove this debug print
            print(message, end='')
            yield str.encode(message)

    return StreamingResponse(messages_generator(), media_type="text/event-stream")
