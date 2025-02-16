import { useEffect } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import "../fonts/fonts.css";



const WelcomePage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    setTimeout(() => {
      window.location.href = "/file-explorer";
    }, 3000);
  }, []);

  return (
    <motion.div
      className="flex items-center justify-center h-screen bg-black text-white"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 1 }}
    >
      <motion.div
        className="text-center flex flex-col justify-start items-center h-full pt-32"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
      >
        <h1
          className="text-8xl font-bold bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent tracking-tight cursor-pointer"
          style={{ fontFamily: "'Nova Square', sans-serif", fontSize: "10rem" }}
          onClick={() => navigate("/")}
        >
          repo.ai
        </h1>
        
        {/* Modified byline with stacked text */}
        <div 
          className="flex flex-col items-center cursor-pointer mt-2" 
          style={{ fontFamily: "'Geist Mono', monospace" }}
          onClick={() => navigate("/")}
        >
          <span className="text-sm text-white-400">by</span>
          <span className="text-4xl text-white-400">SYYFT</span>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default WelcomePage;