export const Card = ({ children, className = "" }) => (
  <div className={`rounded-2xl border p-4 bg-white shadow ${className}`}>
    {children}
  </div>
);

export const CardContent = ({ children }) => <div>{children}</div>;
