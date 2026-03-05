import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [downloadUrl, setDownloadUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const upload = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append("video", file);

    const response = await axios.post(
      "http://127.0.0.1:8001/api/upload/",
      formData,
      {
        onUploadProgress: (event) => {
          const percent = Math.round(
            (event.loaded * 100) / event.total
          );
          setProgress(percent);
        },
      }
    );

    setDownloadUrl(response.data.download_url);
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>English ? Hebrew Subtitles</h1>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />

      <button onClick={upload} disabled={!file || loading}>
        {loading ? "Processing..." : "Upload & Translate"}
      </button>

      {progress > 0 && (
        <div className="progress-bar">
          <div className="progress" style={{ width: progress + "%" }} />
        </div>
      )}

      {downloadUrl && (
        <a className="download-btn" href={downloadUrl}>
          Download Hebrew Subtitles
        </a>
      )}
    </div>
  );
}

export default App;
