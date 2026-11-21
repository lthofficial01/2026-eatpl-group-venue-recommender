# 기술적 의사결정과 트레이드오프

## 1. 직접 eat.pl API 대신 K-Skill 경로 사용

- **문제:** 직접 제휴 API 사용에는 기관명/서버 IP 등록 등 사전 조건이 있었습니다.
- **선택:** 테스트·서비스 연결에서는 K-Skill을 통한 eat.pl 조회 경로를 사용했습니다.
- **구현에서 중요했던 것:** 응답의 실제 제공처 확인, 링크 출처 검증, 업종/지역/매출 순위 필드의 의미 구분, 오류/빈 후보 처리.
- **한계:** 프록시 서비스의 가용성, 검색 범위와 제공 데이터 스키마에 의존합니다.

근거: [PR #7](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/7), [PR #14](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/14). 지역명·업종표에 대한 **실데이터 정제는 팀원의 [PR #16](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/16)**이 주요 근거입니다.

## 2. SQLite 선택 및 온라인 백업

- **문제:** 링크 기반 모임방과 참가자 수정 정보가 서버 프로세스 재시작 후에도 유지되어야 합니다.
- **선택:** MVP에서는 SQLite를 지속 저장소로 사용. 별도 DB 서버 운영 부담을 줄였습니다.
- **본인 개선 영역:** 운영 DB의 온라인 백업, 백업된 복사본의 스키마/무결성 검증, 동시 쓰기 시점의 잠금 경합 완화.
- **구체적 방식:** SQLite `Connection.backup`으로 일관된 복사본을 만들고, 백업 파일에 `quick_check`를 수행합니다. 기존 목적지 파일을 덮어쓰지 않도록 합니다.
- **한계:** 워커/서버 수를 늘릴 경우 동시성 제약과 상태 관리 모델을 다시 설계해야 합니다.

기본 모임 저장 구조·API는 [팀원 PR #13](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/13), 배포·백업 개선은 [PR #14](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/14), [PR #28](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/28)로 구분합니다.

## 3. 그룹 선호 랭킹: 단순 가중치 합계의 한계

- **증상:** 중식 2명과 한식 1명이어도 예산·매출·방문 유형 가점으로 한식이 우선되는 사례.
- **변경:** 식당은 **음식 종류 최다 득표 → 세부 적합 점수 → 제공된 매출 순위** 순으로 비교.
- **안전:** 알레르기 위험이 높다고 분류된 후보는 선호 득표가 많아도 제외합니다. 정보 미확인은 '안전'으로 해석하지 않습니다.
- **트레이드오프:** 다수의 음식 취향을 명시적으로 앞세우는 정책이므로 소수 취향/예산 최적화와는 다른 결과가 나옵니다. 학습형 모델이 아닙니다.

근거: [PR #30](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/30), [실제 추천 코드](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/blob/main/moim/recommend.py), [독립 재현 예제](../examples/group_ranker.py).

## 4. AWS Lightsail / Vercel 분리 운영

- **서버:** Python API와 SQLite는 Lightsail, 정적 프론트는 Vercel에 배포.
- **운영 이슈:** HTTPS 도메인·CORS 허용 출처·서버 호스트 검증·비밀키 관리·프론트/백엔드 버전 불일치.
- **선택:** Gunicorn 단일 worker를 사용하는 초기 서비스 구성과 읽기 전용 배포 점검. DB 초기화 없이 백업→코드 검증→재시작·검증 순서.
- **제약:** GitHub/Vercel 성공 상태만으로 AWS 실제 커밋이 일치한다고 단정할 수 없습니다. 서버 SSH에서 버전을 확인해야 합니다.

근거: [PR #14](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/14), [PR #20](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/20), [PR #28](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/28), [팀 배포 가이드](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/blob/main/docs/deployment.md).

## 5. 5/6·6/6 자동 갱신 시 깜빡임 해결

- **원인:** 방·추천 데이터를 일정 시간마다 가져오는 과정에서 화면 전체 DOM을 다시 만들어 내용이 같아도 시각적으로 깜빡였습니다.
- **수정:** 이전 상태와 같으면 DOM을 유지, 상세 정보나 경고가 바뀔 때는 결과의 필요한 부분만 교체.
- **검증:** 자동 폴링 전후 카드 노드와 열린 설명 영역이 유지되는지 브라우저 테스트를 추가했습니다.

근거: [PR #30](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/pull/30), [UI 테스트](https://github.com/BDAI9/2026-eatpl-group-venue-recommender/blob/main/tests/ui_smoke.mjs).

## 6. 향후 개선

- 추천 목록의 실제 사용자 평가셋과 결과 편향 분석
- 알레르기 위험 신호의 과잉 제외/누락에 대한 전문가 검증
- 프록시 장애·요청 제한을 고려한 캐시·재시도 정책
- 접속 수 증가 시 DB/worker 분리, 부하 및 복구 시험
- 초대 링크·참여자 이름·알레르기 입력에 대한 보관/삭제 정책

[README](../README.md) · [아키텍처](architecture.md) · [기여 내역](evidence.md)