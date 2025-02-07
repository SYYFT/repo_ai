import { useEffect } from "react";
import { motion } from "framer-motion";

const WelcomePage = () => {
  console.log("WelcomePage is rendering!"); // ✅ Debugging Log

  useEffect(() => {
    console.log("Navigating to /file-explorer in 3 seconds..."); // ✅ Debugging Log
    setTimeout(() => {
      window.location.href = "/file-explorer";
    }, 9000);
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
        className="text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
      >
        <h1 className="text-6xl font-bold">Repo.ai by SYYFT</h1>
        <p className="text-xl mt-4">Understand Your Code Instantly.</p>
      </motion.div>
    </motion.div>
  );
};

export default WelcomePage;
