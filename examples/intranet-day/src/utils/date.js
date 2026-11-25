export const dayKey = (date = new Date()) =>
  new Intl.DateTimeFormat('sv-SE', { timeZone: 'Asia/Seoul' }).format(date);

export const time = (value) =>
  value
    ? new Date(value).toLocaleTimeString('ko-KR', { timeZone: 'Asia/Seoul', hour12: false })
    : '—';
