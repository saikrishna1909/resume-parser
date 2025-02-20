import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom"; // ✅ Added useNavigate
import "../styles/ResumeViewer.css"; // ✅ Import CSS for styling

const ResumeViewer = () => {
  const { id } = useParams(); // Get the resume ID from the URL
  const navigate = useNavigate(); // ✅ Hook to navigate back
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchResumeDetails = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/details/${id}`);
        if (!response.ok) {
          throw new Error("Failed to fetch resume details");
        }
        const data = await response.json();
        setResume(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchResumeDetails();
  }, [id]);

  if (loading) return <p className="loading-text">⏳ Loading resume details...</p>;
  if (error) return <p className="error-text">❌ {error}</p>;

  return (
    <div className="resume-container">
      <button onClick={() => navigate(-1)} className="back-btn">🔙 Back</button> {/* ✅ Back Button */}

      <h2>📄 Resume Details</h2>
      {resume ? (
        <div className="resume-content">
          <p><strong>👤 Name:</strong> {resume.name}</p>
          <p><strong>📧 Email:</strong> {resume.email}</p>
          <p><strong>📞 Phone:</strong> {resume.phone}</p>
          <p><strong>📂 Filename:</strong> {resume.filename}</p>

          {resume.core_skills && resume.core_skills.length > 0 && (
            <>
              <h3>💡 Core Skills</h3>
              <ul>
                {resume.core_skills.map((skill, index) => (
                  <li key={index}>{skill}</li>
                ))}
              </ul>
            </>
          )}

          <h3>👨‍💼 Experience</h3>
          <pre className="resume-text">{resume.experience}</pre>

          <h3>🎓 Education</h3>
          <pre className="resume-text">{resume.education}</pre>

          <h3>⭐ Resume Rating: {resume.resume_rating}/10</h3>

          {resume.improvement_areas && resume.improvement_areas.length > 0 && (
            <>
              <h3>📌 Improvement Areas</h3>
              <ul>
                {resume.improvement_areas.map((area, index) => (
                  <li key={index}>{area}</li>
                ))}
              </ul>
            </>
          )}

          {resume.upskill_suggestions && resume.upskill_suggestions.length > 0 && (
            <>
              <h3>📚 Upskill Suggestions</h3>
              <ul>
                {resume.upskill_suggestions.map((suggestion, index) => (
                  <li key={index}>{suggestion}</li>
                ))}
              </ul>
            </>
          )}

          <button
            onClick={() => window.open(`http://localhost:8000/api/download/${resume.file_id}`, "_blank")}
            className="download-btn"
          >
            📥 Download Resume
          </button>
        </div>
      ) : (
        <p className="error-text">Resume details not found.</p>
      )}
    </div>
  );
};

export default ResumeViewer;
