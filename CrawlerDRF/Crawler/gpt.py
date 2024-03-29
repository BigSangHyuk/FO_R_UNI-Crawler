from dotenv import load_dotenv
import openai
import os
import re
import asyncio

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)

async def get_ai_response(content, img_url):
    
    async def make_request_4():
        model_engine = "gpt-4-vision-preview"
        prompt=[
            {"role":"system", "content":[{"type":"text", "text":"너는 대학교 공지사항 내용을 입력받으면 글 안에서 마감기한 혹은 행사 날짜를 찾아서 알려주는 AI야. 만약 입력받은 공지사항 글과 첨부이미지에서 마감기한이 있으면 마감기한 날짜를, 당일 하루짜리 행사이면 당일 행사 날짜를 XXXX.XX.XX 형식으로 답변해줘. 답변에 불필요한 말이나 한글 없이 XXXX.XX.XX 형식으로만 대답해줘."},]},
            {"role":"user", "content":[{"type":"text", "text":content},]},
        ]
        for img in img_url:
            prompt[1]["content"].append({"type":"image_url", "image_url":img})
            
        completions = await asyncio.to_thread(
            client.chat.completions.create,
            model=model_engine,
            messages=prompt,
            max_tokens=500,
        )
        return completions.choices[0].message.content
    
    async def make_request_3():
        model_engine = "gpt-3.5-turbo-instruct"
        system_prompt = "너는 대학교 공지사항 내용을 입력받으면 글 안에서 마감기한 혹은 행사 날짜를 찾아서 알려주는 AI야. 만약 입력받은 공지사항 글에서 마감기한이 있으면 마감기한 날짜를, 당일 하루짜리 행사이면 당일 행사 날짜를 XXXX.XX.XX 형식으로 답변해줘. 답변에 불필요한 말이나 한글 없이 XXXX.XX.XX 형식으로만 대답해줘."
        prompt = f"SYSTEM: {system_prompt}\nUSER: {content}\nAI: "
        completions = await asyncio.to_thread(
            client.completions.create,
            model=model_engine,
            prompt=prompt,
            max_tokens=1000,
            n=5,
            stop=None,
            temperature=0.5,
        )
        return completions.choices[0].text.strip()

    try:
        if img_url:
            try:
                response = await make_request_4()
            except:
                response = await make_request_3()
        else:
            response = await make_request_3()
    except:
        response = ''
    
    date = re.search(r'\d{4}\.\d{2}\.\d{2}', response)
    
    return date.group() if date else ''