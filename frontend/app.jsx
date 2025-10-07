const { useState, useEffect } = React;

function App() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [backendReady, setBackendReady] = useState(false);

  useEffect(() => {
    const healthCheck = setInterval(async () => {
      try {
        const res = await fetch('/api/health');
        const data = await res.json();
        if (data.status === 'ready') {
          setBackendReady(true);
          clearInterval(healthCheck);
        }
      } catch (error) {
        console.error('Health check failed:', error);
      }
    }, 1000);
    return () => clearInterval(healthCheck);
  }, []);

  const handleFileChange = (e) => {
    setImage(e.target.files[0]);
    setResult(null);
  };

  const handleUpload = async () => {
    if (!image) return;
    const formData = new FormData();
    formData.append('file', image);
    setLoading(true);
    const res = await fetch('/api/detect', {
      method: 'POST',
      body: formData,
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <main className="p-4 max-w-md mx-auto text-center">
      <h1 className="text-2xl font-bold mb-4">Intimate Area Detector</h1>
      <input type="file" accept="image/*" onChange={handleFileChange} className="mb-4" />
      <button
        onClick={handleUpload}
        disabled={loading || !backendReady}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        {loading ? 'Processing...' : (backendReady ? 'Detect Areas' : 'Backend Loading...')}
      </button>
      {result && (
        <div className="mt-4 text-left">
          <h2 className="font-semibold">Detection Result:</h2>
          <pre className="bg-gray-100 p-2 rounded text-sm whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </main>
  );
}

const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);
root.render(<App />);
