export const Button = ({ children, ...props }) => (
  <button
    className="px-4 py-2 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition disabled:opacity-50"
    {...props}
  >
    {children}
  </button>
);
