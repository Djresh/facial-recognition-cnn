import axios from "axios";

const API = "http://localhost:5000/api";

export const recognizeFace = (base64Image) => axios.post(API + "/recognize", { image: base64Image });
export const fetchLogs     = (limit = 20)  => axios.get(API + "/logs",    { params: { limit } });
export const fetchStats    = ()            => axios.get(API + "/stats");
export const fetchClasses  = ()            => axios.get(API + "/classes");
export const checkHealth   = ()            => axios.get(API + "/health");
export const reloadModel   = ()            => axios.post(API + "/reload-model");
