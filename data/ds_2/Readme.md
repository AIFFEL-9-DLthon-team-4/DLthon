## DS_1  정규 표현식을 다양하게 시도해 보기





## 일반 데이터 추가

일반 데이터 4000개로 설정 -> 추후 더 필요하면 추가 할 예정





## 데이터 전처리


구두점과의 거리를 만듬

공백이 두 개 이상일 때 하나로 치환

한글, 영어, 구두점(.,?!), 숫자, 줄바꿈(\n)을 제외한 모든 문자를 공백으로 대체

줄바꿈을 포함한 여러 공백을 하나의 공백으로 치환



## 정규화


일반 데이터셋에 있는 ㅋㅋㅋㅋㅋ 같이 자음 모음 같은 경우 2개로 줄임, 자음 모음만  상태



## 불용어 제거

불용어 리스트 590개를 통해 제거



## 형태소 분석

조사인 단어들만  제거한 상태 





## 사용 함수

## \n을 포함한 불필요한 문자 제거 전처리 함수

```

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




```


## 연속되어 나오는 자음 모음를 2글자로 줄이는 정규화 함수

```

def normalize_korean_text(text):
    # \n 문자를 특별한 토큰으로 변환
    text = text.replace('\n', '<newline>')

    # 연속된 자음/모음 제거
    text = repeat_normalize(text, num_repeats=2)

    # <newline>을 다시 \n으로 변환
    text = text.replace('<newline>', '\n')

    return text

```

## 불용어 제거 함수

```

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

```

## 형태소 분석하기 전 \n token을 newline으로 지정

```

def preserve_newlines(text):
    return text.replace('\n', '__NEWLINE__')

def restore_newlines(pos_tags):
    return [(word.replace('__NEWLINE__', '\n'), tag) for word, tag in pos_tags]

```

```

def retain_newline_only(pos_tags):
    # '__'를 제거하고 'NEWLINE'을 '\n'으로 치환
    tokens = ['\n' if word == 'NEWLINE' else word for word, tag in pos_tags if word != '__']
    return tokens  # 토큰 리스트를 반환

```




## 수정 사항

 단순히 train 데이터 셋만 보고 화자의 위치가 \n으로 이루어져 있어서 이 문자열이 필요한 줄 알아서 마지막 결과물에도 \n을 포함시켰지만 test 데이터셋에서는 .,?!이러한 문자들로 화자를 구분하여 \n을 제거해야 된다.
 


## 추가로 진행 해야 되는 상황


1. 특수문자 정규화 부분 고려


2. 형태소 분석한 token들에서 문맥에 맞는 새로운 dictiionaly 추가, -> 이름 같은경우 준, 하야 이런식으로 token이 분리되는 현상이 발생함


3.  다른 형태소 분석 도구도 사용해보기 (khai, Komoran, Kkma, Hannanum)



