# 너의 MBTI는. : 텍스트를 통한 MBTI 예측

## 프로젝트 소개

텍스트를 통한 감정 분석 등은 자연어 처리 분야에서 대중적인 주제이지만, 텍스트 작성자의 성향까지 추측하려는 시도는 많지 않다. 비슷한 연구가 있는지 찾아본 결과, 한국어로 된 논문은 단 1개 밖에 없었다.

해당 한국어 논문은 0.2029 의 전체 정확도를 기록하였고, 해외에서 작성된 논문 중 가장 높은 성능을 보인 모델은 0.6659의 정확도를 기록하였다.

한국어 데이터셋으로도 조금 더 나은 성능의 분류모델을 만들 수 있을 것이라 생각하여 해당 프로젝트를 진행하게 되었다.


## 문제 정의


## 데이터 수집 및 전처리


## 데이터 모델링


## 평가


## Folder Structure
```
.
├── data
│   ├── data.csv
│   └── raw_data
│       └── ...
├── model.py
├── models
│   └── model.h5
├── README.md
├── requirements.txt
└── utils
    ├── add_dictionary.csv
    ├── erase_sentence.csv
    ├── erase_word.csv
    ├── exclude.csv
    ├── login.json
    ├── preprocess.py
    └── scrapper.py
```

## Requirements
```
pip install -r requirements.txt
```

TBA
