export default function Logo({ onHome }) {
  const Tag = onHome ? 'button' : 'div';
  return (
    <Tag
      className="ondo-logo"
      onClick={onHome}
      {...(onHome ? { type: 'button', 'aria-label': 'ONDO 홈으로 이동' } : {})}
    >
      <img className="logo" src={`${import.meta.env.BASE_URL}logo.svg`} alt="온도워크" />

    </Tag>
  );
}
