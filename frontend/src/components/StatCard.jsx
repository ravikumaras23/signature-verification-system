 export default function StatCard({
  title,
  value,
  subtitle,
  icon: Icon,
  className = ""
}) {

  return (
    <div
      className={`stat-card ${className}`}
    >

      <div className="stat-top">

        <span>
          {title}
        </span>

        <div className="stat-icon">
          <Icon
            size={18}
          />
        </div>

      </div>


      <strong>
        {value}
      </strong>


      <small>
        {subtitle}
      </small>

    </div>
  );
}