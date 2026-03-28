import { Outlet, useLocation, useNavigate } from "react-router-dom";

import instagram from "assets/InstagramLogo.png";
import youtube from "assets/youtubeLogo.png";
import linkedin from "assets/linkedlnLogo.png"; 
import facebook from "assets/facebookLogo.png";
import poweredByLogo from "assets/PoweredBy.png";

import styles from "./styles.module.css";

export default function Layout() {
  const location = useLocation();
  const navigate = useNavigate();

  const isHomePage = location.pathname === "/"

  const route = {
    title: isHomePage ? "Dashboard" : "Home",
    path: isHomePage ? "/dashboard" : "/"
  }

  return (
    <div className={styles.container}>
      {/* HEADER */}
      <header className={styles.topBarHeader}>
        <div className={styles.topBarLeft}>
          <button
            className={styles.buttonHomepage}
            aria-label={`Ir para ${route.title}`}
            onClick={() => navigate(route.path)}
          >
            {route.title}
          </button>
        </div>

        <h1 className={styles.topBarCenterTitle}>CS EPS & WIE</h1>

        <div className={styles.topBarRight}>
          <div className={styles.menuIcon}>
            <div></div>
            <div></div>
            <div></div>
          </div>
        </div>
      </header>

      {/* PAGE CONTENT */}
      <main>
        <Outlet />
      </main>

      {/* FOOTER */}
      <footer className={styles.footer}>
        <div className={styles.footerLeft}>
          <p><a href="#">Termos de Uso</a></p>
          <p><a href="#">Política de Privacidade</a></p>
        </div>

        <div className={styles.footerCenter}>
          <p className={styles.poweredByText}>Powered by</p>
          <a href="https://edu.ieee.org/br-uff/" target="_blank" rel="noopener noreferrer" title="Powered by UFF">
            <img src={poweredByLogo} alt="Powered by Logo" className={styles.poweredByLogo} />
          </a>
          <p className={styles.footerText}>© 2024 CS EPS & WIE. Todos os direitos reservados.</p>
        </div>

        <div className={styles.footerRight}>
          <div className={styles.socialIcons}>
            <a href="https://www.instagram.com/ieee.uff/" target="_blank" rel="noopener noreferrer" title="Instagram IEEE UFF">
              <img src={instagram} alt="Instagram Logo" className={styles.instagramLogo} />
            </a>
            <a href="https://www.youtube.com/user/ieeeuffsb" target="_blank" rel="noopener noreferrer" title="YouTube IEEE UFF">
              <img src={youtube} alt="YouTube Logo" className={styles.youtubeLogo} />
            </a>
            <a href="https://br.linkedin.com/company/ramo-estudantil-ieee-uff" target="_blank" rel="noopener noreferrer" title="LinkedIn IEEE UFF">
              <img src={linkedin} alt="LinkedIn Logo" className={styles.linkedinLogo} />
            </a>
            <a href="https://twitter.com/your-account" target="_blank" rel="noopener noreferrer" title="Facebook IEEE UFF">
              <img src={facebook} alt="Facebook Logo" className={styles.FacebookLogo} />
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
