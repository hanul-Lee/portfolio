export function filterProjects(projects, filters) {
  return projects.filter(
    (p) =>
      ['type', 'division', 'year', 'serial'].every(
        (key) => !filters[key] || p[key] === filters[key],
      ) &&
      `${p.code} ${p.businessCode} ${p.name}`
        .toLowerCase()
        .includes(filters.query.trim().toLowerCase()),
  );
}
