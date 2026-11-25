
// useRef는 DOM 요소나 값을 기억하고, useEffect는 렌더링 후 브라우저 작업을 처리합니다.
import { useEffect, useRef } from 'react';
// createPortal은 React의 부모·자식 관계를 유지하면서 DOM의 표시 위치를 옮깁니다.
import { createPortal } from 'react-dom';
import { IconX } from '@tabler/icons-react';
// 컴포넌트 바깥 변수이므로 열린 모든 Modal이 공유합니다.
// dialogs의 마지막 요소가 가장 위에 열린 팝업입니다. 중첩 팝업 처리를 위한 목록입니다.
const dialogs = [];
// 마지막 팝업이 닫힐 때 복원할 body의 기존 인라인 overflow 값입니다.
let bodyOverflow = '';

// props를 구조 분해합니다. title은 접근성 이름, close는 부모가 전달한 닫기 함수입니다.
// children은 <Modal>과 </Modal> 사이의 내용이며 JSX, 문자열 등 React가 표시할 값입니다.
// className을 생략하면 기본값 ''를 사용합니다. Modal 자체에는 open 상태가 없습니다.
// 실제로 팝업을 없애는 것은 close를 받은 부모가 조건부 렌더링을 바꾸는 작업입니다.
export default function Modal({ title, children, close, className = '' }) {
  // ref.current는 아래 <section ref={ref}>의 실제 DOM 요소를 가리킵니다.
  // 처음 렌더링할 때는 아직 DOM이 연결되지 않았으므로 null로 시작합니다.
  const ref = useRef(null);
  // 키보드 이벤트에서 최신 close 함수를 사용하도록 별도의 ref에 보관합니다.
  // ref.current를 바꾸는 것만으로는 화면이 다시 렌더링되지 않습니다.
  const closeRef = useRef(close);
  useEffect(() => {
    closeRef.current = close;
  }, [close]);
  // [close]가 있는 위 Effect는 close가 바뀔 때 갱신됩니다.
  // 아래 [] Effect는 마운트 시 설정하고 언마운트 시 정리합니다.
  // 개발 모드의 StrictMode에서는 설정 → 정리 → 설정을 추가 실행할 수 있습니다.
  useEffect(() => {
    // 닫은 뒤 원래 버튼 등으로 키보드 초점을 돌려주기 위해 현재 위치를 기억합니다.
    const previous = document.activeElement;
    const dialog = ref.current;
    if (!dialogs.length) bodyOverflow = document.body.style.overflow;
    // at(-1)은 배열의 마지막 요소입니다. ?.는 값이 없으면 호출을 건너뜁니다.
    // inert는 아래에 깔린 팝업을 클릭하거나 키보드로 조작하지 못하게 합니다.
    dialogs.at(-1)?.setAttribute('inert', '');
    dialogs.push(dialog);
    dialog.focus();
    function keydown(event) {
      // 팝업이 여러 개여도 맨 위 팝업만 Escape와 Tab을 처리합니다.
      if (dialogs.at(-1) !== dialog) return;
      if (event.key === 'Escape') closeRef.current();
      if (event.key === 'Tab') {
        // querySelectorAll의 결과를 ...로 펼쳐 배열로 만든 뒤 비활성 요소를 제외합니다.
        // 주의: 이 선택자는 모든 종류의 초점 요소를 포함하지 않습니다.
        // 예를 들어 a[href] 링크나 숨겨진 요소까지 다루려면 별도 보완이 필요합니다.
        const elements = [
          ...dialog.querySelectorAll('button,input,select,textarea,[tabindex="0"]'),
        ].filter((el) => !el.disabled);
        const first = elements[0],
          last = elements.at(-1);
        // Shift+Tab으로 처음에서 뒤로 가면 마지막으로, Tab으로 마지막에서
        // 앞으로 가면 처음으로 이동합니다. 이를 '포커스 트랩'이라고 부릅니다.
        if (
          event.shiftKey &&
          (document.activeElement === first || document.activeElement === dialog)
        ) {
          event.preventDefault();
          last?.focus();
        } else if (
          !event.shiftKey &&
          (document.activeElement === last || document.activeElement === dialog)
        ) {
          event.preventDefault();
          first?.focus();
        }
      }
    }
    // 열린 동안 키보드 이벤트를 듣고 body 스크롤을 잠급니다.
    document.addEventListener('keydown', keydown);
    document.body.style.overflow = 'hidden';
    // Effect에서 반환하는 함수는 정리(cleanup) 함수입니다.
    // 팝업이 사라질 때 이벤트 제거, 팝업 목록 갱신, 스크롤·초점 복원을 합니다.
    return () => {
      document.removeEventListener('keydown', keydown);
      dialogs.splice(dialogs.indexOf(dialog), 1);
      dialogs.at(-1)?.removeAttribute('inert');
      document.body.style.overflow = dialogs.length ? 'hidden' : bodyOverflow;
      // 원래 초점 요소가 아직 문서에 연결되어 있을 때만 초점을 복원합니다.
      if (previous?.isConnected) previous.focus();
    };
  }, []);
  // JSX를 변수에 담을 수도 있습니다. content는 팝업에 표시할 React 요소입니다.
  const content = (
    // 배경 모양은 CSS의 modal-overlay가 담당합니다. 배경 클릭 닫기는 구현되어 있지 않습니다.
    <div className="modal-overlay">
      {}
      <section
        ref={ref}
        tabIndex={-1}
        className={`portal-modal ${className}`}
        role="dialog"
        aria-modal="true"
        aria-label={title}
      >
        {}
        <button className="modal-close" onClick={close} aria-label="닫기">
          <IconX size={20} aria-hidden="true" />
        </button>
        {}
        {children}
      </section>
    </div>
  );
  // 서버 렌더링 환경에는 document가 없으므로 DOM을 조회하지 않고 JSX만 반환합니다.
  // 브라우저에서는 .portal 요소가 있으면 그곳에, 없으면 body에 팝업을 붙입니다.
  // DOM 위치만 바뀌며 children의 React 상태·이벤트·부모 관계는 그대로 유지됩니다.
  return typeof document === 'undefined'
    ? content
    : createPortal(content, document.querySelector('.portal') || document.body);
}
