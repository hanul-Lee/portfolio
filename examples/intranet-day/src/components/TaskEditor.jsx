import { useState } from 'react';
import Modal from './Modal';
import { dayKey } from '../utils/date';
import EmployeeSelect from './EmployeeSelect';
import ProjectCodeFields from './ProjectCodeFields';

export default function TaskEditor({
  task,
  save,
  close,
  members,
  projects,
  activities,
  busy,
  error,
}) {
  const [draft, setDraft] = useState(task);
  const [extra, setExtra] = useState({
    code: task.code,
    project: task.project,
    activity: task.activity,
    body: '',
    hours: '0.5',
  });
  const field = (label, key, source = draft, setter = setDraft) => (
    <label>
      {label}
      <input
        required
        value={source[key]}
        onChange={(e) => setter({ ...source, [key]: e.target.value })}
      />
    </label>
  );
  return (
    <Modal title="업무 수정" close={close} className="task-modal">
      <form
        onSubmit={(e) => {
          e.preventDefault();
          save(draft, extra);
        }}
      >
        <div className="panel-heading">
          <h2>
            업무 수정<sup>▪</sup>
          </h2>
          <span>업무일자: {dayKey()}</span>
        </div>
        <div className="form-grid">
          <ProjectCodeFields
            value={draft}
            onChange={setDraft}
            projects={projects}
            activities={activities}
          />
          {field('프로젝트 명칭', 'project')}
          <EmployeeSelect
            label="업무 검토자"
            members={members}
            value={draft.reviewerId}
            required
            onChange={(reviewerId) => setDraft({ ...draft, reviewerId })}
          />
          <label className="full-field">
            업무 내용
            <textarea
              required
              placeholder="업무 내용을 구체적으로 입력해주세요."
              value={draft.body}
              onChange={(e) => setDraft({ ...draft, body: e.target.value })}
            />
          </label>
          <label>
            작업 시간
            <select
              value={draft.hours}
              onChange={(e) => setDraft({ ...draft, hours: e.target.value })}
            >
              {['0.5', '1', '2', '4', '8'].map((h) => (
                <option key={h} value={h}>
                  {Number(h) * 60}분
                </option>
              ))}
            </select>
          </label>
        </div>
        <h2 className="extra-heading">
          추가 업무<sup>▪</sup>
        </h2>
        <div className="form-grid">
          <ProjectCodeFields
            value={extra}
            required={false}
            onChange={setExtra}
            projects={projects}
            activities={activities}
          />
          <label>
            업무 내용
            <input
              placeholder="추가 업무가 있을 때 입력"
              value={extra.body}
              onChange={(e) => setExtra({ ...extra, body: e.target.value })}
            />
          </label>
          <label>
            작업 시간
            <select
              value={extra.hours}
              onChange={(e) => setExtra({ ...extra, hours: e.target.value })}
            >
              {['0.5', '1', '2', '4', '8'].map((h) => (
                <option key={h} value={h}>
                  {Number(h) * 60}분
                </option>
              ))}
            </select>
          </label>
        </div>
        {error && (
          <p className="portal-error" role="alert">
            {error}
          </p>
        )}
        <div className="modal-actions">
          <button type="button" onClick={close}>
            취소
          </button>
          <button className="primary" disabled={busy}>
            저장
          </button>
        </div>
      </form>
    </Modal>
  );
}
