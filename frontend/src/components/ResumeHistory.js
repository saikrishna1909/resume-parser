import React, { useEffect, useState } from "react";
import { fetchResumes } from "../api";
import "../styles/ResumeHistory.css";

const ResumeHistory = ({ onSelectResume }) => {
  const [resumes, setResumes] = useState([]);

  useEffect(() => {
    const loadResumes = async () => {
      try {
        const response = await fetchResumes();
        setResumes(response.data);
      } catch (error) {
        console.error("Error fetching resumes", error);
      }
    };

    loadResumes();
  }, []);

  return (
    <div className="history-section">
      <h2>Uploaded Resumes</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>File Name</th>
            <th>View</th>
          </tr>
        </thead>
        <tbody>
          {resumes.map((resume) => (
            <tr key={resume.id}>
              <td>{resume.id}</td>
              <td>{resume.filename}</td>
              <td>
                <button onClick={() => onSelectResume(resume.id)}>View</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ResumeHistory;
