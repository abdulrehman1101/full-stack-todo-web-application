import HeroSection from '@/src/components/landing/HeroSection';
import FeatureCards from '@/src/components/landing/FeatureCards';
import Footer from '@/src/components/footer/Footer';

export default function Home() {
  return (
    <div className="min-h-screen bg-white dark:bg-[#020617]">

      <main>
        <HeroSection />
        <FeatureCards />
      </main>

      <Footer />

    </div>
  );
}
