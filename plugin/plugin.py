import requests
from bs4 import BeautifulSoup

from typing import Literal, List
from typing_extensions import Self

from .message import Message


class Plugin:
    def __init__(self, name: str) -> None:
        self.name = name

    def generateMessage(self) -> dict:
        return {}


class BrowserPlugin(Plugin):
    mode: Literal["browse", "parse"] = "browse"
    url: str

    __google_search_api_key: str

    def __init__(self, mode: Literal["browse", "parse"]) -> None:
        super().__init__(name="browser")
        self.mode = mode

    def setBrowseParameters(self, google_search_api_key: str) -> Self:
        self.__google_search_api_key = google_search_api_key
        return self

    def setParseParameters(self, url: str) -> Self:
        self.url = url
        return self

    def generateMessage(self) -> dict:
        message = Message("user", self.generatePrompt())
        return message.getMessage()

    def generatePrompt(self) -> str:
        prompt: str = ""
        if self.mode == "browse":
            print("browsing mode")
            prompt = "browsing mode"
        elif self.mode == "parse":
            prompt = "Используй в ответе данные из этой веб-страницы: " + self.webpageExtractPlainText()

        return prompt

    # Return plain text content of webpage

    def webpageExtractPlainText(self) -> str:
        # Get HTML soure code of the webpage
        res = requests.get(self.url)

        # Parse the source code using BeatifulSoup
        soup = BeautifulSoup(res.text, 'html.parser')

        # Extract plain text content
        text = soup.get_text()

        return text[0:8000]


class SmmPlugin(Plugin):
    def __init__(self, accent: Literal['vk', 'article', 'header', 'ideas']) -> None:
        super().__init__(name="smm")
        self.accent = accent

    def generateMessage(self) -> dict:
        message = Message("user", self.generatePrompt())
        return message.getMessage()

    def generatePrompt(self) -> str:
        match self.accent:
            case "vk":
                return "Ты профессиональный копирайтер и SMMщик, который фокусируется на соцсети vk."
            case "article":
                return "Ты профессиональный копирайтер, который пишет очень крутые статьи"
            case "header":
                return "Ты профессиональный копирайтер, который делает очень крутые заголовки"
            case "ideas":
                return "Ты профессиональный копирайтер, который помогает в придумывание идей для контента"
        return ""


class TOVPlugin(Plugin):
    def __init__(self, tov: str) -> None:
        super().__init__(name="smm")
        self.tov = tov

    def generateMessage(self) -> dict:
        message = Message("user", self.generatePrompt())
        return message.getMessage()

    def generatePrompt(self) -> str:
        return "При написание контента использую этот TOV: " + self.tov


class ConversationPlugin(Plugin):
    def __init__(self, roles: List[Literal["user", "assistant", "system"]], content: List[str]) -> None:
        super().__init__(name="conversation")

        print(roles)
        print(content)

        messages: List[Message] = []
        for i in range(len(roles)):
            messages.append(Message(roles[i], content[i]))
        
        self.messages = messages

    def generateMessages(self) -> List[dict]:
        messages: List[dict] = []
        for message in self.messages:
            messages.append(message.getMessage())

        return messages
