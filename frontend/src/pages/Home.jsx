import Navbar from "../components/Navbar";
import HeroSection from "../components/HeroSection";
import UploadBox from "../components/UploadBox";
import Footer from "../components/Footer";

function Home() {
  return (
    <div>
      <Navbar />

      <HeroSection />

      <div className="max-w-5xl mx-auto px-6 pb-20">
        <UploadBox />
      </div>

      <Footer />
    </div>
  );
}

export default Home;