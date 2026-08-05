import { wordmark } from '../assets.js';

export default function BrandHeader({ landing = false, onLogin, onReset }) {
  return (
    <>
      <header className={`brand-header ${landing ? 'brand-header--landing' : ''}`}>
        {landing ? (
          <a className="brand-home" href="#main" aria-label="Horizon Bank home">
            <img src={wordmark} alt="Horizon Bank" />
          </a>
        ) : (
          <a className="brand-home" href="#main" aria-label="Return to the Horizon Bank preview home" onClick={(event) => { event.preventDefault(); onReset(); }}>
            <img src={wordmark} alt="Horizon Bank" />
          </a>
        )}
        {landing ? (
          <button className="header-login" type="button" onClick={onLogin}>Login</button>
        ) : (
          <button className="header-reset" type="button" aria-label="Reset preview" onClick={onReset}>Reset</button>
        )}
      </header>
      <div className="brand-rule" />
    </>
  );
}
