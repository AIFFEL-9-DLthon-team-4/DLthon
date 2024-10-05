



## \n 없는 일반 데이터 없는 상태인 train 데이터 셋 전처리


## 사용 함수

1. preprocess_sentence 함수 적용

```
def preprocess_sentence(sentence):
    sentence = sentence.lower().strip()

    # 구두점과의 거리를 만듭니다 (예: "I am a student." -> "I am a student .")
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)

    # 공백이 두 개 이상일 때 하나로 치환
    sentence = re.sub(r'[" "]+', " ", sentence)

    # 한글, 영어, 구두점(.,?!), 숫자을제외한 모든 문자를 공백으로 대체
    sentence = re.sub(r'[^a-zA-Z0-9.,?!가-힣]', ' ', sentence)

    sentence = sentence.strip()
    return sentence

```



2. Label Encoding

```

from sklearn.preprocessing import LabelEncoder

# LabelEncoder 객체 생성
le = LabelEncoder()

# 'class' 열의 값을 정수로 변환
train_df['label'] = le.fit_transform(train_df['class'])

# 'processed_conversation' 열과 'label' 열만 남기고 나머지 열 삭제
train_df = train_df[['processed_conversation', 'label']]

# 열 이름 변경
train_df = train_df.rename(columns={'processed_conversation': 'text'})

# 결과 출력
print(train_df.head())


```



2. konlpy를 통해 형태소 분석

```
## konlpy를 통해 형태소 분석

train_df['pos'] = train_df['text'].apply(lambda x: okt.morphs(x))

```

3. remove_josa 함수를 통해 조사 제거

```

def remove_josa(pos_tags):

  new_pos_tags = []
  for word, tag in pos_tags:
    if tag != 'Josa':
      new_pos_tags.append((word, tag))
  return new_pos_tags


train_df['filtered_pos'] = train_df['pos'].apply(remove_josa)

```



## konlpy  형태소 분석

konlpy를 통해 나온 조사 같은 경우 없어도 문맥의 흐름에 영향을 주지 않을거 같아 제거


## label encoding

{0: '갈취 대화', 1: '기타 괴롭힘 대화', 2: '직장 내 괴롭힘 대화', 3: '협박 대화'}





