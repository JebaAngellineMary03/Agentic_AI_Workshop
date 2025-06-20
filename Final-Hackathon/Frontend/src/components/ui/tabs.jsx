import React,{useState} from "react";

export const Tabs = ({ children, defaultValue }) => {
  const [activeTab, setActiveTab] = useState(defaultValue);

  return children.map(child =>
    child.type.displayName === "TabsList"
      ? React.cloneElement(child, { activeTab, setActiveTab })
      : child.props.value === activeTab
      ? child
      : null
  );
};

export const TabsList = ({ children, activeTab, setActiveTab }) => (
  <div className="flex space-x-4 border-b border-gray-300 mb-4">
    {children.map(child =>
      React.cloneElement(child, { activeTab, setActiveTab })
    )}
  </div>
);

export const TabsTrigger = ({ value, children, activeTab, setActiveTab }) => (
  <button
    onClick={() => setActiveTab(value)}
    className={`px-4 py-2 rounded-t-md ${
      activeTab === value ? "bg-indigo-600 text-white" : "bg-gray-100 text-gray-600"
    }`}
  >
    {children}
  </button>
);

export const TabsContent = ({ children }) => <div>{children}</div>;

TabsList.displayName = "TabsList";
TabsTrigger.displayName = "TabsTrigger";
TabsContent.displayName = "TabsContent";
