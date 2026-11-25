# ONDO WORK 개발 연습 공개본

AI를 활용해 하루 동안 만든 개인 인트라넷의 공개용 버전입니다. 원본 회사·직원·DB 자료를 포함하지 않습니다.

- 원본 폴더와 원본 로고·DB는 수정하거나 복사하지 않았습니다.
- ONDO WORK 로고와 직원·부서·이메일(example.com)·프로젝트·문서·일정은 가상입니다.
- 공개본은 실제 인증/서버/DB 없이 가상 계정과 localStorage로 동작합니다. 체험 입력은 브라우저에만 남고, 상단 초기화로 지울 수 있습니다. 날짜가 바뀌면 초기화됩니다.
- 파일 첨부는 공개본에서 비활성화했습니다.
- 초기 구현 1일과 공개용 정리는 별도입니다. AI 코드 생성·구현을 학습 사례로 소개하며 독자 개발·실무 도입·사용성 검증 성과를 주장하지 않습니다.

## 실행과 수정

이 폴더에서 `npm ci`, `npm run dev`를 실행합니다. `npm test`로 가상 데이터·근태·게시글·결재·초기화를 검사합니다.
`npm run build`는 포트폴리오의 `src/assets/demos/intranet-day` 정적 파일을 갱신합니다. 그 뒤 저장소 루트에서 `npm run build`를 실행하면 사례와 데모가 dist에 함께 포함됩니다.

사례 내용: `src/content/projects.json`의 intranet-day, 데모 진입: `assets/demos/intranet-day/index.html`.
