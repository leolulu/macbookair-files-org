from revChatGPT.V3 import Chatbot
chatbot = Chatbot(api_key="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",proxy='http://127.0.0.1:10809')


with open('input.txt','r',encoding='utf-8') as f:
    content = f.read()

content = content[:9000]

content += '\n\n-------------------------\n\n'

content += '请以列表形式概括上面文章的内容'

print(content,'\n\n\n')

for data in chatbot.ask(content):
    print(data, end="", flush=True)

print('\n\n')