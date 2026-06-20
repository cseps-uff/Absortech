import Status from "src/components/Status";
import styles from "./styles.module.css";

export default function Dashboard() {
  return (
    <section className={styles.dashboardSection}>
      <div className={styles.headerBlock}>
        <h1 className={styles.title}>Monitoramento de dispensers</h1>
        <p className={styles.subtitle}>Estoque e condições operacionais das unidades instaladas, atualizados em tempo real.</p>
      </div>

      <div className={styles.statusDiv}>
        <Status />
      </div>
    </section>
  );
}
