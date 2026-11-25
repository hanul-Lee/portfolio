import { useState } from 'react';
import './App.scss';

export default function Members({ onExpired, members: providedMembers }) {
  const [members, setMembers] = useState([]);
  const [keyword, setKeyword] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const search = keyword.trim().toLowerCase();

  const allMembers = providedMembers || members;
  const filteredMembers = allMembers.filter((member) =>
    [member.id, member.name, member.email, member.department, member.job_title].some((value) =>
      String(value ?? '')
        .toLowerCase()
        .includes(search),
    ),
  );

  return (
    <div className="intranet">
      <header className="header">
        <div className="brand">ONDO</div>
        <span>개발 연습용 가상 인트라넷 · 개발용</span>
      </header>

      <div className="layout">
        <aside className="sidebar">
          <div className="sidebar-title">조직 관리</div>
          <div className="menu-active">직원 목록</div>
        </aside>

        <main className="content">
          <div className="page-heading">
            <div>
              <h1>직원 목록</h1>
              <p>가상 직원 데이터를 조회합니다.</p>
            </div>
            <span className="count-badge">전체 {allMembers.length}명</span>
          </div>

          <section className="card">
            <div className="toolbar">
              <label htmlFor="member-search">직원 검색</label>
              <input
                id="member-search"
                type="search"
                placeholder="이름, 사번, 부서, 직급, 이메일 검색"
                value={keyword}
                onChange={(event) => setKeyword(event.target.value)}
              />
              {}
            </div>

            {loading && !providedMembers ? (
              <p className="message">회원 목록을 불러오는 중입니다.</p>
            ) : error ? (
              <p className="message error" role="alert">
                {error}
              </p>
            ) : (
              <div className="table-wrap">
                <table>
                  <caption className="sr-only">직원 목록</caption>
                  <thead>
                    <tr>
                      <th scope="col">사번</th>
                      <th scope="col">이름</th>
                      <th scope="col">부서</th>
                      <th scope="col">직급</th>
                      <th scope="col">이메일</th>
                      <th scope="col">권한</th>
                      <th scope="col">가입일</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredMembers.map((member) => (
                      <tr key={member.id}>
                        <td>{member.id}</td>
                        <td className="member-name">{member.name}</td>
                        <td>{member.department}</td>
                        <td>{member.job_title}</td>
                        <td>{member.email}</td>
                        <td>
                          <span className={member.role === 'Admin' ? 'role admin' : 'role'}>
                            {member.role === 'Admin' ? '관리자' : '일반 사용자'}
                          </span>
                        </td>
                        <td>{member.joined_at}</td>
                      </tr>
                    ))}
                    {filteredMembers.length === 0 && (
                      <tr>
                        <td colSpan={7} className="message">
                          검색 결과가 없습니다.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </main>
      </div>
    </div>
  );
}
