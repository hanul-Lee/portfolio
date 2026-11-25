import { useState } from 'react';
import {
  IconFileCheck,
  IconUserCircle,
  IconPlane,
  IconClock,
  IconFileText,
  IconX,
} from '@tabler/icons-react';
import Panel from './Panel';
import Modal from './Modal';
import EmployeeSelect from './EmployeeSelect';
import { dayKey } from '../utils/date';
import { approvalBuckets, approvalStatus, currentApprover } from '../utils/approvals';
import '../approvals.scss';

const descriptions = [
  '연차·반차·각종 휴가 및 교육·훈련 신청',
  '출장 일정과 차량 배차 신청',
  '개인 연장·휴일 근무 신청',
  '팀 단위 연장·휴일 근무 신청',
  '연장근무 확인 신청',
  '재직증명서 발급 신청',
  '원천징수영수증 발급 신청',
  '신규 입사 및 정보 변경에 따른 명함 신청',
  '연차 사용 일정 변경 신청',
  '업무용 주차 확인 신청',
];
const requestTypes = [
  '연차(휴가)',
  '오전반차',
  '오후반차',
  '시차',
  '경조휴가',
  '보건휴가',
  '출산휴가',
  '특별휴가',
  '경유',
  '훈련',
  '교육',
  '업무시작 미입력',
  '병가',
  '기타',
];

export function ApprovalHome({ data, user, compose, view }) {
  const [box, setBox] = useState(0);
  const [search, setSearch] = useState('');
  const [allTemplates, setAllTemplates] = useState(false);
  const buckets = approvalBuckets(data.approvals, user.id);
  const documents = (
    box === 3
      ? buckets[0].filter((d) => d.status === 'approved')
      : box === 4
        ? buckets[0].filter((d) => d.status === 'draft')
        : buckets[box]
  )
    .filter((d) => `${d.title} ${d.template} ${d.author}`.includes(search))
    .sort((a, b) => b.createdAt - a.createdAt);
  return (
    <div className="approval-layout">
      <aside className="approval-sidebar">
        <h2>
          <IconFileCheck size={20} aria-hidden="true" /> 전자결재
        </h2>
        <button className="primary" onClick={() => compose(data.templates[0])}>
          문서작성
        </button>
        <h3>결재문서함</h3>
        {['기안한 문서', '결재대기 문서', '반려 문서', '결재완료 문서', '임시저장 문서'].map(
          (s, i) => (
            <button className={box === i ? 'selected' : ''} key={s} onClick={() => setBox(i)}>
              {s}
              <span>›</span>
            </button>
          ),
        )}
      </aside>
      <div className="approval-main">
        <div className="portal-page-heading">
          <div>
            <h1>전자결재 홈</h1>
            <span>결재할 문서를 확인하거나 새 신청을 작성하세요.</span>
          </div>
          <input
            type="search"
            aria-label="결재 문서 검색"
            placeholder="문서 검색"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <h3>나의 현황</h3>
        <div className="approval-stats">
          {[
            ['승인대기', buckets[1].length, 1],
            ['기안한 문서', buckets[0].length, 0],
            ['결재완료', buckets[0].filter((d) => d.status === 'approved').length, 3],
            ['반려문서', buckets[2].length, 2],
          ].map(([label, count, index]) => (
            <button key={label} onClick={() => setBox(index)}>
              <span>{label}</span>
              <strong>{count}</strong>
            </button>
          ))}
        </div>
        <Panel
          title="문서 서식"
          action={
            <button className="text-button" onClick={() => setAllTemplates(true)}>
              전체 서식
            </button>
          }
        >
          <div className="template-list">
            {data.templates.slice(0, 4).map((t, i) => (
              <button key={t} onClick={() => compose(t)}>
                <strong>{t}</strong>
                <span>{descriptions[i]}</span>
                <b>›</b>
              </button>
            ))}
          </div>
        </Panel>
        <Panel
          title={
            ['기안한 문서', '결재대기 문서', '반려 문서', '결재완료 문서', '임시저장 문서'][box]
          }
          action={<span className="muted">{documents.length}건</span>}
        >
          <div className="approval-documents">
            {documents.map((doc) => (
              <button
                className="approval-document-card"
                key={doc.id}
                onClick={() => (doc.status === 'draft' ? compose(doc.template, doc) : view(doc))}
              >
                <div>
                  <h3>
                    {doc.title}{' '}
                    <span className={`status-pill ${doc.status}`}>
                      {approvalStatus[doc.status]}
                    </span>
                  </h3>
                  <p>
                    {doc.template} · 기안자: {doc.author} · {doc.member?.department}
                  </p>
                  <p>
                    {doc.startDate} ~ {doc.endDate} · {doc.reason}
                  </p>
                </div>
                <div className="approval-mini-line">
                  {doc.approverIds.map((id) => (
                    <span key={id}>
                      <IconUserCircle size={22} aria-hidden="true" />
                      <small>{data.members.find((m) => m.id === id)?.name}</small>
                    </span>
                  ))}
                </div>
              </button>
            ))}
            {!documents.length && <p className="empty-state">해당 문서가 없습니다.</p>}
          </div>
        </Panel>
      </div>
      <aside className="approval-recent">
        <h3>최근 사용 서식</h3>
        {[...new Set(buckets[0].sort((a, b) => b.createdAt - a.createdAt).map((d) => d.template))]
          .slice(0, 3)
          .map((t) => (
            <button key={t} onClick={() => compose(t)}>
              <IconFileText size={18} aria-hidden="true" /> {t}
            </button>
          ))}
      </aside>
      {allTemplates && (
        <Modal title="전체 문서 서식" close={() => setAllTemplates(false)}>
          <h2>전체 문서 서식</h2>
          <div className="template-list">
            {data.templates.map((t, i) => (
              <button key={t} onClick={() => compose(t)}>
                <strong>{t}</strong>
                <span>{descriptions[i]}</span>
                <b>›</b>
              </button>
            ))}
          </div>
        </Modal>
      )}
    </div>
  );
}

