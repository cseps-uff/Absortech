import axios from "axios";

const { protocol, hostname, port } = window.location;
const envApiHost = import.meta.env.VITE_API_HOST || import.meta.env.API_HOST;
export const baseURL = envApiHost || `${protocol}//${hostname}${port ? `:${port}` : ''}/api`;

const api = axios.create({
    baseURL,
    headers: { "Content-Type": "application/json" }
});

export const fetchLeituras = async () => {
    try {
        const response = await api.get("/leituras/");
        return response.data;
    } catch (error) {
        throw new Error(`Erro ao buscar leituras: ${error}`);
    }
};

export default api;
