import React, { useEffect, useState } from "react";
import { fetchResumeDetails } from "../api";

const ResumeDetails = ({ resumeId }) => {
  const [resume, setResume] = useState(null);

  useEffect(() => {
    const loadResumeDetails = async () => {
      try {
        const response = await fetchResumeDetails(resumeId);
        setResume(response.data);
      } catch (error) {
        console.error("Error fetching resume details", error);
      }
    };

    if (resumeId) {
      loadResumeDetails();
    }
  }, [resumeId]);

  if (!resume) {
    return <p>Select a resume to view details.</p>;
  }

  return (
    <div>
      <h2>Resume Details</h2>
      <p><strong>Name:</strong> {resume.name}</p>
      <p><strong>Email:</strong> {resume.email}</p>
      <p><strong>Skills:</strong> {resume.skills.join(", ")}</p>
    </div>
  );
};

export default ResumeDetails;
