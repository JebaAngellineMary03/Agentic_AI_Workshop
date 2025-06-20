import VideoDashboard from "./components/VideoDashboard";

function App() {
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <h1 className="text-3xl font-bold text-center text-indigo-600 mb-8">
        🎥 Video Evaluation Portal
      </h1>

      <div className="max-w-6xl mx-auto">
        <VideoDashboard />
      </div>
    </div>
  );
}

export default App;
