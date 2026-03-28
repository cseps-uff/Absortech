import styles from "./styles.module.css";
import heroImage from "assets/homePageImg.png";

export default function Home() {
  return (
    <main className={styles.container}>
      {/* Seção da Imagem de Fundo Superior */}
      <section className={styles.topImageSection}>
        <img
          src={heroImage}
          alt="Contêiner inteligente Absortech instalado"
          className={styles.heroImage}
          loading="eager"
          decoding="async"
        />
        <div className={styles.imageOverlay}></div>
        <div className={styles.topImageContent}>
          <h1>ABSORTECH</h1>
          <p>DIGNIDADE E DISCRIÇÃO</p>
        </div>
      </section>

      {/* Seção de Blocos (Caixinhas) */}
      <section className={styles.textBlocksSection}>
        <div className={styles.textBlocksContainer}>
          <div className={styles.textBlock}>
            <div className={styles.yellowSquare}></div>
            <div className={styles.textBlockContent}>
              <h2>Processo Produtivo</h2>
              <p>
                Detalhes sobre a fabricação e montagem de nossos produtos, garantindo alta qualidade e eficiência.
              </p>
            </div>
          </div>

          <div className={styles.textBlock}>
            <div className={styles.yellowSquare}></div>
            <div className={styles.textBlockContent}>
              <h2>Instalação e Manutenção</h2>
              <p>
                Informações sobre a facilidade de instalação e as práticas de manutenção para a longevidade do produto.
              </p>
            </div>
          </div>

          <div className={styles.textBlock}>
            <div className={styles.yellowSquare}></div>
            <div className={styles.textBlockContent}>
              <h2>Tecnologia Integrada</h2>
              <p>
                Exploração das tecnologias incorporadas que tornam nossos contêineres inteligentes e autônomos.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className={`${styles.mainContentSection} ${styles.purpleGradientBackground}`}>
        <div className={`${styles.mainContentContainer} ${styles.contentFlex}`}>
          <figure className={styles.featureImageWrapper}>
            <img
              src={heroImage}
              alt="Estrutura do contêiner com foco na robustez do design"
              className={styles.featureImage}
              loading="lazy"
              decoding="async"
            />
            <figcaption className={styles.featureCaption}>Design funcional com proporção otimizada para diferentes ambientes.</figcaption>
          </figure>
          <div className={styles.textContent}>
            <h2>Metas e nossos 4 “idade”</h2>
            <p>
              Praticidade, simplicidade, responsividade e escalabilidade. Prático pela fácil instalação e baixa manutenção. Simples pelo visual limpo e elegante. Responsivo pela tecnologia eficiente. Escalável pelo uso de um sistema de comunicação otimizado e rápido entre contêineres.
            </p>
          </div>
        </div>
      </section>

      <section className={`${styles.mainContentSection} ${styles.purpleGradientBackground}`}>
        <div className={`${styles.mainContentContainer} ${styles.contentFlex} ${styles.reverse}`}>
          <figure className={styles.featureImageWrapper}>
            <img
              src={heroImage}
              alt="Sistema inteligente monitorando níveis de absorventes"
              className={styles.featureImage}
              loading="lazy"
              decoding="async"
            />
            <figcaption className={styles.featureCaption}>Telemetria em tempo real para reposição ágil e previsível.</figcaption>
          </figure>
          <div className={styles.textContent}>
            <h2>Contêiner Autômato</h2>
            <p>
              Um produto simples, prático, responsivo e escalável. Prático pela fácil instalação e baixa manutenção. Simples pelo visual limpo e elegante. Responsivo pela tecnologia eficiente. Escalável pelo uso de um sistema de comunicação otimizado e rápido entre contêineres.
            </p>
          </div>
        </div>
      </section>

      {/* Emanuel caso vc ache importante ter o componente Status na Homepage, você pode colocá-lo aqui */}
      {/* <section className={styles.statusSection}>
          <h1 className={styles.title2}>Contêineres - Prédio de Engenharia</h1>
          <div className={styles.statusDiv}>
            <Status />
          </div>
      </section> */}

    </main>
  );
}
