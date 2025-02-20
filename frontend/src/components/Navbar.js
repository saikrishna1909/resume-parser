import React from "react";
import { Link } from "react-router-dom";
import "../styles/Navbar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      {/* Clicking on "Resume Parser" navigates to Home */}
      <h1>
        <Link to="/" className="navbar-title">Resume Parser</Link>
      </h1>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/upload">Upload Resume</Link></li>
        <li><Link to="/history">View History</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