export function ApprovalDocument({ data, user, template, document, back, save, decide, busy }) {
  const peers = data.members.filter((m) => m.id !== user.id && m.department === user.department);
  const readonly = document && document.status !== 'draft';
  const [draft, setDraft] = useState(
    document || {
      template,
      title: template,
      requestType: '연차(휴가)',
      startDate: dayKey(),
      endDate: dayKey(),
      reason: '',
      approverIds: peers.slice(0, 2).map((m) => m.id),
      referenceIds: [],
      substituteId: '',
      contact: '',
      attachments: [],
    },
  );
  const [receivedAt] = useState(() => dayKey(new Date(document?.createdAt || Date.now())));
  const [fileError, setFileError] = useState('');
  const [fileBusy, setFileBusy] = useState(false);
  const [comment, setComment] = useState('');
  const [lineEditing, setLineEditing] = useState(false);
  const [submitError, setSubmitError] = useState('');
  function moveApprover(index, offset) {
    const next = [...draft.approverIds];
    [next[index], next[index + offset]] = [next[index + offset], next[index]];
    field('approverIds', next);
  }
  const field = (key, value) => setDraft((previous) => ({ ...previous, [key]: value }));
  const author = readonly ? document.member : user;
  async function attach(files) {
    setFileError('');
    if (files.length > 3 || [...files].reduce((n, f) => n + f.size, 0) > 1024 * 1024) {
      setFileError('파일은 총 1MB 이하, 최대 3개까지 선택해주세요.');
      return;
    }
    try {
      setFileBusy(true);
      const attachments = await Promise.all(
        [...files].map(
          (f) =>
            new Promise((resolve, reject) => {
              const reader = new FileReader();
              reader.onload = () => resolve({ name: f.name, data: reader.result });
              reader.onerror = () => reject(new Error('파일을 읽지 못했습니다.'));
              reader.readAsDataURL(f);
            }),
        ),
      );
      field('attachments', attachments);
    } catch (e) {
      setFileError(e.message);
    } finally {
      setFileBusy(false);
    }
  }
  const line = [
    author,
    ...draft.approverIds.map((id) => data.members.find((m) => m.id === id)),
  ].filter(Boolean);
  return (
    <div className="approval-compose">
      <div className="approval-compose-main">
        <div className="portal-page-heading">
          <div>
            <h1>{readonly ? '전자결재 문서 상세' : draft.template}</h1>
            <span>
              {readonly
                ? '신청 내용과 결재 진행 상황을 확인하세요.'
                : '결재선 확인 → 신청 내용 입력 → 상신 · * 필수 항목'}
            </span>
          </div>
          <button disabled={busy || fileBusy} onClick={back}>
            ← 전자결재 홈
          </button>
        </div>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            if (busy || fileError || fileBusy) return;
            const status = e.nativeEvent.submitter?.value || 'pending';
            if (
              status === 'pending' &&
              (!draft.approverIds.length || draft.approverIds.some((id) => !id))
            ) {
              setLineEditing(true);
              setSubmitError('결재자를 1명 이상 선택하고 빈 결재자 항목을 확인해주세요.');
              return;
            }
            if (draft.endDate < draft.startDate) {
              setSubmitError('종료일은 시작일과 같거나 이후여야 합니다.');
              return;
            }
            if (status === 'pending' && (!draft.title.trim() || !draft.reason.trim())) {
              setSubmitError('기안 제목과 목적 및 사유를 입력해주세요.');
              return;
            }
            setSubmitError('');
            save({ ...draft, approverIds: draft.approverIds.filter(Boolean), status });
          }}
        >
          <fieldset disabled={busy || readonly}>
            <Panel
              title="1. 결재선 확인"
              action={
                !readonly ? (
                  <button
                    type="button"
                    aria-expanded={lineEditing}
                    aria-controls="approval-line-editor"
                    onClick={() => setLineEditing(!lineEditing)}
                  >
                    {lineEditing ? '설정 닫기' : '결재선 설정'}
                  </button>
                ) : (
                  <span className="muted">접수일: {receivedAt}</span>
                )
              }
            >
              <p className="approval-hint">
                {readonly
                  ? '지정된 순서대로 결재가 진행됩니다.'
                  : '같은 부서의 결재자가 기본 지정됩니다. 담당자와 결재 순서를 확인해주세요. (최대 5명)'}
              </p>
              <div className="approval-line-cards">
                {line.map((m, i) => (
                  <div className={i ? 'approver' : ''} key={`${m.id}-${i}`}>
                    <small>{i ? `결재 ${i}` : '기안'}</small>
                    <strong>
                      {m.name} {m.job_title}
                    </strong>
                    <span>{m.department}</span>
                  </div>
                ))}
              </div>
              {!readonly && lineEditing && (
                <div className="line-editor" id="approval-line-editor">
                  {draft.approverIds.map((id, i) => (
                    <div key={i}>
                      <EmployeeSelect
                        label={`결재자 ${i + 1}`}
                        members={data.members}
                        value={id}
                        exclude={[user.id, ...draft.approverIds.filter((_, index) => index !== i)]}
                        onChange={(value) =>
                          field(
                            'approverIds',
                            draft.approverIds.map((old, index) => (index === i ? value : old)),
                          )
                        }
                      />
                      <button
                        type="button"
                        disabled={i === 0}
                        aria-label={`결재자 ${i + 1} 순서 앞으로`}
                        onClick={() => moveApprover(i, -1)}
                      >
                        ↑
                      </button>
                      <button
                        type="button"
                        disabled={i === draft.approverIds.length - 1}
                        aria-label={`결재자 ${i + 1} 순서 뒤로`}
                        onClick={() => moveApprover(i, 1)}
                      >
                        ↓
                      </button>
                      <button
                        type="button"
                        aria-label={`결재자 ${i + 1} 삭제`}
                        onClick={() =>
                          field(
                            'approverIds',
                            draft.approverIds.filter((_, index) => index !== i),
                          )
                        }
                      >
                        <IconX size={16} aria-hidden="true" />
                      </button>
                    </div>
                  ))}
                  <button
                    type="button"
                    disabled={draft.approverIds.length >= 5}
                    onClick={() => field('approverIds', [...draft.approverIds, ''])}
                  >
                    + 결재자 추가
                  </button>
                </div>
              )}
            </Panel>
            <Panel
              title="2. 신청 내용"
              action={
                data.annualLeave != null ? (
                  <span className="muted">잔여 연차: {data.annualLeave}</span>
                ) : null
              }
            >
              <div className="form-grid">
                <label>
                  서식
                  <select
                    value={draft.template}
                    onChange={(e) =>
                      setDraft((previous) => ({
                        ...previous,
                        template: e.target.value,
                        title:
                          previous.title === previous.template ? e.target.value : previous.title,
                      }))
                    }
                  >
                    {data.templates.map((t) => (
                      <option key={t}>{t}</option>
                    ))}
                  </select>
                </label>
                <label>
                  기안 제목 *
                  <input
                    required
                    maxLength={150}
                    value={draft.title}
                    onChange={(e) => field('title', e.target.value)}
                  />
                </label>
                <label>
                  부서명
                  <input value={author.department} readOnly />
                </label>
                <label>
                  성명 / 직위
                  <input value={`${author.name} / ${author.job_title}`} readOnly />
                </label>
              </div>
              <div className="request-types">
                {requestTypes.map((t, i) => (
                  <button
                    type="button"
                    className={draft.requestType === t ? 'selected' : ''}
                    aria-pressed={draft.requestType === t}
                    key={t}
                    onClick={() => field('requestType', t)}
                  >
                    <span>
                      {i === 0 ? (
                        <IconPlane size={24} aria-hidden="true" />
                      ) : i < 4 ? (
                        <IconClock size={24} aria-hidden="true" />
                      ) : (
                        <IconFileText size={24} aria-hidden="true" />
                      )}
                    </span>
                    {t}
                  </button>
                ))}
              </div>
            </Panel>
            <Panel title="사유 입력">
              <div className="form-grid">
                <label>
                  시작일 *
                  <input
                    type="date"
                    required
                    value={draft.startDate}
                    onChange={(e) =>
                      setDraft((previous) => ({
                        ...previous,
                        startDate: e.target.value,
                        endDate:
                          previous.endDate < e.target.value ? e.target.value : previous.endDate,
                      }))
                    }
                  />
                </label>
                <label>
                  종료일 *
                  <input
                    type="date"
                    required
                    min={draft.startDate}
                    value={draft.endDate}
                    onChange={(e) => field('endDate', e.target.value)}
                  />
                </label>
                <label className="full-field">
                  목적 및 사유 *
                  <textarea
                    required
                    maxLength={10000}
                    value={draft.reason}
                    onChange={(e) => field('reason', e.target.value)}
                    placeholder="신청 사유를 입력해주세요."
                  />
                </label>
                <EmployeeSelect
                  label="업무 대행자 (선택)"
                  members={data.members}
                  value={draft.substituteId}
                  exclude={[author.id]}
                  onChange={(value) => field('substituteId', value)}
                />
                <label>
                  비상 연락처 (선택)
                  <input
                    maxLength={100}
                    value={draft.contact}
                    onChange={(e) => field('contact', e.target.value)}
                  />
                </label>
              </div>
            </Panel>
            <Panel title="참조자 추가 (선택)">
              <p className="approval-hint">
                참조자는 문서를 확인할 수 있으며 결재 순서에는 포함되지 않습니다.
              </p>
              <div className="form-grid">
                {[0, 1].map((i) => (
                  <EmployeeSelect
                    key={i}
                    label={`참조자 ${i + 1}`}
                    members={data.members}
                    value={draft.referenceIds[i]}
                    exclude={[author.id, ...draft.referenceIds.filter((_, index) => index !== i)]}
                    onChange={(value) => {
                      const next = [...draft.referenceIds];
                      next[i] = value;
                      field('referenceIds', next);
                    }}
                  />
                ))}
              </div>
            </Panel>
            <Panel title="증빙서류 (선택)">
              {!readonly && (
                <label>
                  공개 데모에서는 파일 첨부를 받지 않습니다.
                  <input
                    type="file"
                    multiple
                    disabled={true}
                    onChange={(e) => attach(e.target.files)}
                  />
                </label>
              )}
              {fileError && (
                <p className="portal-error" role="alert">
                  {fileError}
                </p>
              )}
              {draft.attachments?.map((a, i) => (
                <div className="attachment-row" key={i}>
                  {readonly ? (
                    <a href={a.data} download={a.name}>
                      {a.name} ↓
                    </a>
                  ) : (
                    <>
                      <span>{a.name}</span>
                      <button
                        type="button"
                        aria-label={`${a.name} 첨부 삭제`}
                        onClick={() =>
                          field(
                            'attachments',
                            draft.attachments.filter((_, index) => index !== i),
                          )
                        }
                      >
                        삭제
                      </button>
                    </>
                  )}
                </div>
              ))}
            </Panel>
          </fieldset>
          {!readonly && (
            <div className="approval-submit-bar">
              {submitError && (
                <p className="portal-error" role="alert">
                  {submitError}
                </p>
              )}
              <div className="approval-submit-content">
                <span className="approval-hint" role="status">
                  {fileBusy
                    ? '첨부파일을 읽는 중입니다…'
                    : busy
                      ? '문서를 저장하는 중입니다…'
                      : '작성 중에는 임시저장하고, 완료되면 상신하세요.'}
                </span>
                <div className="modal-actions">
                  <button
                    type="submit"
                    value="draft"
                    formNoValidate
                    disabled={busy || fileBusy || !!fileError}
                  >
                    {busy ? '저장 중…' : '임시저장'}
                  </button>
                  <button
                    type="submit"
                    className="primary"
                    value="pending"
                    disabled={busy || fileBusy || !!fileError}
                  >
                    {busy ? '처리 중…' : '상신하기'}
                  </button>
                </div>
              </div>
            </div>
          )}
        </form>
        {readonly && document.status === 'pending' && currentApprover(document) === user.id && (
          <Panel title="결재 처리">
            <label>
              검토 의견 / 반려 사유
              <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                maxLength={1000}
              />
            </label>
            <div className="modal-actions">
              <button
                disabled={busy || !comment.trim()}
                onClick={() => decide(document.id, 'reject', comment)}
              >
                반려
              </button>
              <button
                className="primary"
                disabled={busy}
                onClick={() => decide(document.id, 'approve', comment)}
              >
                승인
              </button>
            </div>
          </Panel>
        )}
      </div>
      <aside className="approval-timeline">
        <div className="approval-summary">
          <h3>신청 요약</h3>
          <strong>{draft.title || '제목 미입력'}</strong>
          <dl>
            <div>
              <dt>신청 유형</dt>
              <dd>{draft.requestType}</dd>
            </div>
            <div>
              <dt>신청 기간</dt>
              <dd>
                {draft.startDate || '미입력'} ~ {draft.endDate || '미입력'}
              </dd>
            </div>
            <div>
              <dt>첨부파일</dt>
              <dd>{draft.attachments?.length || 0}개</dd>
            </div>
          </dl>
        </div>
        <h3>
          결재선{' '}
          {readonly && <span className="status-pill">{approvalStatus[document.status]}</span>}
        </h3>
        {line.map((m, i) => {
          const decision = document?.decisions?.find((d) => d.memberId === m.id);
          return (
            <article key={`${m.id}-${i}`}>
              <div
                className={`avatar${decision?.action === 'reject' ? ' rejected' : i > 0 && decision?.action === 'approve' ? ' approved' : ''}`}
              >
                {m.name.slice(0, 1)}
              </div>
              <div>
                <strong>
                  {m.name} {m.job_title}
                </strong>
                <small>{m.department}</small>
                <small>
                  {i === 0
                    ? '기안'
                    : decision
                      ? decision.action === 'approve'
                        ? '승인'
                        : '반려'
                      : !readonly
                        ? '상신 후 결재 예정'
                        : currentApprover(document) === m.id && document.status === 'pending'
                          ? '현재 결재 차례'
                          : '결재 예정'}
                </small>
                {decision?.comment && (
                  <p
                    className={`approval-comment${decision.action === 'reject' ? ' rejected' : ''}`}
                  >
                    {decision.comment}
                  </p>
                )}
              </div>
            </article>
          );
        })}
      </aside>
    </div>
  );
}
