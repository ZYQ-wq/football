import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/api";

export const api = {
  getTeams: () => axios.get(`${BASE_URL}/teams`).then(res => res.data),
  getFormations: () => axios.get(`${BASE_URL}/formations`).then(res => res.data),
  getTactics: () => axios.get(`${BASE_URL}/tactics`).then(res => res.data),
  simulate: (payload) => axios.post(`${BASE_URL}/simulate`, payload).then(res => res.data),
};