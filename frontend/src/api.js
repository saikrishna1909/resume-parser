
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";  // ✅ FIXED: This should match the backend

export const uploadResume = async (formData) => {
  try {
    console.log("📤 Uploading to:", `${API_URL}/upload`);  // ✅ Debugging log
    console.log("📝 FormData:", formData);  // ✅ Ensure file is attached

    const response = await axios.post(`${API_URL}/upload`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    console.log("✅ Upload Success:", response.data);
    return response.data;
  } catch (error) {
    console.error("❌ Upload error:", error.response?.data || error.message);
    throw error;
  }
};



export const fetchResumes = async () => {
  return axios.get(`${API_URL}/history`);
};

export const fetchResumeDetails = async (id) => {
  return axios.get(`${API_URL}/resume/${id}`);
};
