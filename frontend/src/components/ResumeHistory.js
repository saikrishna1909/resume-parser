import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/ResumeHistory.css";

const ResumeHistory = () => {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchResumes = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/history");
        if (!response.ok) {
          throw new Error("Failed to fetch resumes");
        }
        const data = await response.json();
        setResumes(Array.isArray(data.resumes) ? data.resumes : []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchResumes();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm("❗ Are you sure you want to delete this resume?")) return;

    try {
      const response = await fetch(`http://localhost:8000/api/resumes/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Failed to delete resume");
      }

      setResumes(resumes.filter(resume => resume._id !== id));
      alert("✅ Resume deleted successfully!");
    } catch (err) {
      alert("❌ Error deleting resume.");
    }
  };

  if (loading) return <div className="loading">⏳ Loading resume history...</div>;
  if (error) return <p className="error">❌ {error}</p>;

  return (
    <div className="history-container">
      <h2>📜 Resume History</h2>
      {resumes.length > 0 ? (
        <table className="resume-table">
          <thead>
            <tr>
              <th>📂 Filename</th>
              <th>⚡ Actions</th>
            </tr>
          </thead>
          <tbody>
            {resumes.map((resume) => (
              <tr key={resume._id}>
                <td>{resume.filename}</td>
                <td>
                  <button className="view-btn" onClick={() => navigate(`/resume/${resume._id}`)}>👁️ View</button>
                  <button className="delete-btn" onClick={() => handleDelete(resume._id)}>🗑️ Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p className="no-resumes">🚫 No resumes found.</p>
      )}
    </div>
  );
};

export default ResumeHistory;
