import Status from "src/components/Status";
import styles from "./styles.module.css";

export default function Dashboard() {
  return (
    <section className={styles.dashboardSection}>
      <div className={styles.headerBlock}>
        <h1 className={styles.title}>Contêineres - Prédio de Engenharia</h1>
        <p className={styles.subtitle}>Monitoramento em tempo real para reposição mais eficiente e previsível.</p>
      </div>

      <div className={styles.statusDiv}>
        <Status />
      </div>
    </section>
  );
}
