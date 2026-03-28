import styles from "./styles.module.css";
import { fetchLeituras } from "src/services/api";
import { useQuery } from "react-query";

interface Leitura {
  andar: string;
  data: string;
  hora: string;
  valor_leitura: number;
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
      {leituras.map((item, index) => {
        const quantidadeAbsorventes = Number(item.valor_leitura);
        
        return (
          <div key={index} className={styles.container}>
            <p className={styles.text1}>Andar {item.andar}</p>
            <div className={styles.statusDiv}>
              <p className={styles.text2}>
                {quantidadeAbsorventes > 3 ? "• Condição estável" : "• Alerta"} -{" "}
                {quantidadeAbsorventes} absorvente{quantidadeAbsorventes !== 1 ? "s" : ""}
              </p>
              <div
                className={
                  quantidadeAbsorventes >= 3 ? styles.greenSignal : styles.redSignal
                }
              />
            </div>
          </div>
        );
      })}
    </div>
  );
}
