from transformers import pipeline

class TranDetector():
    def __init__(self):
        self.model_name = "facebook/nllb-200-3.3B"

    def detection(self, text:str, from_lang:str, to_lang:str):
        # 언어 선택을 좀 더 자유롭게 하기
        #step4
        translator = pipeline('translation', model= self.model_name, device=-1, src_lang=from_lang, tgt_lang=to_lang, max_length=512)

        #step5
        result = translator(text, max_length=512)
        return result[0]['translation_text']
        
