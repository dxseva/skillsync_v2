import Hero from "../components/landing/Hero";
import Features from "../components/landing/Features";
import HowItWorks from "../components/landing/HowItWorks";
import TechStack from "../components/landing/TechStack";
import FAQ from "../components/landing/FAQ";
import Footer from "../components/landing/Footer";

export default function LandingPage() {
  return (
    <main>
      <Hero />
      <Features />
      <HowItWorks />
      <TechStack />
      <FAQ />
      <Footer />
    </main>
  );
}
