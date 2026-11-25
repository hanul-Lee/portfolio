export default function Panel({ title, children, action, className = '' }) {
  return (
    <section className={`dash-panel ${className}`}>
      <div className="panel-heading">
        <h2>
          {title}
          <sup>▪</sup>
        </h2>
        {action}
      </div>
      {children}
    </section>
  );
}
