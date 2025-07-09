import React from 'react';
import { Menu } from 'lucide-react';
import { useUIStore } from '../store/uiStore';

const Header = () => {
  const toggleSidebar = useUIStore((state) => state.toggleSidebar);

  return (
    <header className="flex items-center h-12 bg-[#333333] px-4 shrink-0">
      <button 
        onClick={toggleSidebar} 
        className="text-gray-300 hover:text-white focus:outline-none"
        aria-label="Toggle sidebar"
      >
        <Menu size={24} />
      </button>
      <h1 className="ml-4 text-lg font-semibold text-gray-200">
        Ardi Agent
      </h1>
    </header>
  );
};

export default Header;