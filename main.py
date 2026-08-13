import argparse
import json
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


# --------------------------------------------------
# 환경변수 설정
# --------------------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")


# --------------------------------------------------
# 날짜 검증
# --------------------------------------------------

def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")

        if len(date_string) != 10:
            return False

        if date_string[4] != "-" or date_string[7] != "-":
            return False

        return True

    except ValueError:
        return False


# --------------------------------------------------
# Gemini API 호출
# --------------------------------------------------

def call_gemini(prompt):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-3.5-flash-lite:generateContent"
    )

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    text = result["candidates"][0]["content"]["parts"][0]["text"]

    return text

def search_restaurants(city, limit=5):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    headers = {
        "Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"
    }

    params = {
        "query": f"{city} 맛집",
        "size": limit
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    print("Kakao HTTP 상태 코드:", response.status_code)

    if response.status_code != 200:
       print("Kakao API 오류 응답:")
       print(response.text)

    response.raise_for_status()

    result = response.json()

    restaurants = []

    for place in result.get("documents", []):
        restaurant = {
            "name": place.get("place_name", ""),
            "address": place.get("road_address_name") or place.get("address_name", ""),
            "category": place.get("category_name", ""),
            "url": place.get("place_url", ""),
            "x": float(place["x"]) if place.get("x") else None,
            "y": float(place["y"]) if place.get("y") else None
        }

        restaurants.append(restaurant)

    return restaurants

def save_raw_data(date_string, recommendation, restaurants, errors):
    os.makedirs("results", exist_ok=True)

    file_path = f"results/travel_{date_string}.json"

    data = {
        "date": date_string,
        "recommendation": recommendation,
        "restaurants": restaurants,
        "errors": errors
    }

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

    return file_path

def get_cached_data(date):
    """
    같은 날짜의 기존 원본 JSON 파일이 있으면 읽어온다.
    파일이 없으면 None을 반환한다.
    """

    raw_file = Path("results") / f"travel_{date}.json"

    if not raw_file.exists():
        return None

    with open(raw_file, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_final_report(recommendation, restaurants, errors):

    restaurants_text = ""

    if restaurants:
        for i, restaurant in enumerate(restaurants, 1):
            restaurants_text += f"""
{i}. {restaurant["name"]}
- 주소: {restaurant["address"]}
- 카테고리: {restaurant["category"]}
- URL: {restaurant["url"]}
"""
    else:
        restaurants_text = "데이터 없음"

    errors_text = ""

    if errors:
        for error in errors:
            errors_text += f"- {error['step']}: {error['message']}\n"
    else:
        errors_text = "없음"

    prompt = f"""
다음 데이터를 바탕으로 국내 여행 최종 리포트를 Markdown 형식으로 작성해주세요.

[1차 여행 추천]
추천 지역: {recommendation["recommended_city"]}
날씨: {recommendation["weather"]}
행사/축제:
{chr(10).join("- " + event for event in recommendation["events"])}

추천 이유:
{recommendation["reason"]}

[맛집 목록]
{restaurants_text}

[오류 목록]
{errors_text}

최종 리포트에는 반드시 다음 항목을 포함하세요.

# 국내 여행 추천 리포트

## 1. 추천 지역
추천 지역과 추천 이유를 요약하세요.

## 2. 날씨
여행 시기의 날씨를 설명하세요.

## 3. 행사/축제
행사와 축제를 목록으로 정리하세요.

## 4. 추천 맛집
맛집을 목록으로 정리하세요.
맛집 데이터가 없으면 "데이터 없음"이라고 작성하세요.

## 5. 1일 여행 일정
오전 / 오후 / 저녁으로 나누어 일정을 제안하세요.

## 6. 오류 정보
오류가 없으면 "없음"이라고 작성하세요.

Markdown 문법을 사용하세요.
Markdown 코드 블록으로 감싸지 말고 순수 Markdown만 출력하세요.
"""

    return call_gemini(prompt)

def save_report(date_string, report):
    os.makedirs("results", exist_ok=True)

    file_path = f"results/travel_report_{date_string}.md"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(report)

    return file_path

# --------------------------------------------------
# 여행 추천 JSON 요청
# --------------------------------------------------

def get_travel_recommendation(date_string):

    prompt = f"""
여행 날짜는 {date_string}입니다.

한국 국내 여행지를 하나 추천해주세요.

해당 날짜의 실제 날씨를 조회하는 것이 아니라,
해당 시기의 일반적인 계절 날씨와 여행 특성을 기준으로 추천해주세요.

반드시 아래 JSON 형식으로만 답변해주세요.

{{
  "recommended_city": "도시 이름",
  "weather": "해당 시기의 일반적인 날씨 요약",
  "events": [
    "행사 또는 축제 후보 1",
    "행사 또는 축제 후보 2"
  ],
  "reason": "추천 근거를 2~4문장으로 작성"
}}

주의사항:
- JSON 이외의 설명은 작성하지 마세요.
- recommended_city는 문자열 하나만 작성하세요.
- weather는 문자열이어야 합니다.
- events는 문자열 배열이어야 합니다.
- events는 1~3개를 작성하세요.
- reason은 문자열이어야 합니다.
"""

    text = call_gemini(prompt)

    try:
        # Gemini가 반환한 JSON 문자열을 Python dictionary로 변환
        recommendation = json.loads(text)

        required_keys = [
            "recommended_city",
            "weather",
            "events",
            "reason"
        ]

        if not all(key in recommendation for key in required_keys):
            raise ValueError("필수 JSON 키가 누락되었습니다.")

        return recommendation

    except json.JSONDecodeError:
        print("Gemini JSON 파싱에 실패했습니다.")
        print("JSON 형식으로 다시 요청합니다.")

        retry_prompt = f"""
    앞서 요청한 여행 추천 결과를 JSON으로 다시 출력해주세요.

    여행 날짜: {date_string}

    반드시 아래 형식과 정확히 같은 구조로 출력하세요.

    {{
      "recommended_city": "도시 이름",
      "weather": "날씨 요약",
      "events": [
        "행사 또는 축제 1",
        "행사 또는 축제 2"
      ],
      "reason": "추천 이유"
    }}

    중요:
    - JSON만 출력하세요.
    - ```json 같은 코드 블록을 사용하지 마세요.
    - JSON 앞뒤에 설명을 작성하지 마세요.
    - recommended_city는 문자열 하나입니다.
    - weather는 문자열입니다.
    - events는 문자열 배열입니다.
    - events는 1~3개입니다.
    - reason은 문자열입니다.
    """

        retry_text = call_gemini(retry_prompt)

        recommendation = json.loads(retry_text)

        required_keys = [
            "recommended_city",
            "weather",
            "events",
            "reason"
        ]

        if not all(key in recommendation for key in required_keys):
            raise ValueError("재시도 결과에서도 필수 JSON 키가 누락되었습니다.")

        return recommendation

# --------------------------------------------------
# 메인 프로그램
# --------------------------------------------------

def main():

    errors = []

    parser = argparse.ArgumentParser(
        description="AI 여행 추천 프로그램"
    )

    parser.add_argument(
        "-date",
        required=True,
        help="여행 날짜 (YYYY-MM-DD 형식)"
    )

    args = parser.parse_args()

    # 날짜 검증
    if not validate_date(args.date):
        print("잘못된 날짜 형식입니다.")
        print("사용법: python main.py -date YYYY-MM-DD")
        return

    print(f"입력 날짜: {args.date}")
    print("날짜 형식이 올바릅니다.")

    # API 키 확인
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY가 설정되지 않았습니다.")
        print(".env 파일에 GEMINI_API_KEY를 설정해주세요.")
        return

    cached_data = get_cached_data(args.date)

    if cached_data:
        print("기존 결과 데이터를 발견했습니다.")
        print("API 호출을 건너뛰고 저장된 데이터를 사용합니다.")

        recommendation = cached_data["recommendation"]
        restaurants = cached_data["restaurants"]
        errors = cached_data.get("errors", [])

    else:
        print("새로운 여행 추천 데이터를 생성합니다.")
        print("Gemini API 호출 중...")

        try:
            recommendation = get_travel_recommendation(args.date)

            print("\n1차 여행 추천 결과:")

            print("추천 지역:", recommendation["recommended_city"])
            print("날씨:", recommendation["weather"])

            print("행사:")
            for event in recommendation["events"]:
                print("-", event)

            print("추천 이유:")
            print(recommendation["reason"])

            print("\nKakao 맛집 검색 중...")

            if not KAKAO_REST_API_KEY:
                print("KAKAO_REST_API_KEY가 설정되지 않았습니다.")

                errors.append({
                    "step": "kakao_api_key",
                    "message": "KAKAO_REST_API_KEY가 설정되지 않았습니다."
                })

                restaurants = []

            else:
                try:
                    restaurants = search_restaurants(
                        recommendation["recommended_city"]
                    )

                    print(f"맛집 검색 결과: {len(restaurants)}곳")

                    for restaurant in restaurants:
                        print("\n맛집 이름:", restaurant["name"])
                        print("주소:", restaurant["address"])
                        print("카테고리:", restaurant["category"])
                        print("URL:", restaurant["url"])
                        print("좌표:", restaurant["x"], restaurant["y"])

                except requests.RequestException as e:
                    print("Kakao 맛집 검색 중 오류가 발생했습니다.")
                    print(e)

                    errors.append({
                        "step": "kakao_restaurant_search",
                        "message": str(e)
                    })

                    restaurants = []

            raw_file = save_raw_data(
                args.date,
                recommendation,
                restaurants,
                errors
            )

            print(f"\n원본 데이터 저장 완료: {raw_file}")

        except (requests.RequestException, json.JSONDecodeError, ValueError) as e:
            print("Gemini 여행 추천 처리 중 오류가 발생했습니다.")
            print(e)

            errors.append({
                "step": "recommendation",
                "message": str(e)
            })

            return

        except (KeyError, IndexError) as e:
            print("Gemini 응답 형식을 처리하는 중 오류가 발생했습니다.")
            print(e)

            errors.append({
                "step": "recommendation_format",
                "message": str(e)
            })

            return

    print("\n최종 여행 리포트 생성 중...")

    try:
        report = generate_final_report(
            recommendation,
            restaurants,
            errors
        )

        report_file = save_report(
            args.date,
            report
        )

        print(f"최종 여행 리포트 저장 완료: {report_file}")

        print("\n" + "=" * 50)
        print("여행 추천 프로그램 실행 완료")
        print("=" * 50)

        print("\n원본 데이터:")

        raw_file = save_raw_data(
            args.date,
            recommendation,
            restaurants,
            errors
        )

        print(f"  {raw_file}")

        print("\n최종 여행 리포트:")
        print(f"  {report_file}")

        print("\nresults 폴더에서 결과 파일을 확인할 수 있습니다.")

    except requests.RequestException as e:
        print("최종 리포트 생성 중 Gemini API 오류가 발생했습니다.")
        print(e)

        errors.append({
            "step": "final_report",
            "message": str(e)
        })


if __name__ == "__main__":
    main()


