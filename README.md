# 가계부 백엔드 API

가계부 앱의 Django 기반 백엔드입니다.  
사용자 인증(JWT)을 통해 **계좌 등록, 조회, 삭제 및 거래 내역 등록, 조회 기능**을 제공합니다.  
RESTful API 기반으로 작동하며, Swagger를 통한 자동화된 API 문서도 함께 제공합니다.
---

## 팀원 및 역할

- 박 현: 배포 과정 총괄
- 이지윤: 계좌 관리 API (등록, 조회, 삭제), 모델 및 시리얼라이저 설계, 테스트 코드 작성
- 최승민: 프로젝트 초기 구조 설계, Swagger 문서 작성, 전체 코드 리뷰 및 통합, GitHub Action CI 추가
--- 

## 주요 기능

- 회원가입 / 로그인, 로그아웃 (JWT 인증)
- 내 정보 조회
- 계좌 등록 / 목록 조회 / 삭제
- Swagger 기반 API 문서
- 사용자별 데이터 접근 제한

---

## 기술 스택

|              | 기술                           | 설명                        |
|--------------|-------------------------------|----------------------------|
| **Backend**  | Python                        | 3.12                       |
|              | Django                        | 5.2.2                      |
|              | Django REST Framework (DRF)   | RESTful API 구현            |
|              | Simple JWT                    | JWT 기반 인증 시스템           |
|              | drf-yasg                      | Swagger 문서 자동화 도구       |
| **Database** | PostgreSQL                    | 관계형 데이터베이스             |
|              | psycopg2                      | PostgreSQL 데이터베이스 어댑터  |
| **Dev Tools**| isort                         | import 정렬 자동화            |
|              | black                         | Python 코드 포매터            |

---
## 디렉토리 구조

django_mini_project/
├── .config_secret/ # 환경변수 및 시크릿 관리
├── .github/ # GitHub Actions 등 워크플로
├── accounts/ # 계좌 관련 모델, API
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
├── config/ # Django 설정
├── requirements/ # 패키지 요구사항
├── transaction/ # 거래 내역 처리용 앱
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
├── user/ # 사용자 인증/관리
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
├── utils/ # 상수, 공통 유틸
├── .gitignore
├── main.py
├── manage.py # Django 진입점
├── pyproject.toml # 빌드 설정
├── README.md
├── requirements.txt
├── test.sh # 코드 포맷팅 검사 스크립트
└──  uv.lock # 패키지 버전 락 파일
---

## API 문서
- Swagger: http://localhost:8000/swagger/

- 대부분의 API는 로그인한 사용자만 사용할 수 있도록 보호되어 있습니다.
Swagger 문서에서 API를 테스트하려면, 로그인 후 발급받은 Access Token을 사용해 인증해야 합니다.
Swagger 문서 상단의 Authorize 🔓 버튼을 클릭한 후, 아래 형식으로 입력하세요:
`Bearer <your_access_token>`
입력 후 인증이 완료되면 🔒 아이콘이 있는 API 엔드포인트들을 테스트할 수 있습니다.

#### User (인증 및 사용자)
| 메서드    | 경로                     | 설명                 |
| ------ | ---------------------- | ------------------ |
| `POST` | `/user/login/`         | 로그인 (JWT 발급)       |
| `POST` | `/user/logout/`        | 로그아웃 (토큰 블랙리스트 처리) |
| `GET`  | `/user/me/`            | 현재 로그인한 사용자 정보 조회  |
| `POST` | `/user/signup/`        | 회원가입               |
| `POST` | `/user/token/refresh/` | JWT Refresh 토큰 갱신  |

#### Accounts (계좌)
| 메서드      | 경로                  | 설명       |
| -------- | ------------------- | -------- |
| `GET`    | `/accounts/`        | 계좌 목록 조회 |
| `POST`   | `/accounts/create/` | 계좌 등록    |
| `DELETE` | `/accounts/{id}/`   | 계좌 삭제    |

#### Transactions (거래 내역)
| 메서드      | 경로                           | 설명          |
| -------- | ---------------------------- | ----------- |
| `GET`    | `/transactions/`             | 거래 내역 전체 조회 |
| `POST`   | `/transactions/create/`      | 거래 내역 등록    |
| `DELETE` | `/transactions/{id}/delete/` | 거래 내역 삭제    |
| `PUT`    | `/transactions/{id}/update/` | 거래 내역 전체 수정 |
| `PATCH`  | `/transactions/{id}/update/` | 거래 내역 일부 수정 |
---

## 참고 사항

본 프로젝트는 학습 및 팀 연습을 목적으로 진행되었으며, 이를 위해 일부 테스트 스크립트(`test.py`) 파일이 프로젝트 디렉토리 내부에 포함되어 있습니다.  
실제 운영 또는 배포 환경에서는 테스트 코드를 분리하거나 별도의 테스트 디렉토리(`tests/`)로 관리하는 것이 권장되지만,  
이 프로젝트에서는 나중에 참고하거나 복습할 수 있도록 코드와 함께 보존해두었습니다.
