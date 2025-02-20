import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import UploadPage from "./pages/UploadPage";
import HistoryPage from "./pages/HistoryPage";
import ResumeViewer from "./pages/ResumeViewer"; // ✅ New Component

function App() {
  return (
    <Router>
      <Navbar />
      <div className="container"> {/* ✅ Wrap content inside a container */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/resume/:id" element={<ResumeViewer />} /> {/* ✅ New Route */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
