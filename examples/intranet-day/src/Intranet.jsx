import { useCallback, useEffect, useState } from 'react';
import {
  IconHome,
  IconFileCheck,
  IconNews,
  IconListDetails,
  IconClock,
  IconUsers,
  IconBuilding,
  IconCar,
  IconDeviceLaptop,
  IconArrowUpRight,
  IconRefresh,
  IconCheck,
} from '@tabler/icons-react';
import Members from './Members';
import './intranet.scss';
import Logo from './components/Logo';
import Panel from './components/Panel';
import Modal from './components/Modal';
import TaskEditor from './components/TaskEditor';
import ProjectCodeFields from './components/ProjectCodeFields';
import { ApprovalHome, ApprovalDocument } from './components/Approvals';
import useWorkspace from './hooks/useWorkspace';
import { dayKey, time } from './utils/date';
import { approvalBuckets, approvalStatus } from './utils/approvals';

export default function Intranet({ user, onLogout, loggingOut, error, onExpired, initialData }) {
  const {
    data,
    loading,
    busy,
    error: dataError,
    refresh,
    mutate,
  } = useWorkspace(onExpired, initialData);
  const [page, setPage] = useState('메인');
  const [now, setNow] = useState(new Date());
  const [modal, setModal] = useState(null);
  const [editor, setEditor] = useState(null);
  const [pendingPage, setPendingPage] = useState(null);
  const [notice, setNotice] = useState('');
  const [category, setCategory] = useState('전체');
  const [search, setSearch] = useState('');
  const [boardPage, setBoardPage] = useState(0);
  const [noticeTab, setNoticeTab] = useState('공지사항');
  const [approvalTab, setApprovalTab] = useState(0);
  const [period, setPeriod] = useState('주간');
  const [calendar, setCalendar] = useState(() => new Date(`${dayKey().slice(0, 7)}-01T12:00:00`));
  const [scheduleTab, setScheduleTab] = useState('팀일정');
  const [attendanceMonth, setAttendanceMonth] = useState(dayKey().slice(0, 7));
  const [quick, setQuick] = useState({ code: '', activity: '', reviewerId: '', body: '' });
  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);
  useEffect(() => {
    if (!notice) return;
    const timer = setTimeout(() => setNotice(''), 4000);
    return () => clearTimeout(timer);
  }, [notice]);
  const today = dayKey(now),
    record = data.records[today] || {};
  const tasks = data.tasks.filter((t) => t.date === today);
  const sortedPosts = [...data.posts].sort((a, b) => b.createdAt - a.createdAt);
  const filtered = sortedPosts.filter(
    (p) =>
      (category === '전체' || p.category === category) &&
      `${p.title} ${p.body} ${p.author}`.toLowerCase().includes(search.toLowerCase()),
  );
  const elapsed = record.in
    ? Math.max(0, Math.floor(((record.out || now.getTime()) - record.in) / 1000))
    : 0;
  const duration = (seconds) =>
    `${String(Math.floor(seconds / 3600)).padStart(2, '0')}:${String(Math.floor((seconds % 3600) / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
  const close = useCallback(() => {
    setModal(null);
    setPendingPage(null);
  }, []);
  function navigate(next) {
    if (!record.in) {
      setPendingPage(next);
      setModal({ type: 'checkin' });
    } else {
      setPage(next);
      setSearch('');
      setBoardPage(0);
    }
  }
  function guard(action) {
    if (!record.in) setModal({ type: 'checkin' });
    else action();
  }
  async function write(endpoint, input, message) {
    if (await mutate(endpoint, input)) {
      if (message) setNotice(message);
      return true;
    }
    return false;
  }
  async function checkin() {
    if (
      await write('attendance', { action: 'checkin' }, '출근 처리되었습니다. 좋은 하루 보내세요!')
    ) {
      setModal(null);
      if (pendingPage) setPage(pendingPage);
      setPendingPage(null);
    }
  }
  const more = (next) => (
    <button className="text-button" onClick={() => navigate(next)}>
      더보기 →
    </button>
  );
  const blankTask = { code: '', activity: '', project: '', reviewerId: '', body: '', hours: '1' };
  async function addTask(e) {
    e.preventDefault();
    if (!record.in) return guard(() => {});
    if (
      await write(
        'tasks',
        { tasks: [{ ...quick, project: quick.project || quick.code, hours: '1' }] },
        '업무가 추가되었습니다.',
      )
    )
      setQuick({ code: '', activity: '', reviewerId: '', body: '' });
  }
  const attendanceRows = Object.entries(data.records)
    .filter(([date]) => date.startsWith(attendanceMonth))
    .sort(([a], [b]) => b.localeCompare(a));
  const monthHours =
    attendanceRows.reduce(
      (n, [date, r]) => n + (r.out ? r.out - r.in : date === today ? now.getTime() - r.in : 0),
      0,
    ) / 3600000;
  const buckets = approvalBuckets(data.approvals, user.id);
  function compose(template, doc) {
    setEditor({ template, document: doc });
    navigate('전자결재 문서작성');
  }
  function view(doc) {
    setEditor({ template: doc.template, document: doc });
    navigate('전자결재 문서작성');
  }
  const currentDocument = editor?.document
    ? data.approvals.find((d) => d.id === editor.document.id) || editor.document
    : undefined;
  const weekStart = dayKey(new Date(now.getTime() - 6 * 86400000));
  const periodTasks = data.tasks.filter((t) =>
    period === '주간'
      ? t.date >= weekStart && t.date <= today
      : t.date.startsWith(today.slice(0, 7)),
  );
  const totalHours = periodTasks.reduce((n, t) => n + Number(t.hours), 0);
  const chart =
    period === '주간'
      ? Array.from({ length: 7 }, (_, i) => {
          const date = dayKey(new Date(now.getTime() - (6 - i) * 86400000));
          return {
            label: date.slice(-2),
            hours: data.tasks
              .filter((t) => t.date === date)
              .reduce((n, t) => n + Number(t.hours), 0),
          };
        })
      : Array.from({ length: 6 }, (_, i) => {
          const month = new Date(now.getFullYear(), now.getMonth() - 5 + i, 1);
          const prefix = dayKey(month).slice(0, 7);
          return {
            label: String(month.getMonth() + 1),
            hours: data.tasks
              .filter((t) => t.date.startsWith(prefix))
              .reduce((n, t) => n + Number(t.hours), 0),
          };
        });
  const projects = [...new Set(periodTasks.map((t) => t.project))].map((name) => ({
    name,
    tasks: periodTasks.filter((t) => t.project === name),
  }));
  const calendarYear = calendar.getFullYear(),
    calendarMonth = calendar.getMonth();
  const calendarCells = [
    ...Array(new Date(calendarYear, calendarMonth, 1).getDay()).fill(null),
    ...Array.from(
      { length: new Date(calendarYear, calendarMonth + 1, 0).getDate() },
      (_, i) => i + 1,
    ),
  ];
  const events = data.events.filter(
    (e) =>
      e.date?.startsWith(`${calendarYear}-${String(calendarMonth + 1).padStart(2, '0')}`) &&
      (scheduleTab === '사내일정'
        ? e.scope === 'company'
        : e.scope === 'team' && e.department === user.department),
  );
  const nextWeek = dayKey(new Date(now.getTime() + 7 * 86400000));
  const teamLeaves = [...(data.teamLeaves || [])].sort(
    (a, b) => a.startDate.localeCompare(b.startDate) || a.name.localeCompare(b.name, 'ko'),
  );
  const leaveGroups = [
    {
      title: '오늘 휴가자',
      leaves: teamLeaves.filter((leave) => leave.startDate <= today && leave.endDate >= today),
    },
    {
      title: '일주일 이내 휴가 예정자',
      leaves: teamLeaves.filter((leave) => leave.startDate > today && leave.startDate <= nextWeek),
    },
  ];
  return (
    <div className={`portal ${page === '메인' ? 'portal-home' : ''}`}>
      <header className="portal-header">
        <Logo
          onHome={() => {
            setPage('메인');
            setModal(null);
            setEditor(null);
            setPendingPage(null);
          }}
        />
        <div className="header-tools">
          <button onClick={() => navigate('최신글')}>최신글</button>
          <button onClick={() => navigate('직원 목록')}>직원 검색</button>
          <button disabled={loggingOut} onClick={onLogout}>
            {loggingOut ? '로그아웃 중…' : '로그아웃'}
          </button>
        </div>
      </header>
      <div className="portal-layout">
        <nav className="portal-nav" aria-label="주 메뉴">
          {[
            ['메인', IconHome, 'HOME'],
            ['전자결재', IconFileCheck, '전자결재'],
            ['최신글', IconNews, '최신글'],
            ['게시판', IconListDetails, '게시판'],
            ['근태', IconClock, '근태'],
            ['직원 목록', IconUsers, '팀관리'],
          ].map(([key, NavIcon, label]) => (
            <button
              key={key}
              className={
                page === key || (key === '전자결재' && page === '전자결재 문서작성') ? 'active' : ''
              }
              onClick={() => navigate(key)}
            >
              <NavIcon size={21} stroke={1.8} aria-hidden="true" />
              {label}
            </button>
          ))}
        </nav>
        <main
          className="portal-content"
          onClickCapture={(e) => {
            if (
              !record.in &&
              e.target.closest('button,input,select,textarea,a') &&
              !e.target.closest('[data-attendance]')
            ) {
              e.preventDefault();
              e.stopPropagation();
              setModal({ type: 'checkin' });
            }
          }}
        >
          {(error || dataError) && (
            <p role="alert" className="portal-error">
              {error || dataError}
              <button data-attendance onClick={refresh}>
                다시 불러오기
              </button>
            </p>
          )}
          {loading ? (
            <p className="message" role="status">
              가상 직원과 업무 데이터를 불러오는 중입니다.
            </p>
          ) : page === '메인' ? (
            <div className="dashboard">
              <aside className="dashboard-left">
                <section className="profile-card">
                  <div className="avatar">{user.name.slice(0, 1)}</div>
                  <div>
                    <h2>
                      {user.name} {user.job_title}
                    </h2>
                    <p>
                      {user.department} · {user.id}
                    </p>
                  </div>
                </section>
                <Panel title="오늘의 근무" className="work-card">
                  <div className="work-buttons" data-attendance>
                    <button
                      className="primary"
                      disabled={busy || !!record.out}
                      onClick={() => (record.in ? setModal({ type: 'checkout' }) : checkin())}
                    >
                      {record.out ? '퇴근 완료' : record.in ? '퇴근' : '출근'}
                    </button>
                    <button
                      disabled={busy || !record.in || !!record.out}
                      onClick={() =>
                        write('attendance', { action: 'overtime' }, '연장근무 상태를 변경했습니다.')
                      }
                    >
                      {record.overtime ? '연장근무 종료' : '연장근무'}
                    </button>
                    <select
                      aria-label="근무 상태"
                      disabled={busy || !record.in || !!record.out}
                      value={record.status || '근무'}
                      onChange={(e) =>
                        write('attendance', { action: 'status', status: e.target.value })
                      }
                    >
                      {['근무', '출장', '외근'].map((s) => (
                        <option key={s}>{s}</option>
                      ))}
                    </select>
                  </div>
                  <dl className="detail-list">
                    <dt>출근시간</dt>
                    <dd>{time(record.in)}</dd>
                    <dt>누적시간</dt>
                    <dd className="blue">{duration(elapsed)}</dd>
                    <dt>퇴근시간</dt>
                    <dd>{time(record.out)}</dd>
                    <dt>접속 디바이스</dt>
                    <dd>Web browser</dd>
                  </dl>
                  <div className="section-divider" />
                  <div className="panel-heading">
                    <h2>
                      오늘의 일정<sup>▪</sup>
                    </h2>
                    {more('근태')}
                  </div>
                  <form className="quick-task" onSubmit={addTask}>
                    <div className="two-fields">
                      <ProjectCodeFields
                        value={quick}
                        onChange={setQuick}
                        projects={data.projects}
                        activities={data.activities}
                      />
                    </div>
                    <label>
                      업무 검토자
                      <select
                        required
                        value={quick.reviewerId}
                        onChange={(e) => setQuick({ ...quick, reviewerId: e.target.value })}
                      >
                        <option value="">직원 선택</option>
                        {data.members.map((m) => (
                          <option key={m.id} value={m.id}>
                            {m.name} · {m.department}
                          </option>
                        ))}
                      </select>
                    </label>
                    <label>
                      업무 내용
                      <input
                        required
                        placeholder="업무 내용 입력"
                        value={quick.body}
                        onChange={(e) => setQuick({ ...quick, body: e.target.value })}
                      />
                    </label>
                    <div className="two-fields">
                      <button className="primary" disabled={busy}>
                        업무 추가
                      </button>
                      <button
                        type="button"
                        onClick={() =>
                          guard(() => setModal({ type: 'task', task: tasks[0] || blankTask }))
                        }
                      >
                        업무 수정
                      </button>
                    </div>
                  </form>
                  <div className="task-list">
                    {tasks.slice(0, 1).map((t) => (
                      <button
                        key={t.id}
                        onClick={() => guard(() => setModal({ type: 'task', task: t }))}
                      >
                        <strong>{t.hours}h</strong>
                        <span>
                          {t.body}
                          <small>
                            {t.project} · 검토: {t.reviewer}
                          </small>
                        </span>
                      </button>
                    ))}
                    {!tasks.length && <p className="muted">등록된 업무가 없습니다.</p>}
                  </div>
                </Panel>
                <Panel title="바로가기">
                  <div className="shortcut-list">
                    {['게시판', '전자결재', '직원 목록'].map((s) => (
                      <button key={s} onClick={() => navigate(s)}>
                        {s}
                        <IconArrowUpRight size={16} aria-hidden="true" />
                      </button>
                    ))}
                  </div>
                </Panel>
              </aside>
              <div className="dashboard-main">
                <div className="dashboard-top">
                  <Panel title="전자결재" action={more('전자결재')}>
                    <div className="tabs">
                      {['기안 문서', '결재대기', '반려'].map((s, i) => (
                        <button
                          key={s}
                          className={approvalTab === i ? 'selected' : ''}
                          onClick={() => setApprovalTab(i)}
                        >
                          {s} <b>{buckets[i].length}</b>
                        </button>
                      ))}
                    </div>
                    <div className="approval-list">
                      {buckets[approvalTab].slice(0, 3).map((doc) => (
                        <button
                          key={doc.id}
                          onClick={() =>
                            doc.status === 'draft' ? compose(doc.template, doc) : view(doc)
                          }
                        >
                          <span>
                            [{doc.template}] {doc.title}
                            <small> | {doc.author}</small>
                          </span>
                          <em>{approvalStatus[doc.status]}</em>
                        </button>
                      ))}
                      {!buckets[approvalTab].length && (
                        <p className="muted">해당 문서가 없습니다.</p>
                      )}
                    </div>
                  </Panel>
                  <Panel
                    title="MY MANHOUR"
                    action={
                      <div className="mini-tabs">
                        {['주간', '월간'].map((p) => (
                          <button
                            key={p}
                            className={period === p ? 'selected' : ''}
                            onClick={() => setPeriod(p)}
                          >
                            {p}
                          </button>
                        ))}
                      </div>
                    }
                  >
                    <div className="manhour-layout">
                      <div>
                        <p className="muted">
                          {period} 업무 등록시간 <strong className="blue">{totalHours}h</strong> /{' '}
                          {period === '주간' ? 40 : 160}h
                        </p>
                        <div className="progress">
                          <span
                            style={{
                              width: `${Math.min(100, (totalHours / (period === '주간' ? 40 : 160)) * 100)}%`,
                            }}
                          />
                        </div>
                        <div className="hour-stats">
                          <span>
                            연장근무<strong>{record.overtime ? '진행 중' : '미진행'}</strong>
                          </span>
                          <span>
                            남은 연차<strong>{data.annualLeave ?? '미등록'}</strong>
                          </span>
                        </div>
                        <div className="bar-chart" aria-label={`${period} 등록 업무시간 차트`}>
                          {chart.map((c, i) => (
                            <div key={i} title={`${c.label}: ${c.hours}시간`}>
                              <span
                                style={{
                                  height: `${(c.hours / Math.max(8, ...chart.map((v) => v.hours))) * 100}%`,
                                }}
                              />
                              <small>{c.label}</small>
                            </div>
                          ))}
                        </div>
                      </div>
                      <div className="project-list">
                        {projects.slice(0, 1).map((p) => (
                          <article key={p.name}>
                            <div className="project-header">
                              <strong>{p.name}</strong>
                              <span className="hours-chip">
                                {p.tasks.reduce((n, t) => n + Number(t.hours), 0)}h
                              </span>
                              <button
                                onClick={() =>
                                  guard(() =>
                                    setModal({
                                      type: 'task',
                                      task: { ...p.tasks[0], id: undefined, body: '' },
                                    }),
                                  )
                                }
                              >
                                + 오늘 일정에 추가
                              </button>
                            </div>
                            {p.tasks.slice(0, 1).map((t) => (
                              <p key={t.id}>
                                <small>
                                  {t.date} · 검토 {t.reviewer}
                                </small>
                                {t.body}
                              </p>
                            ))}
                          </article>
                        ))}
                        {!projects.length && (
                          <p className="muted">등록된 프로젝트 업무가 없습니다.</p>
                        )}
                      </div>
                    </div>
                  </Panel>
                </div>
                <div className="dashboard-middle">
                  <Panel title="공지사항 및 소식" action={more('게시판')}>
                    <div className="tabs">
                      {['공지사항', '경조사알림'].map((c) => (
                        <button
                          key={c}
                          className={noticeTab === c ? 'selected' : ''}
                          onClick={() => setNoticeTab(c)}
                        >
                          {c === '공지사항' ? '사내공지' : c}
                        </button>
                      ))}
                    </div>
                    <div className="notice-list">
                      {sortedPosts
                        .filter((p) => p.category === noticeTab)
                        .slice(0, 3)
                        .map((p) => (
                          <button
                            key={p.id}
                            onClick={() => guard(() => setModal({ type: 'post', post: p }))}
                          >
                            <span>{p.title}</span>
                            <time>{p.date}</time>
                          </button>
                        ))}
                      {!sortedPosts.some((p) => p.category === noticeTab) && (
                        <p className="muted">등록된 소식이 없습니다.</p>
                      )}
                    </div>
                  </Panel>
                  <Panel title="팀원 현황" action={more('직원 목록')}>
                    <div className="team-subheading">
                      {user.department} · {data.team.length}명
                      <span>
                        {['근무', '외근', '출장', '퇴근', '미출근']
                          .map((s) => `${s} ${data.team.filter((m) => m.status === s).length}`)
                          .join(' · ')}
                      </span>
                    </div>
                    <div className="team-list">
                      {data.team.slice(0, 3).map((m) => (
                        <div className="team-row" key={m.id}>
                          <span>
                            {m.name} {m.job_title}
                          </span>
                          <span
                            className={
                              m.status === '근무'
                                ? 'green'
                                : m.status === '외근'
                                  ? 'purple'
                                  : 'muted'
                            }
                          >
                            ● {m.status}
                          </span>
                        </div>
                      ))}
                    </div>
                  </Panel>
                </div>
                <div className="dashboard-bottom">
                  <Panel
                    title="오늘의 식단"
                    action={
                      <button
                        className="text-button"
                        onClick={() => setModal({ type: 'info', title: '오늘의 식단' })}
                      >
                        전체
                      </button>
                    }
                  >
                    <div className="meal">
                      <strong>점심</strong>
                      {data.meals.length ? (
                        data.meals.slice(0, 3).map((m) => <span key={m.id}>{m.name}</span>)
                      ) : (
                        <span>등록된 식단이 없습니다.</span>
                      )}
                    </div>
                  </Panel>
                  <Panel title="나의 현황">
                    <dl className="detail-list">
                      <dt>소속 부서</dt>
                      <dd>{user.department}</dd>
                      <dt>기안 문서</dt>
                      <dd>{buckets[0].length}건</dd>
                      <dt>결재 대기</dt>
                      <dd className="blue">{buckets[1].length}건</dd>
                      <dt>예약</dt>
                      <dd>{data.reservations.length}건</dd>
                    </dl>
                  </Panel>
                  <Panel title="현황공유">
                    <div className="share-cards">
                      {[
                        [IconBuilding, '회의실 현황'],
                        [IconCar, '배차현황'],
                        [IconDeviceLaptop, '비품현황'],
                      ].map(([StatusIcon, s]) => (
                        <button
                          key={s}
                          onClick={() => guard(() => setModal({ type: 'info', title: s }))}
                        >
                          <StatusIcon size={22} stroke={1.8} aria-hidden="true" />
                          {s}
                        </button>
                      ))}
                    </div>
                  </Panel>
                  <Panel title="사내 SW">
                    <div className="software-cards">
                      {data.services.map((service) => (
                        <button
                          key={service.id}
                          onClick={() =>
                            guard(() => setModal({ type: 'info', title: service.name }))
                          }
                        >
                          {service.label}
                        </button>
                      ))}
                    </div>
                  </Panel>
                </div>
              </div>
              <aside className="dashboard-right">
                <Panel
                  title="캘린더"
                  action={
                    <div className="mini-tabs">
                      {['팀일정', '사내일정'].map((s) => (
                        <button
                          key={s}
                          className={scheduleTab === s ? 'selected' : ''}
                          onClick={() => setScheduleTab(s)}
                        >
                          {s}
                        </button>
                      ))}
                    </div>
                  }
                >
                  <div className="calendar-title">
                    <button
                      aria-label="이전 달"
                      onClick={() => setCalendar(new Date(calendarYear, calendarMonth - 1, 1))}
                    >
                      ‹
                    </button>
                    <strong>
                      {calendarYear}년 {calendarMonth + 1}월
                    </strong>
                    <button
                      aria-label="다음 달"
                      onClick={() => setCalendar(new Date(calendarYear, calendarMonth + 1, 1))}
                    >
                      ›
                    </button>
                  </div>
                  <div className="calendar-grid">
                    {'일월화수목금토'.split('').map((s, i) => (
                      <small key={s} className={i === 0 ? 'red' : i === 6 ? 'blue' : ''}>
                        {s}
                      </small>
                    ))}
                    {calendarCells.map((d, i) => (
                      <span
                        key={i}
                        className={`${i % 7 === 0 ? 'red' : i % 7 === 6 ? 'blue' : ''} ${d && `${calendarYear}-${String(calendarMonth + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}` === today ? 'today' : ''}`}
                      >
                        {d}
                      </span>
                    ))}
                  </div>
                  <div className="section-divider" />
                  {scheduleTab === '팀일정' &&
                    leaveGroups.map(({ title, leaves }) => (
                      <section key={title} aria-label={title}>
                        <h3>
                          {title} · {new Set(leaves.map((leave) => leave.memberId)).size}명
                        </h3>
                        {title === '일주일 이내 휴가 예정자' && (
                          <p className="muted">
                            내일부터 {nextWeek.slice(5).replace('-', '/')}까지
                          </p>
                        )}
                        {leaves.map((leave) => (
                          <div className="schedule" key={leave.id}>
                            <p>
                              <b>{leave.name}</b> · {leave.requestType}
                              <small>
                                {leave.startDate}
                                {leave.startDate !== leave.endDate ? ` ~ ${leave.endDate}` : ''}
                              </small>
                            </p>
                          </div>
                        ))}
                        {!leaves.length && (
                          <p className="muted">
                            {title === '오늘 휴가자'
                              ? '오늘 휴가자가 없습니다.'
                              : '일주일 이내 예정된 휴가가 없습니다.'}
                          </p>
                        )}
                        <div className="section-divider" />
                      </section>
                    ))}
                  <h3>{scheduleTab}</h3>
                  {events.slice(0, 2).map((e) => (
                    <div className="schedule" key={e.id}>
                      <strong>{e.date.slice(-2)}</strong>
                      <p>
                        {e.title}
                        <small>{e.time}</small>
                      </p>
                    </div>
                  ))}
                  {!events.length && <p className="muted">등록된 일정이 없습니다.</p>}
                </Panel>
              </aside>
            </div>
          ) : page === '전자결재' ? (
            <ApprovalHome data={data} user={user} compose={compose} view={view} />
          ) : page === '전자결재 문서작성' && editor ? (
            <ApprovalDocument
              key={editor.document?.id || editor.template}
              data={data}
              user={user}
              template={editor.template}
              document={currentDocument}
              busy={busy}
              back={() => setPage('전자결재')}
              save={async (draft) => {
                if (
                  await write(
                    'approvals',
                    {
                      ...draft,
                      approverIds: draft.approverIds.filter(Boolean),
                      referenceIds: draft.referenceIds.filter(Boolean),
                    },
                    draft.status === 'draft' ? '문서를 임시저장했습니다.' : '문서를 상신했습니다.',
                  )
                )
                  setPage('전자결재');
              }}
              decide={async (id, action, comment) => {
                if (
                  await write(
                    'decision',
                    { id, action, comment },
                    action === 'approve' ? '승인 처리했습니다.' : '반려 처리했습니다.',
                  )
                )
                  setPage('전자결재');
              }}
            />
          ) : page === '직원 목록' ? (
            <Members members={data.members} onExpired={onExpired} />
          ) : (
            <>
              <div className="portal-page-heading">
                <div>
                  <h1>{page}</h1>
                  <span>
                    {page === '근태'
                      ? '나의 출퇴근 기록과 근무 시간을 확인하세요.'
                      : 'DB에 연결된 직원들의 사내 소식을 확인하세요.'}
                  </span>
                </div>
                <span className="muted">{today}</span>
              </div>
              {page === '근태' ? (
                <>
                  <div className="attendance-summary">
                    <Panel title="오늘의 근무">
                      <strong className="summary-number">
                        {record.out ? '퇴근 완료' : record.in ? record.status : '출근 전'}
                      </strong>
                      <p>
                        출근 {time(record.in)} · 퇴근 {time(record.out)}
                      </p>
                      <button
                        data-attendance
                        className="primary"
                        disabled={busy || !!record.out}
                        onClick={() => (record.in ? setModal({ type: 'checkout' }) : checkin())}
                      >
                        {record.out ? '퇴근 완료' : record.in ? '퇴근하기' : '출근하기'}
                      </button>
                    </Panel>
                    <Panel title="오늘 누적 시간">
                      <strong className="summary-number blue">{duration(elapsed)}</strong>
                      <p>출근부터 퇴근까지의 기록 시간</p>
                    </Panel>
                    <Panel title="선택 월 누적 시간">
                      <strong className="summary-number">
                        {monthHours.toFixed(1)}
                        <small> 시간</small>
                      </strong>
                      <p>{attendanceRows.length}일 출근 기록</p>
                    </Panel>
                  </div>
                  <Panel
                    title="근태 기록"
                    action={
                      <input
                        aria-label="조회 월"
                        type="month"
                        value={attendanceMonth}
                        onChange={(e) => setAttendanceMonth(e.target.value)}
                      />
                    }
                  >
                    <div className="table-wrap">
                      <table>
                        <thead>
                          <tr>
                            {['날짜', '직원', '출근', '퇴근', '근무 시간', '상태'].map((s) => (
                              <th key={s}>{s}</th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {attendanceRows.map(([date, r]) => (
                            <tr key={date}>
                              <td>{date}</td>
                              <td>{user.name}</td>
                              <td>{time(r.in)}</td>
                              <td>{time(r.out)}</td>
                              <td>
                                {r.out
                                  ? duration(Math.floor((r.out - r.in) / 1000))
                                  : date === today
                                    ? duration(elapsed)
                                    : '퇴근 미기록'}
                              </td>
                              <td>{r.out ? '퇴근' : r.status}</td>
                            </tr>
                          ))}
                          {!attendanceRows.length && (
                            <tr>
                              <td colSpan={6} className="empty-state">
                                해당 월의 기록이 없습니다.
                              </td>
                            </tr>
                          )}
                        </tbody>
                      </table>
                    </div>
                  </Panel>
                </>
              ) : (
                <Panel
                  title={page === '최신글' ? '최신 게시글' : '사내 게시판'}
                  action={
                    <div className="board-actions">
                      <button disabled={busy} onClick={refresh}>
                        <IconRefresh size={16} aria-hidden="true" /> 최신글 불러오기
                      </button>
                      <button className="primary" onClick={() => setModal({ type: 'write' })}>
                        글쓰기
                      </button>
                    </div>
                  }
                >
                  <div className="board-toolbar">
                    <div className="tabs">
                      {['전체', '공지사항', '경조사알림', '자유게시판'].map((c) => (
                        <button
                          key={c}
                          className={category === c ? 'selected' : ''}
                          onClick={() => {
                            setCategory(c);
                            setBoardPage(0);
                          }}
                        >
                          {c}
                        </button>
                      ))}
                    </div>
                    <input
                      type="search"
                      aria-label="게시글 검색"
                      placeholder="제목, 내용, 작성자 검색"
                      value={search}
                      onChange={(e) => {
                        setSearch(e.target.value);
                        setBoardPage(0);
                      }}
                    />
                  </div>
                  <p className="result-count">
                    총 <strong>{filtered.length}</strong>개의 게시글
                  </p>
                  <div className="table-wrap">
                    <table className="board-table">
                      <thead>
                        <tr>
                          {['구분', '제목', '작성자 / 부서', '등록일'].map((s) => (
                            <th key={s}>{s}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {filtered.slice(boardPage * 6, boardPage * 6 + 6).map((p) => (
                          <tr key={p.id}>
                            <td>
                              <span className="status-pill">{p.category}</span>
                            </td>
                            <td>
                              <button
                                className="post-link"
                                onClick={() => guard(() => setModal({ type: 'post', post: p }))}
                              >
                                {p.title}
                              </button>
                              {p.demo && <small className="demo-tag">초기 테스트 데이터</small>}
                            </td>
                            <td>
                              {p.author}
                              <small className="member-department">{p.member?.department}</small>
                            </td>
                            <td>{p.date}</td>
                          </tr>
                        ))}
                        {!filtered.length && (
                          <tr>
                            <td colSpan={4} className="empty-state">
                              검색 결과가 없습니다.
                            </td>
                          </tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                  <div className="board-pagination">
                    <button disabled={!boardPage} onClick={() => setBoardPage(boardPage - 1)}>
                      이전
                    </button>
                    <span>
                      {boardPage + 1} / {Math.max(1, Math.ceil(filtered.length / 6))}
                    </span>
                    <button
                      disabled={(boardPage + 1) * 6 >= filtered.length}
                      onClick={() => setBoardPage(boardPage + 1)}
                    >
                      다음
                    </button>
                  </div>
                </Panel>
              )}
            </>
          )}
        </main>
      </div>
      <footer className="portal-footer">
        <span>© 2026 ONDO.</span>
        <span>개발 연습용 가상 인트라넷</span>
      </footer>
      {notice && (
        <div className="portal-toast" role="status">
          <IconCheck size={18} aria-hidden="true" /> {notice}
        </div>
      )}
      {modal?.type === 'checkin' && (
        <Modal title="출근 안내" close={close} className="checkin-modal">
          <Logo />
          <h2>
            금일 <span className="blue">출근 처리</span>를 완료해주세요.
          </h2>
          <p>
            {now.toLocaleString('ko-KR', {
              timeZone: 'Asia/Seoul',
              year: 'numeric',
              month: '2-digit',
              day: '2-digit',
              weekday: 'short',
              hour: '2-digit',
              minute: '2-digit',
              hour12: false,
            })}
          </p>
          <button className="primary" disabled={busy} onClick={checkin}>
            출근하기
          </button>
          {dataError && (
            <p className="portal-error" role="alert">
              {dataError}
            </p>
          )}
          <small>출근 후 업무 화면으로 이동합니다.</small>
        </Modal>
      )}
      {modal?.type === 'checkout' && (
        <Modal title="퇴근 확인" close={close}>
          <h2>퇴근 처리하시겠습니까?</h2>
          <p>
            오늘 누적 근무 시간 <strong>{duration(elapsed)}</strong>
          </p>
          {dataError && (
            <p className="portal-error" role="alert">
              {dataError}
            </p>
          )}
          <div className="modal-actions">
            <button disabled={busy} onClick={close}>
              취소
            </button>
            <button
              className="primary"
              disabled={busy}
              onClick={async () => {
                if (
                  await write(
                    'attendance',
                    { action: 'checkout' },
                    '퇴근 처리되었습니다. 수고하셨습니다!',
                  )
                )
                  close();
              }}
            >
              퇴근하기
            </button>
          </div>
        </Modal>
      )}
      {modal?.type === 'task' && (
        <TaskEditor
          task={modal.task}
          projects={data.projects}
          activities={data.activities}
          members={data.members}
          busy={busy}
          error={dataError}
          close={close}
          save={async (draft, extra) => {
            const changed = [draft];
            if (extra.body.trim()) changed.push({ ...draft, ...extra, id: undefined });
            if (await write('tasks', { tasks: changed }, '업무가 저장되었습니다.')) close();
          }}
        />
      )}
      {modal?.type === 'post' && (
        <Modal title="게시글 상세" close={close} className="post-modal">
          <span className="status-pill">{modal.post.category}</span>
          <h2>{modal.post.title}</h2>
          <p className="muted">
            {modal.post.author} · {modal.post.member?.department} · {modal.post.date}
          </p>
          <div className="post-body">{modal.post.body}</div>
          <div className="modal-actions">
            <button
              onClick={() => {
                close();
                setPage('게시판');
              }}
            >
              게시판으로
            </button>
            <button className="primary" onClick={close}>
              닫기
            </button>
          </div>
        </Modal>
      )}
      {modal?.type === 'write' && (
        <Modal title="게시글 작성" close={close}>
          <h2>
            게시글 작성<sup>▪</sup>
          </h2>
          <form
            className="post-form"
            onSubmit={async (e) => {
              e.preventDefault();
              const form = new FormData(e.currentTarget);
              if (
                await write(
                  'posts',
                  {
                    title: form.get('title').trim(),
                    body: form.get('body').trim(),
                    category: form.get('category'),
                  },
                  '게시글이 등록되었습니다.',
                )
              )
                close();
            }}
          >
            <label>
              작성자
              <input readOnly value={`${user.name} · ${user.department}`} />
            </label>
            <label>
              게시판
              <select name="category">
                {['공지사항', '경조사알림', '자유게시판'].map((s) => (
                  <option key={s}>{s}</option>
                ))}
              </select>
            </label>
            <label>
              제목
              <input
                name="title"
                required
                maxLength={150}
                pattern=".*\S.*"
                placeholder="제목을 입력해주세요."
              />
            </label>
            <label>
              내용
              <textarea
                name="body"
                required
                maxLength={10000}
                placeholder="공유할 소식을 작성해주세요."
              />
            </label>
            {dataError && (
              <p className="portal-error" role="alert">
                {dataError}
              </p>
            )}
            <div className="modal-actions">
              <button type="button" disabled={busy} onClick={close}>
                취소
              </button>
              <button className="primary" disabled={busy}>
                등록
              </button>
            </div>
          </form>
        </Modal>
      )}
      {modal?.type === 'info' && (
        <Modal title={modal.title} close={close}>
          <h2>{modal.title}</h2>
          <p className="muted">화면 확인용 가상 데이터입니다.</p>
          {modal.title === '오늘의 식단' ? (
            <div className="info-list">
              {data.meals.map((m) => (
                <p key={m.id}>{m.name}</p>
              ))}
            </div>
          ) : data.services.some((s) => s.name === modal.title) ? (
            <div className="info-list">
              {data.services
                .filter((s) => s.name === modal.title)
                .map((s) => (
                  <div key={s.id}>
                    <strong>
                      {s.requestNo} · {s.status}
                    </strong>
                    <p>{s.description}</p>
                    <small>{s.date}</small>
                  </div>
                ))}
            </div>
          ) : (
            <div className="table-wrap info-table">
              <table className="board-table">
                <thead>
                  <tr>
                    {['자원', '시간', '신청자', '목적', '상태'].map((v) => (
                      <th key={v}>{v}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {data.sharedReservations
                    .filter(
                      (r) =>
                        r.category ===
                        { '회의실 현황': '회의실', 배차현황: '차량', 비품현황: '비품' }[
                          modal.title
                        ],
                    )
                    .map((r) => (
                      <tr key={r.id}>
                        <td>{r.name}</td>
                        <td>{r.time}</td>
                        <td>
                          {r.author} · {r.member?.department}
                        </td>
                        <td>{r.purpose}</td>
                        <td>{r.status}</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          )}
          <div className="modal-actions">
            <button className="primary" onClick={close}>
              확인
            </button>
          </div>
        </Modal>
      )}
    </div>
  );
}
