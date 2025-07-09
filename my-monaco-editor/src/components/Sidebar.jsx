import React from 'react';
import { FolderTree, MessageSquare } from 'lucide-react';
import { useUIStore } from '../store/uiStore';
import FileTree from './FileTree/FileTree.jsx';
import ChatWindow from './ChatWindow.jsx'; // <-- Standardized name

const Sidebar = () => {
  const { sidebarView, setSidebarView } = useUIStore((state) => ({
    sidebarView: state.sidebarView,
    setSidebarView: state.setSidebarView,
  }));

  return (
    <aside className="w-64 bg-[#252526] flex flex-col shrink-0">
      <div className="flex p-2 border-b border-b-[#333333] shrink-0">
        <button 
          onClick={() => setSidebarView('files')}
          title="File Explorer"
          className={`p-2 rounded focus:outline-none ${sidebarView === 'files' ? 'text-white bg-[#37373d]' : 'text-gray-400 hover:bg-[#37373d]'}`}
        >
          <FolderTree size={24} />
        </button>
        <button 
          onClick={() => setSidebarView('chat')}
          title="Agent Chat"
          className={`ml-2 p-2 rounded focus:outline-none ${sidebarView === 'chat' ? 'text-white bg-[#37373d]' : 'text-gray-400 hover:bg-[#37373d]'}`}
        >
          <MessageSquare size={24} />
        </button>
      </div>
      
      {sidebarView === 'files' && (
        <div className="flex flex-col flex-1 overflow-hidden">
          <h3 className="p-2 text-sm font-bold text-gray-400 uppercase tracking-wider shrink-0">
            File Explorer
          </h3>
          <FileTree />
        </div>
      )}
      
      {sidebarView === 'chat' && <ChatWindow />}
    </aside>
  );
};

export default Sidebar;