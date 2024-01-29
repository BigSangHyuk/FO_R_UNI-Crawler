from dotenv import load_dotenv
from openai import OpenAI
import os
import re

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def get_ai_response(content):
    
    system_prompt = "너는 대학교 공지사항 내용을 입력받으면 글 안에서 마감기한 혹은 행사 날짜를 찾아서 알려주는 AI야. 만약 입력받은 공지사항 글에서 마감기한이 있으면 마감기한 날짜를, 당일 하루짜리 행사이면 당일 행사 날짜를 XXXX.XX.XX 형식으로 답변해줘. 답변에 불필요한 말이나 한글 없이 XXXX.XX.XX 형식으로만 대답해줘."
    prompt = f"SYSTEM: {system_prompt}\nUSER: {content}\nAI: "
    
    model_engine = "gpt-3.5-turbo-instruct"
    completions = client.completions.create(
            model=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=5,
            stop=None,
            temperature=0.5,
        )
    response = completions.choices[0].text.strip()
    
    date = re.search(r'\d{4}\.\d{2}\.\d{2}', response)
    
    return date.group() if date else ''