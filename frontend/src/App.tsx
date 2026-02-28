import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/ui/Navbar";
import LandingPage from "./pages/LandingPage";
import AppFlow from "./pages/AppFlow";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/app" element={<AppFlow />} />
      </Routes>
    </BrowserRouter>
  );
}
