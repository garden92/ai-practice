# 마케팅 데이터 분석 프로젝트

Jupyter Notebook 기반 마케팅 캠페인 데이터 생성 및 분석 프로젝트

## 빠른 시작

```bash
# 실행
docker-compose up

# 접속
브라우저에서 http://localhost:8888
토큰: mytoken

# 종료
docker-compose down
```

## 사용법

### 데이터 생성

```python
from create_data import create_data

cr = create_data()
df = cr.tmsdata()  # 시계열 마케팅 데이터 생성
```

### 한글 폰트 설정

```python
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False
```

### 기본 시각화

```python
import seaborn as sns

# 산점도
plt.scatter(df['cost'], df['revenue'])

# 상관관계
sns.heatmap(df[['impressions', 'clicks', 'revenue', 'cost']].corr(),
            annot=True, fmt='.2f')
```

## 데이터 항목

- **채널**: Email, SMS, Push, Ads, Search
- **지표**: 노출수, 클릭수, 비용, 전환수, 매출, CTR, CVR, ROAS
- **기간**: 2024-01-01 ~ 2024-06-30 (시계열 추세 및 계절성 반영)

## 구조

```
work/
├── create_data.py      # 데이터 생성 모듈
└── create_data.ipynb   # 분석 노트북
```
