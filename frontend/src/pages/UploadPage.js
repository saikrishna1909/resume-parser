import React from "react";
import UploadResume from "../components/UploadResume";

const UploadPage = () => {
  return (
    <div className="container">
     <h2 style={{ 
    textAlign: "center", 
    fontWeight: "bold", 
    fontSize: "32px", 
    color: "gray", 
    marginBottom: "20px" 
}}>
    Upload Resume
</h2>
      <UploadResume />
    </div>
  );
};

export default UploadPage;
