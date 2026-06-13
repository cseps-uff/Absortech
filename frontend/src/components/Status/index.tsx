import styles from "./styles.module.css";
import { fetchLeituras } from "src/services/api";
import { useQuery } from "react-query";

interface Dispenser {
  id: number;
  nome: string;
  localização: string;
  instituicao: string;
  bloco: string;
  andar: number;
  ativo: boolean;
  created_at: string;
}

interface Leitura {
  id: number;
  timestamp: string;
  distancia_cm: number;
  quantidade_estimada: number;
  porcentagem_ocupacao: number;
  dispenser: Dispenser;
}

export default function Status() {
  const {
    data: leituras,
    isLoading,
    error,
  } = useQuery<Leitura[]>("fetchLeituras", fetchLeituras, {
    refetchInterval: 5000,
    retry: false
  });

  // Show loading
  if (isLoading) {
    return (
      <div className={styles.loadingContainer}>
        <p>Carregando dados...</p>
      </div>
    );
  }

  // Show error
  if (error) {
    return (
      <div className={styles.loadingContainer}>
        <p>Erro ao carregar dados. Tente novamente.</p>
      </div>
    );
  }

  // Show message if no readings available
  if (!leituras || !Array.isArray(leituras) || leituras.length === 0) {
    return (
      <div className={styles.loadingContainer}>
        <p>Não há dados disponíveis.</p>
      </div>
    );
  }

  return (
    <div className={styles.status}>
      {leituras.map((leitura, index) => {
        const quantidade = leitura.quantidade_estimada;
        const ocupacao = leitura.porcentagem_ocupacao;
        const dispenser = leitura.dispenser;
        
        // Status: alerta se ocupação > 80% ou quantidade < 3
        const isAlert = ocupacao >= 80 || quantidade < 3;
        
        return (
          <div key={index} className={styles.container}>
            <div>
              <p className={styles.text1}>
                {dispenser.nome} - Andar {dispenser.andar}
              </p>
              <p className={styles.text2}>
                {isAlert ? "🔴 Alerta" : "🟢 Condição estável"} -{" "}
                {quantidade} absorvente{quantidade !== 1 ? "s" : ""} ({ocupacao.toFixed(1)}%)
              </p>
              <p style={{ fontSize: "0.85em", color: "#666", marginTop: "4px" }}>
                {dispenser.localização} | Bloco {dispenser.bloco}
              </p>
            </div>
            <div className={isAlert ? styles.redSignal : styles.greenSignal} />
          </div>
        );
      })}
    </div>
  );
}
