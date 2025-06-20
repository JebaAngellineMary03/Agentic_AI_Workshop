import axios from "axios";

const BASE_URL = "http://localhost:8000"; // Backend FastAPI server

export const analyzeVideo = async (youtube_url) =>
  axios.post(`${BASE_URL}/analyze`, { youtube_url });

export const getEvaluations = async (studentId) =>
  axios.get(`${BASE_URL}/evaluations`);

export const getFeedback = async (youtube_url) =>
  axios.get(`${BASE_URL}/feedback_logs`, { params: { youtube_url } });
