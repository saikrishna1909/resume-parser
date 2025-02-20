import React, { useState } from "react";
import "../styles/HistoryPage.css";
import ResumeHistory from "../components/ResumeHistory";
import ResumeDetails from "../components/ResumeDetails";

const HistoryPage = () => {
  const [selectedResumeId, setSelectedResumeId] = useState(null);

  return (
    <div className="container">
      <h2>Resume History</h2>
      <ResumeHistory onSelectResume={setSelectedResumeId} />
      <ResumeDetails resumeId={selectedResumeId} />
    </div>
  );
};

export default HistoryPage;
