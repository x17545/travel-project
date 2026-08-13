# AI 여행 추천 CLI 프로그램

날짜를 입력하면 Gemini API를 이용하여 여행지를 추천하고,  
추천된 도시를 기준으로 Kakao Local API를 이용해 맛집을 검색한 뒤  
최종 여행 리포트를 Markdown 파일로 저장하는 CLI 기반 Python 프로그램입니다.

---

## 1. 프로그램 개요

사용자가 여행 날짜를 입력하면 다음과 같은 순서로 여행 정보를 생성합니다.

1. 사용자가 여행 날짜를 입력합니다.
2. Gemini API를 이용하여 여행지를 추천받습니다.
3. Gemini의 응답을 JSON 형식으로 파싱합니다.
4. 추천된 도시를 Kakao Local API에 전달합니다.
5. 해당 도시의 맛집 5곳을 검색합니다.
6. 1차 여행 추천 결과와 맛집 정보를 이용하여 최종 여행 리포트를 생성합니다.
7. 원본 JSON 데이터와 최종 Markdown 리포트를 `results/` 폴더에 저장합니다.

---

## 2. 주요 기능

- `argparse`를 이용한 CLI 인터페이스
- `-date "YYYY-MM-DD"` 형식의 날짜 입력
- 날짜 형식 검증
- Google Gemini API를 이용한 여행지 추천
- Gemini 응답의 JSON 구조화 및 파싱
- JSON 파싱 실패 시 1회 재시도
- Kakao Local API를 이용한 맛집 검색
- 추천 도시 기준 맛집 최대 5곳 검색
- API 오류 발생 시 오류 정보 관리
- 맛집 API 실패 시에도 최종 리포트 생성 진행
- 원본 데이터를 JSON 파일로 저장
- 최종 여행 리포트를 Markdown 파일로 저장

---

## 3. 개발 환경

- Python 3.10 이상
- 터미널 기반 CLI 프로그램
- Google Gemini API
- Kakao Local API
- `requests`
- `python-dotenv`

---

## 4. 프로젝트 구조

```text
travel_project/
├── .venv/                  # Python 가상환경
├── results/                # 실행 결과 저장 폴더
├── .env                    # API 키 저장
├── .gitignore              # Git 제외 파일 설정
├── main.py                 # 메인 프로그램
└── README.md               # 프로젝트 설명서
```

.env 파일에는 API 키가 포함되므로 GitHub에 업로드하지 않습니다.

## 5. API 키 설정

이 프로그램은 외부 API를 사용하므로 API 키가 필요합니다.

API 키는 Python 코드에 직접 작성하지 않고 .env 파일에 저장합니다.

.env 파일 예시

```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
KAKAO_REST_API_KEY=YOUR_KAKAO_REST_API_KEY
```

위의 YOUR_... 부분에는 실제 발급받은 API 키를 입력합니다.

실제 API 키는 README.md, GitHub 저장소, 코드, 실행 결과 파일 등에 직접 작성하지 않습니다.

## 6. 가상환경 실행

Windows PowerShell에서 프로젝트 폴더로 이동한 후 가상환경을 실행합니다.

.venv\Scripts\Activate.ps1

가상환경이 정상적으로 활성화되면 터미널 앞에 다음과 같이 표시됩니다.

(.venv)

PowerShell에서 실행 정책 오류가 발생하는 경우 현재 사용자 범위에서 다음 명령을 사용할 수 있습니다.

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

## 7. 필요한 패키지 설치

다음 명령으로 필요한 패키지를 설치합니다.

pip install requests python-dotenv

## 8. 프로그램 실행 방법

다음과 같이 실행합니다.

python main.py -date "2026-08-15"

-date 옵션은 필수입니다.

날짜는 다음 형식을 사용해야 합니다.

YYYY-MM-DD

예:

```text
python main.py -date "2026-08-15"
```

잘못된 날짜 형식을 입력하면 프로그램이 사용법을 출력하고 종료합니다.

## 9. 프로그램 실행 흐름

프로그램은 다음 순서로 실행됩니다.

사용자 날짜 입력
       ↓
날짜 형식 검증
       ↓
Gemini API 호출
       ↓
1차 여행 추천 JSON 생성
       ↓
추천 도시 추출
       ↓
Kakao Local API 호출
       ↓
맛집 검색
       ↓
원본 JSON 저장
       ↓
Gemini API를 이용한 최종 리포트 생성
       ↓
Markdown 리포트 저장
       ↓
결과 저장 경로 안내

## 10. 실행 결과

프로그램을 실행하면 results/ 폴더에 결과 파일이 생성됩니다.

예:

```text
results/
├── travel_2026-08-15.json
└── travel_report_2026-08-15.md
```

원본 JSON

원본 JSON에는 다음 정보가 포함됩니다.

1차 여행 추천 결과
추천 도시
날씨
행사/축제
추천 이유
맛집 검색 결과
오류 정보
최종 Markdown 리포트

최종 리포트에는 다음 내용이 포함됩니다.

추천 지역
추천 이유
날씨 요약
행사/축제 목록
추천 맛집
1일 여행 일정

## 11. 오류 처리

외부 API를 사용하는 프로그램이므로 API 호출 과정에서 오류가 발생할 수 있습니다.

Gemini API 오류

Gemini API 호출 또는 JSON 파싱 과정에서 오류가 발생하면 오류를 처리합니다.

JSON 파싱에 실패한 경우에는 JSON 형식으로 다시 요청하여 최대 1회 재시도합니다.

Kakao Local API 오류

Kakao API에서 인증, 네트워크, 쿼터 등의 오류가 발생하더라도 프로그램 전체를 중단하지 않습니다.

이 경우 맛집 목록을 데이터 없음 상태로 처리하고 최종 여행 리포트 생성을 계속합니다.

API 키 미설정

필요한 API 키가 설정되지 않은 경우 프로그램을 실행하지 않고 API 키 설정 방법을 안내합니다.

## 12. API 키 보안 주의사항

API 키는 외부에 공개되지 않도록 관리해야 합니다.

API 키를 코드에 직접 작성하지 않고 .env 파일이나 환경변수를 사용하는 이유는 다음과 같습니다.

GitHub 등에 API 키가 실수로 공개되는 것을 방지할 수 있습니다.
API 키를 변경할 때 코드를 수정하지 않아도 됩니다.
API 사용량 및 과금과 관련된 보안 사고를 예방할 수 있습니다.
협업 과정에서 API 키가 다른 사람에게 노출되는 것을 줄일 수 있습니다.

Git에 업로드하지 않는 파일

.gitignore에 다음 내용을 추가하여 API 키와 가상환경이 GitHub에 올라가지 않도록 합니다.

```text
.env
.venv/
__pycache__/
```

## 13. 결과 확인

프로그램 실행이 완료되면 터미널에 결과 파일의 저장 경로가 표시됩니다.

예:

원본 데이터:
results/travel_2026-08-15.json

최종 여행 리포트:
results/travel_report_2026-08-15.md

생성된 Markdown 파일은 VS Code 또는 GitHub에서 확인할 수 있습니다.

## 14. 학습 목표

이 프로젝트를 통해 다음 내용을 학습했습니다.

REST API의 요청과 응답 구조
HTTP GET/POST 방식의 차이
LLM API의 JSON 구조화
LLM 결과를 다음 API 요청의 입력으로 활용하는 방법
외부 API의 인증, 네트워크, 쿼터, 파싱 오류 처리
.env와 환경변수를 이용한 API 키 관리
Python CLI 프로그램 구현
JSON 및 Markdown 파일 저장

