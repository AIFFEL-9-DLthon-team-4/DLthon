
from soynlp.normalizer import *
import re

# label
id2label = {0: "협박", 1: "갈취", 2: "직장내괴롭힘", 3: "기타괴롭힘", 4: "일반대화"}
label2id = {"협박": 0, "갈취": 1, "직장내괴롭힘": 2, "기타괴롭힘": 3, "일반대화": 4}
num_labels = 5



# 불필요한 문자열 제거 함수
def preprocess_sentence(sentence):
    sentence = sentence.lower().strip()

    # 구두점과의 거리를 만듭니다 (예: "I am a student." -> "I am a student .")
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)

    # 공백이 두 개 이상일 때 하나로 치환
    sentence = re.sub(r'[" "]+', " ", sentence)

    # 한글, 영어, 구두점(.,?!), 숫자, 줄바꿈(\n)을 제외한 모든 문자를 공백으로 대체
    sentence = re.sub(r'[^a-zA-Z0-9.,?!가-힣\n]', ' ', sentence)

    sentence = sentence.strip()
    return sentence


# 자음 모음 문자 정규화 - 'sonlp' 사용
def normalize_korean_text(text):
    # \n 문자를 특별한 토큰으로 변환
    text = text.replace('\n', '<newline>')
    
    # 연속된 자음/모음 제거
    text = repeat_normalize(text, num_repeats=2)
    
    # <newline>을 다시 \n으로 변환
    text = text.replace('<newline>', '\n')
    
    return text


# 불용어 제거 함수
def remove_stopwords(text, stopwords):
    # 줄바꿈을 기준으로 문장을 나누기
    sentences = text.split('\n')
    
    # 각 문장에서 불용어 제거
    filtered_sentences = []
    for sentence in sentences:
        tokens = sentence.split()  # 공백을 기준으로 토큰화
        filtered_tokens = [token for token in tokens if token not in stopwords]
        filtered_sentences.append(' '.join(filtered_tokens))
    
    # 줄바꿈으로 다시 연결
    return '\n'.join(filtered_sentences)

