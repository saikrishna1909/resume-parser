import React from "react";
import { Link } from "react-router-dom";
import "../styles/Home.css";

const Home = () => {
  return (
    <div className="home-container">
      <h2>Welcome to Resume Parser</h2>
      <div className="options">
        <Link to="/upload" className="option-btn">Resume Upload</Link>
        <Link to="/history" className="option-btn">View History</Link>
      </div>
    </div>
  );
};

export default Home;

