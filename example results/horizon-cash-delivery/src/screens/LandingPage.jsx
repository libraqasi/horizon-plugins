import BrandHeader from '../components/BrandHeader.jsx';
import { BoxIcon, PinIcon } from '../components/Icons.jsx';
import { cashIcon, droneIcon, heroImage } from '../assets.js';

export default function LandingPage({ onLogin }) {
  return (
    <div className="landing-page">
      <a className="skip-link" href="#main">Skip to content</a>
      <BrandHeader landing onLogin={onLogin} />
      <main id="main">
        <section className="landing-hero">
          <div className="hero-photo-wrap">
            <img className="hero-photo" src={heroImage} alt="A family watches a delivery drone arrive outside their home" />
          </div>
          <div className="hero-copy">
            <img className="hero-drone-icon" src={droneIcon} alt="" />
            <h1>Cash, delivered<br />to your door.</h1>
            <p>Get cash from your Horizon Bank checking account delivered to a drop spot you choose.</p>
            <button className="button button--primary hero-login" type="button" onClick={onLogin}>Login</button>
          </div>
        </section>
        <section className="how-it-works" aria-labelledby="how-heading">
          <h2 id="how-heading">How it works</h2>
          <div className="steps-list">
            <article className="marketing-step">
              <span className="marketing-step-icon"><img src={cashIcon} alt="" /></span>
              <div><h3>Choose your amount</h3><p>Select the cash amount you want from your checking account.</p></div>
            </article>
            <article className="marketing-step">
              <span className="marketing-step-icon"><PinIcon /></span>
              <div><h3>Pick a drop spot</h3><p>Choose a safe, convenient location around your home.</p></div>
            </article>
            <article className="marketing-step">
              <span className="marketing-step-icon"><BoxIcon /></span>
              <div><h3>Track your delivery</h3><p>Follow each step from cash preparation through arrival.</p></div>
            </article>
          </div>
        </section>
      </main>
      <footer className="landing-footer"><p>Cash delivery service preview</p></footer>
    </div>
  );
}
