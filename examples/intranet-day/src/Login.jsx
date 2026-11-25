
// useState는 컴포넌트가 값을 기억하고, 변경된 값으로 화면을 다시 계산하도록 합니다.
import { useState } from 'react';

// { onLogin }은 부모가 전달한 props 객체에서 onLogin을 꺼내는 구조 분해 문법입니다.
// App에서 전달한 setUser 함수를 여기서는 onLogin이라는 이름으로 사용합니다.
// 'on...'은 어떤 일이 일어났을 때 호출할 함수에 자주 쓰는 이름 규칙입니다.
// 이름만 붙이면 자동 실행되는 것이 아니라 아래 onLogin(data.user)가 직접 호출합니다.
export default function Login({ onLogin }) {
  // 입력칸의 값을 빈 문자열로 시작합니다. 숫자처럼 보여도 사번은 문자열로 다룹니다.
  // 예: '001'을 숫자로 바꾸면 앞의 0이 사라져 다른 사번이 될 수 있습니다.
  const [id, setId] = useState('');
  // 비밀번호도 입력 중에는 문자열로 기억합니다. 콘솔에 출력하지 마세요.
  const [password, setPassword] = useState('');
  // visible은 '비밀번호를 글자로 보여 줄까?'입니다. 처음에는 숨깁니다.
  const [visible, setVisible] = useState(false);
  // busy는 '서버 답을 기다리는 중인가?'입니다. 입력과 제출 버튼을 잠시 막습니다.
  const [busy, setBusy] = useState(false);
  // 오류 문구가 없을 때는 ''. 오류가 생기면 아래 안내 문단에 표시합니다.
  const [error, setError] = useState('');

  // submit은 폼을 제출할 때 실행됩니다. async이므로 await를 사용할 수 있습니다.
  // event는 브라우저에서 일어난 제출 사건의 정보를 담은 React 이벤트 객체입니다.
  async function submit(event) {
    // HTML 폼은 기본적으로 제출하면서 페이지를 이동/새로고침할 수 있습니다.
    // 그 기본 동작을 막고, 아래 fetch로 요청해서 React 화면 안에서 결과를 처리합니다.
    // 주의: 이것이 브라우저의 required 검사까지 없애는 것은 아닙니다.
    event.preventDefault();
    // 재시도할 때 이전 오류를 지우고 '기다리는 중'으로 바꿉니다.
    setError('');
    setBusy(true);
    try {
      // fetch는 비동기로 서버에 요청합니다. await는 이 함수에서 응답을 기다립니다.
      // 기다리는 동안 브라우저 전체가 멈추는 것은 아닙니다.
      const response = await fetch('/api/login', {
        // 이 API는 로그인 정보를 보내므로 POST 요청을 사용합니다.
        method: 'POST',
        // 서버에 '본문은 JSON 형식입니다'라고 알려 주는 요청 헤더입니다.
        headers: { 'Content-Type': 'application/json' },
        // JSON.stringify는 JavaScript 객체를 전송할 문자열로 바꿉니다.
        // { id: id.trim(), password }에서 password는 password: password의 줄임말입니다.
        // trim()은 사번 앞뒤의 공백을 없앱니다. 입력칸 상태 자체를 바꾸지는 않습니다.
        // 비밀번호의 공백은 실제 비밀번호 일부일 수 있으므로 여기서는 제거하지 않습니다.
        // 주의: JSON 변환은 암호화가 아닙니다. 비밀번호 숨김 표시도 암호화가 아닙니다.
        // 실제 서비스의 전송 보호에는 HTTPS 같은 별도 준비가 필요합니다.
        body: JSON.stringify({ id: id.trim(), password }),
      });
      // 응답 본문을 JavaScript 값으로 읽습니다. 이 작업도 비동기라 await가 필요합니다.
      // 서버가 JSON 대신 HTML 등을 보내면 여기서 파싱 오류가 날 수 있습니다.
      const data = await response.json();
      // fetch는 HTTP 401/500 응답만으로 자동으로 catch로 가지 않습니다.
      // ok(상태 코드 200~299)를 검사하고 실패면 Error를 던져 catch로 보냅니다.
      // ||는 왼쪽이 비어 있는 등의 falsy 값이면 오른쪽 기본 문구를 사용합니다.
      if (!response.ok) throw new Error(data.message || '로그인에 실패했습니다.');
      // 성공하면 이 컴포넌트의 입력 상태를 비웁니다. 모든 메모리를 지우는 보장은 아닙니다.
      setPassword('');
      // 부모에게 '이 직원으로 로그인했어요'라고 알립니다.
      // App의 user가 바뀌어 Login 대신 Intranet을 보여 주게 됩니다.
      // 서버는 별도로 세션 쿠키를 설정합니다. 화면 상태만으로 인증하지 않습니다.
      onLogin(data.user);
    } catch (err) {
      // instanceof는 오류가 어떤 종류인지 확인합니다.
      // SyntaxError는 JSON 읽기 실패, TypeError는 fetch 연결 실패 등에서 생길 수 있습니다.
      // 이 코드는 둘을 연결 안내로 묶습니다. 이 종류만으로 정확한 원인을 확정할 수는 없습니다.
      // 조건 ? 참일 때 값 : 거짓일 때 값은 삼항 연산자입니다.
      setError(
        err instanceof SyntaxError || err instanceof TypeError
          ? '백엔드 연결을 확인해주세요. 서버를 재시작한 후 다시 시도하세요.'
          : err.message,
      );
    } finally {
      // 성공/실패 어느 쪽이든 요청 진행 상태를 끝냅니다.
      setBusy(false);
    }
  }

  return (
    // main은 이 페이지의 중심 내용을 뜻하는 HTML 태그입니다.
    // 실제 요소가 되는 소문자 태그이며, 큰 제목이나 버튼과는 역할이 다릅니다.
    // className은 CSS 스타일 이름입니다. 태그의 의미와 스타일은 별개의 역할입니다.
    <main className="login-page">
      {}
      <div className="login-top">
         <img className="login-wordmark" src={`${import.meta.env.BASE_URL}logo.svg`} alt="온도워크" />
        <span>개발 연습용 가상 인트라넷</span>
      </div>
      <div className="login-stage">
        {}
        <section className="login-card" aria-labelledby="login-heading">

          {}
          <h1 id="login-heading">
            온도워크 인트라넷에
            <br />
            오신 것을 환영합니다.
          </h1>
          {}
          <p className="login-subtitle">함께 일하는 더 편리한 방법</p>
          {}
          <form onSubmit={submit}>
            {}
            <label htmlFor="employee-id">사원번호</label>
            {}
            <input
              id="employee-id"
              autoComplete="username"
              placeholder="사원번호를 입력해주세요."
              value={id}
              onChange={(e) => setId(e.target.value)}
              required
              maxLength={100}
              disabled={busy}
              autoCapitalize="none"
              spellCheck={false}
            />
            <label htmlFor="employee-password">비밀번호</label>
            {}
            <div className="password-field">
              {}
              <input
                id="employee-password"
                type={visible ? 'text' : 'password'}
                autoComplete="current-password"
                placeholder="비밀번호를 입력해주세요."
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                maxLength={200}
                disabled={busy}
              />
              {}
              <button
                type="button"
                onClick={() => setVisible((v) => !v)}
                aria-label={visible ? '비밀번호 숨기기' : '비밀번호 보기'}
                aria-pressed={visible}
              >
                {}
                {visible ? '숨김' : '보기'}
              </button>
            </div>
            {}
            {error && (
              <p className="login-error" role="alert">
                {error}
              </p>
            )}
            {}
            <button className="login-submit" type="submit" disabled={busy}>
              {busy ? '로그인 중…' : '로그인'}
            </button>
          </form>
          {}
          <div className="demo-credentials">
            <span>테스트 계정</span>
            <strong>user001 ~ user100</strong>
            <span>비밀번호</span>
            <strong>TestOnly!2026</strong>
          </div>
          <p className="login-help">회원 100명의 테스트 계정으로 로그인할 수 있습니다.</p>
        </section>
      </div>
      {}
      <footer className="login-footer">
        <span>© 2026 ONDO.</span>
        {}
      </footer>
    </main>
  );
}
