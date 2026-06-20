import styles from "./styles.module.css";
import { fetchLeituras } from "src/services/api";
import { useQuery } from "react-query";

const LIMITE_ALERTA_QUANTIDADE = 3;

const dateFormatter = new Intl.DateTimeFormat("pt-BR", {
  dateStyle: "short",
  timeStyle: "short",
});

export default function Status() {
  const {
    data: leituras,
    isLoading,
    error,
  } = useQuery("fetchLeituras", fetchLeituras, {
    refetchInterval: 5000,
    retry: false
  });

  if (isLoading) {
    return (
      <div className={styles.loadingContainer}>
        <p>Carregando dados...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.loadingContainer}>
        <p>Erro ao carregar dados. Tente novamente.</p>
      </div>
    );
  }

  if (!leituras || leituras.length === 0) {
    return (
      <div className={styles.loadingContainer}>
        <p>Nao ha dados disponiveis.</p>
      </div>
    );
  }

  return (
    <div className={styles.status}>
      {leituras.map((leitura) => {
        const quantidade = leitura.quantidade_estimada;
        const ocupacao = leitura.porcentagem_ocupacao;
        const dispenser = leitura.dispenser;
        const isAlert = quantidade === null || quantidade <= LIMITE_ALERTA_QUANTIDADE;
        const nivel = Math.min(Math.max(ocupacao ?? 0, 0), 100);
        const quantidadeLabel = quantidade === null
          ? "Quantidade indisponivel"
          : `${quantidade} absorvente${quantidade !== 1 ? "s" : ""}`;

        return (
          <article
            key={leitura.id}
            className={`${styles.container} ${isAlert ? styles.alertCard : ""}`}
          >
            <header className={styles.cardHeader}>
              <div>
                <p className={styles.institution}>{dispenser.instituicao}</p>
                <h2 className={styles.title}>{dispenser.nome}</h2>
              </div>
              <span className={`${styles.badge} ${isAlert ? styles.alertBadge : styles.stableBadge}`}>
                <span className={styles.badgeDot} aria-hidden="true" />
                {isAlert ? "Reposicao necessaria" : "Condicao estavel"}
              </span>
            </header>

            <p className={styles.location}>
              {dispenser.localizacao} - Bloco {dispenser.bloco} - {dispenser.andar}o andar
            </p>

            <div className={styles.metrics}>
              <div className={styles.primaryMetric}>
                <span className={styles.metricLabel}>Estoque estimado</span>
                <strong>{quantidadeLabel}</strong>
              </div>
              <div className={styles.metric}>
                <span className={styles.metricLabel}>Distancia</span>
                <strong>{leitura.distancia_cm.toFixed(1)} cm</strong>
              </div>
              <div className={styles.metric}>
                <span className={styles.metricLabel}>Ultima leitura</span>
                <strong>{dateFormatter.format(new Date(leitura.timestamp))}</strong>
              </div>
            </div>

            <div className={styles.levelSection}>
              <div className={styles.levelHeader}>
                <span>Nivel do dispenser</span>
                <strong>{ocupacao === null ? "Indisponivel" : `${ocupacao.toFixed(1)}%`}</strong>
              </div>
              <div
                className={styles.levelTrack}
                role="meter"
                aria-label={`Nivel de ${dispenser.nome}`}
                aria-valuemin={0}
                aria-valuemax={100}
                aria-valuenow={nivel}
              >
                <div
                  className={`${styles.levelFill} ${isAlert ? styles.alertLevel : styles.stableLevel}`}
                  style={{ width: `${nivel}%` }}
                />
              </div>
            </div>
          </article>
        );
      })}
    </div>
  );
}
