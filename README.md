# 프로젝트 README

## 개요
이 프로젝트는 서강대 Datavisulization 수업의 팀 프로젝트로 데이터 시각화를 통해 혐오 표현의 추이를 표현했습니다. 프로젝트는 세 명의 팀원과 함께 지행했고 주제는 최근 증가하고 있는 혐오 표현에 대한 분석입니다. 프로젝트는  세가지 형태의 데이터 시각화를 구현했습니다.
1. Clear Communication: 명확하게 알아볼 수 있는 형태
2. Unconventional Charting Type: 직관적인 정보 전달보다는 데이터의 의미를 담아 전달
3. Analog Material Incorporated: 소리, 맛, 촉감 등 아날로그적 형태로 데이터를 표현

## 데이터셋
### 데이터 추출 방법
- 웹 크롤링을 통해 뉴스 댓글 데이터를 수집
- 네이트의 베스트 댓글 시스템을 사용하여 2005년부터 2024년까지의 데이터를 추출

### 데이터 전처리 및 분석
- 뉴스 댓글 데이터를 연도별, 카테고리별로 분류
- 스마일게이트의 혐오 표현 분석 모델을 사용하여 댓글 데이터를 분석
- 각 댓글의 혐오 카테고리를 여성/가족, 남성, 성소수자, 인종/국적, 연령, 지역, 종교, 악플/욕설, Clean으로 분류

## 결과
### 주요 발견 사항
- 혐오 표현의 연도별 증가 추이를 확인
- 각 혐오 표현 카테고리별 비율 분석

### 데이터 시각화
- 파이썬을 활용한 누적 막대 그래프를 통해 연도별 혐오 표현의 비율과 증가 추이를 명확하게 전달
- p5.js를 활용한 글자 시각화로 혐오 표현의 증가 추이를 창의적으로 전달

