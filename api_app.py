from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from usecase.image_usecase import *
from usecase.text_usecase import *
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

# .env 파일의 환경 변수 불러오기
load_dotenv()

# 환경 변수 사용하기
host = os.getenv('FRONT_HOST', 'localhost')
port = os.getenv('FFRONT_PORT', 3000)

print(host)
print(port)
text_usecase = TextUsecase()
image_usecase = ImageUsecase()
app = FastAPI()

class TextRequest(BaseModel):
    text: str

class ImageRequest(BaseModel):
    from_lang: int
    to_lang: int
    is_summary: bool
    is_speech: bool

# 허용할 도메인 목록 설정
origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://{0}:80".format(host),
    "http://{0}:3000".format(host),
    "http://{0}".format(host),
    "https://127.0.0.1:3000",
    "https://{0}:80".format(host),
    "https://{0}:3000".format(host),
    "https://{0}:{1}".format(host, port),
    "https://{0}".format(host)
]


# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # 허용할 도메인들
    allow_credentials=True,       # 쿠키 등의 자격 증명 허용 여부
    allow_methods=["*"],          # 모든 HTTP 메소드 허용
    allow_headers=["*"],          # 모든 HTTP 헤더 허용
)

# 파일은 별도로 받고
@app.post("/images")
async def create_speech(file: UploadFile,  request: ImageRequest = Depends()):
    
    contents = await file.read()
    # ImageUsecase의 excute 메서드에 JSON 데이터를 전달
    speech_result = image_usecase.excute(
        contents, 
        request.from_lang, 
        request.to_lang, 
        request.is_summary, 
        request.is_speech
    )
    
    return {
        "result": speech_result
    }

@app.post("/text")
async def create_text(request: TextRequest, from_lang:int, to_lang:int, is_summary:bool, is_speech:bool):
    text_jonson_data = jsonable_encoder(request)
    tran_result = text_usecase.excute(text_jonson_data['text'], from_lang, to_lang, is_summary, is_speech)

    return {
        "result" : tran_result
    }