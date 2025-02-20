
import React, { useState } from "react";
import { uploadResume } from "../api";
import "../styles/UploadResume.css";

const UploadResume = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setMessage("");  // Clear message when new file is selected
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file to upload");
      setMessage("Upload a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setMessage("Uploading... ⏳");
      await uploadResume(formData);
      setMessage("Resume uploaded successfully! ✅");
    } catch (error) {
      setMessage("Error uploading resume ❌");
    }
  };

  return (
    <div className="resume-upload-container">
      <div className="upload-box">
        <h2>📄 Upload Your Resume</h2>
        <label className="upload-label">
          {file ? file.name : "Choose File"}
          <input type="file" onChange={handleFileChange} accept=".pdf,.docx,.html" />
        </label>
        <p className="supported-formats">Supported formats: .pdf, .docx, .html</p>
        <button className="upload-button" onClick={handleUpload}>
          Upload
        </button>
        {message && <p>{message}</p>}
      </div>
    </div>
  );
};

export default UploadResume;
