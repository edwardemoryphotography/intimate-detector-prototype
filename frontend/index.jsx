import React, { useState } from 'react';

export default function Home() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const parseErrorResponse = async (res) => {
    const defaultMessage =
      res.status === 0
        ? 'The server could not process your image. Please try again later.'
        : `The server returned ${res.status}${
            res.statusText ? ` ${res.statusText}` : ''
          }. Please try again.`;
    const contentType = res.headers.get('content-type') || '';

    try {
      if (contentType.includes('application/json')) {
        const errorBody = await res.json();
        return (
          errorBody?.message ||
          errorBody?.error ||
          errorBody?.detail ||
          defaultMessage
        );
      }

      if (contentType.includes('text/')) {
        const errorText = await res.text();
        if (errorText.trim()) {
          return errorText;
        }
      }
    } catch (_parseError) {
      // Ignore parsing issues and fall back to the default message.
    }

    return defaultMessage;
  };

  const handleFileChange = (e) => {
    setImage(e.target.files[0]);
    setResult(null);
    setError(null);
  };

  const handleUpload = async () => {
    if (!image) return;
    const formData = new FormData();
    formData.append('file', image);
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch('http://localhost:5000/api/detect', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const message = await parseErrorResponse(res);
        throw new Error(message);
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult(null);
      if (err instanceof TypeError || err?.message === 'Failed to fetch') {
        setError(
          'We could not reach the detection service. Please check your connection and try again.'
        );
        return;
      }

      if (err instanceof Error && err.message) {
        setError(err.message);
        return;
      }

      setError('An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="p-4 max-w-md mx-auto text-center">
      <h1 className="text-2xl font-bold mb-4">Intimate Area Detector</h1>
      <input type="file" accept="image/*" onChange={handleFileChange} className="mb-4" />
      <button
        onClick={handleUpload}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        {loading ? 'Processing...' : 'Detect Areas'}
      </button>
      {error && (
        <p className="mt-2 text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
      {result && (
        <div className="mt-4 text-left">
          <h2 className="font-semibold">Detection Result:</h2>
          <pre className="bg-gray-100 p-2 rounded text-sm whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </main>
  );
}
