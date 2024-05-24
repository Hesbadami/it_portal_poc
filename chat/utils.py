import openai, json

with open('chat/config.json', 'r') as c:
    config = json.load(c)

api_key = config['open_ai_api']
client = openai.OpenAI(api_key = api_key)

def chat_gpt(messages, max_tokens, presence_penalty, top_p):
    try:
        with open('chat/config.json', 'r') as c:
            config = json.load(c)
        
        response = client.chat.completions.create(
            model=config['gpt_model'],
            messages=messages,  
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            top_p=top_p
        )
        
        return response
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return e  # Return the original text if there's an error