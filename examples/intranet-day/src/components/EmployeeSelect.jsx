import { useState } from 'react';

export default function EmployeeSelect({
  label,
  members,
  value,
  onChange,
  required = false,
  disabled = false,
  exclude = [],
}) {
  const [search, setSearch] = useState('');
  const options = members.filter(
    (m) =>
      !exclude.includes(m.id) &&
      (m.id === value ||
        `${m.name} ${m.department} ${m.job_title} ${m.id}`
          .toLowerCase()
          .includes(search.toLowerCase())),
  );
  return (
    <div className="employee-select">
      <label>
        {label}
        {}
        <select
          aria-label={label}
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          required={required}
          disabled={disabled}
        >
          <option value="">직원을 선택해주세요.</option>
          {options.map((m) => (
            <option key={m.id} value={m.id}>
              {m.name} · {m.job_title} · {m.department} ({m.id})
            </option>
          ))}
        </select>
      </label>
    </div>
  );
}
