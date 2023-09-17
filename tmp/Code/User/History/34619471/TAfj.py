import g4f
from g4f.Provider import (
    Acytoo,
    Aichat,
    Ails,
    Bard,
    Bing,
    ChatgptAi,
    ChatgptLogin,
    DeepAi,
    EasyChat,
    Equing,
    GetGpt,
    H2o,
    HuggingChat,
    Opchatgpts,
    OpenAssistant,
    OpenaiChat,
    Raycast,
    Theb,
    Vercel,
    Wewordle,
    Wuguokai,
    You,
    Yqcloud
)


# print(g4f.Provider.Bard.params)  # supported args

# Automatic selection of provider

# streamed completion
response = g4f.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Напиши пост в vk, про AI"}],
    stream=True,
    provider=DeepAi
)

for message in response:
    print(message, flush=True, end='')

# normal response
# response = g4f.ChatCompletion.create(
#     model=g4f.models.gpt_4,
#     messages=[{"role": "user", "content": "hi"}],
# )  # alterative model setting

# print(response)


# # Set with provider
# response = g4f.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     provider=g4f.Provider.DeepAi,
#     messages=[{"role": "user", "content": "Hello world"}],
#     stream=True,
# )

# for message in response:
#     print(message)