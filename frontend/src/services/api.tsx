import axios from "axios";

export interface Dispenser {
    id: number;
    nome: string;
    localizacao: string;
    instituicao: string;
    bloco: string;
    andar: number;
    ativo: boolean;
    created_at: string;
}

export interface Leitura {
    id: number;
    timestamp: string;
    distancia_cm: number;
    quantidade_estimada: number | null;
    porcentagem_ocupacao: number | null;
    dispenser: Dispenser;
}

interface LeituraApi extends Omit<
    Leitura,
    "distancia_cm" | "porcentagem_ocupacao"
> {
    distancia_cm: string | number;
    porcentagem_ocupacao: string | number | null;
}

const { protocol, hostname, port } = window.location;
const envApiHost = import.meta.env.VITE_API_HOST || import.meta.env.API_HOST;
export const baseURL = envApiHost || `${protocol}//${hostname}${port ? `:${port}` : ''}/api`;

const api = axios.create({
    baseURL,
    headers: { "Content-Type": "application/json" }
});

const parseDecimal = (value: string | number | null): number | null => {
    if (value === null) {
        return null;
    }

    const parsedValue = Number(value);
    return Number.isFinite(parsedValue) ? parsedValue : null;
};

export const fetchLeituras = async (): Promise<Leitura[]> => {
    try {
        const response = await api.get<LeituraApi[]>("/leituras/");
        if (!Array.isArray(response.data)) {
            throw new Error("Formato de resposta invalido");
        }

        return response.data.map((leitura) => {
            const distancia = parseDecimal(leitura.distancia_cm);
            if (distancia === null) {
                throw new Error(`Distancia invalida na leitura ${leitura.id}`);
            }

            return {
                ...leitura,
                distancia_cm: distancia,
                porcentagem_ocupacao: parseDecimal(leitura.porcentagem_ocupacao),
            };
        });
    } catch (error) {
        throw new Error(`Erro ao buscar leituras: ${error}`);
    }
};

export default api;
