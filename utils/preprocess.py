import pickle
import os
import re
import pandas as pd

INPUT_DATA_PATH = '../data/raw_data/'
OUTPUT_FILE_NAME = '../data/data.csv'


#해당 문자열이 포함된 행을 제거할 문자열 로드
with open('exclude', 'rb') as f:
    exclude = pickle.load(f)

#해당 문자열이 포함된 문장을 제거할 문자열 로드
with open('erase_sentence', 'rb') as f:
    erase_sentence = pickle.load(f)

#제거할 문자열 로드
with open('erase_word', 'rb') as f:
    erase_word = pickle.load(f)


# 여러 개로 나눠서 저장된 데이터 파일을 하나로 통합
def concat_data(): 
    files = [pd.read_csv(INPUT_DATA_PATH + file) for file in sorted(os.listdir(INPUT_DATA_PATH))]
    pd.concat(files).to_csv(OUTPUT_FILE_NAME, index=False)


# 닉네임에 MBTI가 포함되어 있으면 mbti를, 포함되어 있지 않으면 None을 리턴
def contains_mbti(nickname):
    nickname = nickname.upper()
    mbti = set()

    # 닉네임에 포함된 MBTI를 집합에 추가, 한글 표기 시 영어로 변환하여 추가
    for p in personalities:
        if re.search(p, nickname): 
            if p in k_decode: p = k_decode[p]
            mbti.add(p)

    # 닉네임에 1가지의 MBTI가 포함되어 있는 경우만 고려
    if len(mbti) == 1: return list(mbti)[0]
    
    return None


# 작성자 닉네임에 MBTI가 포함된 글 및 게시글만 남기고 나머지는 삭제
def get_mbti_data(filename=OUTPUT_FILE_NAME):
    data = pd.read_csv(filename)
    data['MBTI'] = data['nickname'].copy().apply(contains_mbti)
    data.dropna().to_csv(filename, index=False)


# 전처리
def cleanse(filename=OUTPUT_FILE_NAME, 
            exclude:list=exclude, erase_sentence:list=erase_sentence, erase_word:list=erase_word, regex:str=None):
    data = pd.read_csv(filename)

    #특정 문자열을 포함하는 행을 제거
    if exclude: data = data[~data['contents'].str.contains('|'.join(exclude))]
    
    #특정 문자열을 포함하는 문장을 제거
    if erase_sentence: 
        data['contents'] = data['contents'].copy().apply(
            lambda x: ' '.join([i for i in x.split() if not re.search('|'.join(erase_sentence), i)]))

    #특정 문자열을 제거
    if erase_word: data['contents'] = data['contents'].copy().str.replace('|'.join(erase_word),'')

    #특정 문자열 패턴 제거
    if regex: data['contents'] = data['contents'].copy().str.replace(regex,'',regex=True)

    #저장
    data.to_csv(filename, index=False)


# 작성자 닉네임 별로 게시글 및 댓글을 그룹화
def group_by_user(filename=OUTPUT_FILE_NAME):
    data = pd.read_csv(filename)
    nicknames = data['nickname'].unique()
    contents = {name:'' for name in nicknames}

    for _,row in data.iterrows():
        name, string = row[['nickname','contents']]
        contents[name] += string + ' '

    pd.DataFrame(contents.items(), columns=['nickname', 'contents']).merge(
        data[['nickname','MBTI']].drop_duplicates('nickname'), on='nickname').to_csv(filename, index=False)


# MBTI 리스트
personalities = [
    'ISFJ','ISFP','ISTJ','ISTP',
    'INFJ','INFP','INTJ','INTP',
    'ESFJ','ESFP','ESTJ','ESTP',
    'ENFJ','ENFP','ENTJ','ENTP'
]

# 한글로 표기된 MBTI도 분류하기 위해 데이터 추가
k_translate = {
    'IS':'잇', 'IN':'인', 'ES':'엣', 'EN':'엔',
    'FJ':'프제', 'FP':'프피', 'TJ':'티제', 'TP':'팁'
    }

personalities.extend(
    [k_translate[p[:2]]+k_translate[p[2:]] for p in personalities]
)

# 한글로 표기된 MBTI를 영어로 변환하기 위한 사전
k_decode = {personalities[16+i]:personalities[i] for i in range(16)}


if __name__ == '__main__':
    concat_data()
    get_mbti_data()
    cleanse()
    group_by_user()
