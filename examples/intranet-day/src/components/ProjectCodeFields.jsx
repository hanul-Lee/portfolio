import { useCallback, useState } from 'react';
import Modal from './Modal';

import { filterProjects } from '../utils/projects';

export function CodeSearch({ projects, activities, value, select, close }) {
  const empty = { type: '', division: '', year: '', serial: '', query: '' };
  const [filters, setFilters] = useState(empty);
  const [applied, setApplied] = useState(empty);
  const [project, setProject] = useState(projects.find((p) => p.code === value.code));
  const [activity, setActivity] = useState(
    activities.find((a) => `${a.code}.${a.name}` === value.activity),
  );
  const rows = filterProjects(projects, applied);
  return (
    <Modal title="코드검색" close={close} className="code-search-modal">
      <h2>코드검색</h2>
      <form
        className="code-filters"
        onSubmit={(e) => {
          e.preventDefault();
          setApplied(filters);
        }}
      >
        {['type', 'division', 'year', 'serial'].map((key, i) => (
          <label key={key}>
            {['사업종류', '사업부문', '사업연도', '일련번호'][i]}
            <select
              value={filters[key]}
              onChange={(e) => setFilters({ ...filters, [key]: e.target.value })}
            >
              <option value="">전체</option>
              {[...new Set(projects.map((p) => p[key]))].map((v) => (
                <option key={v}>{v}</option>
              ))}
            </select>
          </label>
        ))}
        <label>
          프로젝트 코드 / 명
          <input
            value={filters.query}
            onChange={(e) => setFilters({ ...filters, query: e.target.value })}
            placeholder="코드 또는 프로젝트명"
          />
        </label>
        <button className="primary">검색</button>
        <button
          type="button"
          onClick={() => {
            setFilters(empty);
            setApplied(empty);
          }}
        >
          새로고침
        </button>
      </form>
      <div className="code-tables">
        <section>
          <h3>
            1. 프로젝트 코드 <small>{rows.length}건</small>
          </h3>
          <div className="code-table-scroll">
            <table>
              <thead>
                <tr>
                  <th>신규코드</th>
                  <th>사업코드</th>
                  <th>약칭</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((p) => (
                  <tr key={p.id} className={project?.code === p.code ? 'selected' : ''}>
                    <td>
                      <button
                        type="button"
                        aria-pressed={project?.code === p.code}
                        onClick={() => setProject(p)}
                      >
                        {p.code}
                      </button>
                    </td>
                    <td>
                      <button type="button" onClick={() => setProject(p)}>
                        {p.businessCode}
                      </button>
                    </td>
                    <td>
                      <button type="button" onClick={() => setProject(p)}>
                        {p.name}
                      </button>
                    </td>
                  </tr>
                ))}
                {!rows.length && (
                  <tr>
                    <td colSpan={3}>검색 결과가 없습니다.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>
        <section>
          <h3>2. Activity 코드</h3>
          <div className="code-table-scroll">
            <table>
              <thead>
                <tr>
                  <th>코드</th>
                  <th>명칭</th>
                  <th>비고</th>
                </tr>
              </thead>
              <tbody>
                {activities.map((a) => (
                  <tr key={a.id} className={activity?.code === a.code ? 'selected' : ''}>
                    <td>
                      <button
                        type="button"
                        aria-pressed={activity?.code === a.code}
                        onClick={() => setActivity(a)}
                      >
                        {a.code}
                      </button>
                    </td>
                    <td>
                      <button type="button" onClick={() => setActivity(a)}>
                        {a.name}
                      </button>
                    </td>
                    <td>
                      <button type="button" onClick={() => setActivity(a)} title={a.description}>
                        {a.description}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
      <div className="flex">
        <div className="code-selection">
          선택: {project?.name || '프로젝트를 선택하세요'} ·{' '}
          {activity?.name || 'Activity를 선택하세요'}
        </div>
        <div className="modal-actions">
          <button type="button" onClick={close}>
            취소
          </button>
          <button
            type="button"
            className="primary"
            disabled={!project || !activity}
            onClick={() => {
              select({
                code: project.code,
                project: project.name,
                activity: `${activity.code}.${activity.name}`,
              });
              close();
            }}
          >
            선택 적용
          </button>
        </div>
      </div>

    </Modal>
  );
}

export default function ProjectCodeFields({
  value,
  onChange,
  projects,
  activities,
  required = true,
}) {
  const [open, setOpen] = useState(false);
  const close = useCallback(() => setOpen(false), []);
  return (
    <>
      {[
        ['프로젝트 코드', 'code'],
        ['Activity', 'activity'],
      ].map(([label, key]) => (
        <label key={key}>
          {label}
          <input
            className="code-picker-input"
            required={required}
            readOnly
            aria-label={`${label} 선택`}
            placeholder={`${label} 선택 ⌕`}
            value={value[key] || ''}
            onClick={() => setOpen(true)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                setOpen(true);
              }
            }}
          />
        </label>
      ))}
      {open && (
        <CodeSearch
          projects={projects}
          activities={activities}
          value={value}
          select={(selection) => onChange({ ...value, ...selection })}
          close={close}
        />
      )}
    </>
  );
}
