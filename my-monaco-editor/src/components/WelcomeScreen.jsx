import React from 'react';
import { FolderKanban } from 'lucide-react';
import { useFileStore } from '../store/fileStore';

const WelcomeScreen = () => {
  const openProject = useFileStore((state) => state.openProject);
  const isLoading = useFileStore((state) => state.isLoading);

  return (
    <div className="flex flex-col items-center justify-center h-screen w-screen bg-[#1e1e1e]">
      <h1 className="text-4xl font-bold text-gray-200 mb-4">Ardi Agent Environment</h1>
      <p className="text-lg text-gray-400 mb-8">Open a local folder to begin working.</p>
      <button
        onClick={openProject}
        disabled={isLoading}
        className="flex items-center px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors disabled:bg-gray-500"
      >
        <FolderKanban className="mr-3" size={24} />
        {isLoading ? 'Loading Project...' : 'Open Folder'}
      </button>
      <p className="text-xs text-gray-500 mt-8">Your files stay on your computer. No data is uploaded.</p>
    </div>
  );
};

export default WelcomeScreen;