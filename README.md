# GatherRank — Group Preference-Aware Venue Recommendation

> **모임 구성원의 취향·예산·알레르기를 집계하고, K-Skill을 통한 eat.pl 장소 데이터에 근거 기반 우선순위를 적용한 그룹 장소 추천 서비스.**
>
> **본인 역할: 4인 팀장 · 백엔드 통합 · 데이터 연동(K-Skill) · SQLite 운영 안정성 · AWS/Vercel 배포·검증**

`Python` `SQLite` `K-Skill / eat.pl` `Rule-based Ranking` `AWS Lightsail` `Vercel` `GitHub Actions`

**팀 프로젝트 · 개인 기술 포트폴리오**  
[서비스 체험](https://jj2ya.vercel.app/) · [팀 공식 소스 코드](https://github.com/BDAI9/2026-eatpl-group-venue-recommender) · [프로젝트 아키텍처](docs/architecture.md) · [기술적 의사결정](docs/engineering.md)

> **저장소 구분:** 여기에는 본인이 맡은 영역의 구현·설계·검증 근거와 **독립 실행 가능한 소형 랭킹 예제**만 둡니다. 전체 웹 서비스의 정식 코드와 공동 기여 내역은 [BDAI9 팀 저장소](https://github.com/BDAI9/2026-eatpl-group-venue-recommender)가 기준입니다. 서비스명은 **지금어디가**입니다.

## 프로젝트 개요

| 구분 | 내용 |
| --- | --- |
| **개발 배경** | 모임 장소를 정할 때 음식 취향·예산·알레르기 요구가 충돌하고, 대화로 조율하는 과정이 반복됩니다. |
| **해결 과제** | 링크로 여러 명의 조건을 모은 뒤 데이터에 기반한 추천 후보와 선택 이유를 제시합니다. |
| **담당 역할** | **팀장(4인)**, 브랜치/PR 및 통합 조율, K-Skill 조회·검증 시범, SQLite 백업/데이터 보존, Gunicorn/WSGI·AWS Lightsail 배포 준비, Vercel 연동 점검, 그룹 랭킹·UI 폴링 개선 |
| **기능 범위** | 지역 선택 → 모임 링크 공유 → 개인 조건 수집 → 선호 집계 → 카페·식당·술집 추천 → eat.pl 상세 |
| **검증 결과** | [PR #30](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/30) 기준 **Python 테스트 248개 통과**, 브라우저 E2E 및 API 읽기 점검 성공. *추천 정확도나 실사용자 만족도 수치가 아닙니다.* |
| **개인 저장소 범위** | 프로젝트 구조·담당 기여·트레이드오프 문서 + 의존성 없는 교육용 랭커 예제/테스트. 팀 백엔드 전체를 복제하지 않음. |

## 1. 개발 배경 및 문제 정의

일반 맛집 검색은 인기/매출이 높은 가게를 보여주지만, 실제 모임에서는 여러 사람의 조건이 서로 다릅니다. 특히 **중식 2명·한식 1명인데 보조 점수 때문에 한식이 앞서는 문제**처럼, 추천 순위가 그룹 합의와 어긋날 수 있습니다.

이 프로젝트의 핵심 질문은 다음과 같습니다.

1. 개별 참여자의 조건을 공통 형식으로 수집해 집계할 수 있는가?
2. 음식 선호 다수결·예산·분위기·방문 특성을 어떻게 우선순위에 반영할 것인가?
3. 외부 데이터 지연·불확실성과 알레르기 위험을 어떻게 다룰 것인가?
4. 소규모 팀이 실제 사용자 흐름을 안전하게 배포·검증하려면 무엇이 필요한가?

## 2. 시스템 및 데이터 흐름

```text
브라우저 (Vercel)
    │  모임 링크, 조건 입력, 결과 확인
    ▼
Python API / Gunicorn WSGI (AWS Lightsail)
    ├── SQLite: 모임·참가자·추정 캐시
    ├── K-Skill → eat.pl 가게 검색·제공처 지표
    ├── 업종/메뉴 정보 → 규칙 기반 분류·위험 판단
    └── 그룹 투표·조건별 점수 → 추천 정렬
             └── (선택) 상세 메뉴·후기 / OpenRouter 추정
```

실제 요청 흐름과 모듈 연결은 [아키텍처 문서](docs/architecture.md)를 참고하세요.

## 3. 담당 업무 및 본인 기여

| 영역 | 수행한 일 | 확인 가능한 근거 |
| --- | --- | --- |
| **Team Lead / 협업** | 4인 역할·브랜치 협업 구조 정리, PR·통합·릴리스 관리 | [PR #1](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/1), [#10](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/10), [#27](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/27), [#28](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/28) |
| **K-Skill / 데이터 연동** | eat.pl 후보 조회 시범, 응답·상세 링크 검증, 직접 API와 K-Skill 연결의 제약 분석·진단 | [PR #7](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/7), [#14](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/14) |
| **SQLite / 서버 안정성** | 초기 DB/백업 진단 도구 및 동시 쓰기 중 안전한 SQLite 스냅샷 검증, 운영 DB 보존 절차 | [PR #14](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/14), [#28](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/28), [백업 코드](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/blob/main/moim/backup.py) |
| **AWS / 배포·통합** | Lightsail 운영 환경 준비·점검, Gunicorn/WSGI·systemd 구성, Vercel–API 분리 및 연결 확인 | [PR #14](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/14), [#20](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/20), [#28](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/28) |
| **추천·UX 개선** | 음식 종류 득표 우선 정렬, 알레르기 예외 테스트, 5/6·6/6 화면 부분 갱신 | [PR #30](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/30) |
| **품질·문서화** | 모바일 UI 개선, Playwright 테스트, GitHub Actions·운영 가이드 정리 | [PR #29](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/29), [#31](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/31) |

**팀 기여 구분:** 초기 모임방/참여자 API·기본 추천 로직은 팀원이 [PR #13](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/13)에 구현했고, K-Skill 실데이터 지역·업종 분류 보강은 팀원의 [PR #16](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/16)에서 진행했습니다. 이를 개인 단독 성과로 포함하지 않습니다.

## 4. 핵심 기능

| 단계 | 기능 | 산출물 |
| --- | --- | --- |
| Input | 지역·업종·음식 종류·예산·분위기·알레르기 입력 | 개인별 조건 |
| Collaboration | 링크 공유·조건 수정·응답 수 집계 | 그룹 선호 요약 |
| Retrieval | K-Skill을 통한 eat.pl 장소 후보 조회 | 업종·주소·결제 신호가 있는 후보 |
| Ranking | 고위험 알레르기 제외 → 음식 득표 우선 → 세부 점수·매출 순위 | 정렬된 장소 목록 |
| Evidence | 일치 이유·추정·미확인 경고·eat.pl 상세 링크 | 설명 가능한 추천 결과 |
| Enrichment | 선택적인 상세정보·AI 보강 및 화면 부분 갱신 | 추가된 근거 |

## 5. 기술적 의사결정

| 결정 | 이유 | Trade-off |
| --- | --- | --- |
| K-Skill 사용 | 직접 eat.pl 연동은 기관명·서버 IP 등록이 필요했던 반면, K-Skill 경로로 후보 조회가 가능 | 제공처 프록시의 응답 규격·장애·데이터 범위에 의존 |
| SQLite와 온라인 백업 | 작은 MVP에 맞는 단순한 상태 저장 및 운영 중 데이터 보존 | 단일 서비스의 동시성·확장성 한계 |
| 음식 종류 최다 득표 우선 | 다수의 명시적 음식 선호가 예산/매출 보조 점수에 역전되는 현상을 방지 | 소수 의견이나 가격보다 음식 다수결을 우선하는 정책 |
| 규칙 기반 랭킹 + 선택적 AI | 모델 응답 지연·실패에도 즉시 검증 가능한 일부 후보 제공 | 데이터 근거가 부족하면 추정·경고가 남음 |
| 동일 응답은 DOM 유지 | 폴링 중 화면 깜빡임·펼침 상태 초기화 방지 | 비동기 요청·UI 상태 동기화에 추가 주의 필요 |
| Vercel + Lightsail 분리 | 프론트 정적 배포와 Python API/SQLite 운영을 구분 | CORS·버전 정합성과 서버 수동 배포 점검 필요 |

자세한 근거는 [기술 결정 기록](docs/engineering.md)에 정리했습니다.

## 6. 데이터 및 보안·안전 범위

- **eat.pl 지표:** 가게·업종·주소와 제공된 결제 관련 정보만 근거로 사용합니다. **매출 순위가 추천 정확도를 보증하지는 않습니다.**
- **알레르기:** 높은 위험 신호는 제외하지만, 재료 미확인·교차접촉 위험은 알 수 없습니다. **실제 안전은 매장에 확인해야 합니다.**
- **추정:** 가격·분위기·운영시간은 일부 추정이며 실제 정보를 보증하지 않습니다.
- **보안:** 개인정보·참가자/방장 토큰·실제 DB·API 비밀값을 이 개인 저장소에 보관하지 않습니다.
- **저장소 정책:** 팀의 공동 구현 전체를 개인 소유로 복제하거나 새로운 라이선스를 임의 부여하지 않습니다.

## 7. 주요 산출물 및 구현 근거

| 확인 목적 | 자료 |
| --- | --- |
| K-Skill 조회·데이터 검증 | [`moim/eatpl.py`](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/blob/main/moim/eatpl.py) |
| SQLite 상태 저장 | [`moim/store.py`](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/blob/main/moim/store.py) |
| SQLite 온라인 백업 | [`moim/backup.py`](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/blob/main/moim/backup.py) |
| 운영 WSGI | [`moim/wsgi.py`](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/blob/main/moim/wsgi.py) |
| 그룹 선호 랭커 | [`moim/recommend.py`](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/blob/main/moim/recommend.py) |
| 폴링·부분 렌더링 | [`web/v2.js`](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/blob/main/web/v2.js) |
| 추천 회귀 테스트 | [`tests/test_moim.py`](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/blob/main/tests/test_moim.py) |
| 통합 CI | [`.github/workflows/verify-integration.yml`](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/blob/main/.github/workflows/verify-integration.yml) |
| **독립 실행하는 소형 예제** | [`examples/group_ranker.py`](examples/group_ranker.py), [`tests/test_group_ranker.py`](tests/test_group_ranker.py) |

## 8. 활용 기술

| 계층 | 기술 |
| --- | --- |
| Backend | Python 표준 라이브러리 기반 API, Gunicorn/WSGI |
| DB | SQLite, 온라인 백업·일관성 검사 |
| Data Integration | K-Skill, eat.pl/BC카드 제공 지표 |
| Ranking | 그룹별 선호 집계, 규칙 기반 점수·정렬, 알레르기 위험 신호 |
| Frontend & Cloud | JavaScript, Vercel, AWS Lightsail, HTTPS/CORS |
| Validation | pytest, Playwright, GitHub Actions |
| Optional AI | OpenRouter를 통한 보조적인 가격·분위기·메뉴 해석 |

## 9. 개인 저장소 구조

```text
.
├── README.md                     # 이 문서: 개인 기여 중심 포트폴리오
├── docs/
│   ├── architecture.md           # 실서비스 시스템/데이터 흐름
│   ├── engineering.md            # 기술적 의사결정과 한계
│   └── evidence.md               # 역할별 PR·검증 근거
├── examples/
│   └── group_ranker.py           # 실제 서버와 분리된 최소 랭킹 예제
└── tests/
    └── test_group_ranker.py      # 표준 라이브러리 unittest
```

실제 운영 서비스 소스는 팀 저장소에서 확인하며, 이 저장소의 `examples/`는 **독립적인 교육용 재현 예제**입니다.

## 10. 실행 방법

Python 3.10 이상이면 별도 패키지 설치 없이 최소 랭커와 테스트를 실행할 수 있습니다.

```bash
python examples/group_ranker.py
python -m unittest discover -s tests -v
```

**전체 서비스 실행**은 [팀 저장소 README](https://github.com/BDAI9/2026-eatpl-group-venue-recommender#로컬-실행)를 따릅니다. 개인 저장소만으로 eat.pl 검색·모임방 API·Vercel 사이트를 실행할 수는 없습니다.

## 11. 결과·한계 및 다음 단계

- **검증된 결과:** [PR #30 CI](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/actions/runs/44922000294)에서 Python **248개 테스트** 및 UI 시나리오 점검 통과. 이는 특정 PR 커밋의 결과입니다.
- **개선 사례:** 중식 2명·한식 1명인 입력에서 음식 다수 선호가 우선하도록 정렬하고, 알레르기 제외가 그대로 동작하는 회귀 테스트 추가.
- **한계:** 학습형 추천 모델이 아니라 **설명 가능한 규칙 기반 랭커**입니다. 실제 사용자 만족도·추천 정확도·대규모 확장성은 별도 검증되지 않았습니다.
- **향후:** 사용자 시나리오 기반 평가셋, 후보 부족/편향 분석, 동시 접속 부하·DB 복구 연습, 개인정보 보관·삭제 정책 보완.

---

**Attribution:** BDAI9의 4인 공동 프로젝트입니다. 이 개인 저장소는 팀장으로서의 **통합·운영·개선 기여를 기록**하는 포트폴리오이며 팀 전체 구현물의 단독 저작권이나 성과를 주장하지 않습니다.
