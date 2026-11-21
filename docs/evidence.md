# 역할 및 기여 근거 · Contribution Evidence

**팀 리드 + 백엔드 운영/통합 관점의 기여 기록**입니다. GitHub PR의 작성자·코드·기능 범위를 함께 표기하고, 팀원 구현물을 내 단독 성과로 옮기지 않습니다.

## 내 담당 영역

| 역할 | 작업·설명 | 근거 |
| --- | --- | --- |
| 팀장 / 협업 초기화 | 4명 역할 분담, 저장소 협업 설정, PR 통합·릴리스 조율 | [#1](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/1), [#27](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/27), [#28](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/28) |
| eat.pl / K-Skill 연결 시범 | K-Skill 장소 조회·응답/상세링크 확인, 직접 API 제약·진단 | [#7](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/7), [#10](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/10), [#14](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/14) |
| SQLite 백업·보존 | 백업/진단·운영용 서버 구성, 동시 쓰기 상태에서 백업본 검증 | [#14](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/14), [#28](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/28) |
| 서버 배포·연결 | Gunicorn/WSGI·AWS Lightsail 운영 구성 준비, Vercel 정적 파일·CORS 연결 점검 | [#14](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/14), [#20](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/20), [#28](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/28) |
| 추천 로직·안전 검증 | 다수 음식 득표 우선 랭킹, 알레르기 고위험 예외, 동률 테스트 | [#30](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/30) |
| UI·품질 | 폴링 DOM 유지/부분 갱신, 320–430px 모바일 테스트와 스냅샷, CI | [#29](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/29), [#30](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/30) |
| 정리/문서 | 프로젝트 README, 구조·추천·배포 문서 간소화 | [#31](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/31), [#34](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/34) |

## 팀원이 수행한 주요 구현

| 기능 | 팀원 PR | 기여 구분 |
| --- | --- | --- |
| 링크 기반 모임방·참가자·기본 SQLite 저장 및 추천 초기 구조 | [#13](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/13) | **팀원의 초기 서비스 구현** |
| 비동기 AI 추정과 업종·알레르기 규칙 보강 | [#15](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/15) | **팀원의 개선** |
| K-Skill 실데이터 지역 쿼리·업종 매핑·이름 기반 분류 | [#16](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/16) | **팀원의 검증 및 정제** |
| 사용자 입력/요약 등 후속 통합 | [#25](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/25), [#26](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/26) | 팀 전체 개선 |

## 결과·증거 해석

- [PR #30 자동검증](https://github.com/BDAI9/2026-project-demo/actions/runs/44922000294): Python **248 tests passed** + 브라우저 스모크 및 외부 API/운영 읽기 점검. 기존 repo rename 전 링크여도 GitHub 리디렉션될 수 있습니다.
- '248개'는 자동 테스트 실행 건수이며 **추천 정확도·실사용자 만족도·동시 접속 성능 수치가 아닙니다**.
- 현재 Lightsail 배포 버전은 서버에서 확인해야 합니다. 코드가 main에 병합됐다는 사실만으로 AWS 배포 완료를 주장하지 않습니다.
- 본인 기여는 팀장/통합자/운영·진단/개선 구현자이며, **서비스 전부를 독립 구현한 것은 아닙니다**.

## 면접에서 설명할 한 문단

> 4인 프로젝트의 팀장을 맡아 기능별 브랜치와 통합/릴리스 흐름을 관리했습니다. 백엔드 측에서는 K-Skill을 통한 eat.pl 장소 조회 시범과 응답 검증, SQLite 백업 안정성, AWS Lightsail의 WSGI 배포 구성 및 Vercel 연동 점검에 기여했습니다. 사용 중 발견된 다수 음식 선호 역전 현상과 화면 자동 갱신 깜빡임은 랭킹 정렬 기준과 부분 렌더링을 수정하고 회귀 테스트로 확인했습니다. 초기 모임방 API와 실데이터 분류 개선 등은 팀원들의 구현을 통합한 작업입니다.

[README](../README.md) · [아키텍처](architecture.md)