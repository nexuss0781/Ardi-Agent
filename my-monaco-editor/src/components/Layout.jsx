import React from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import Terminal from './Terminal';
import Editor from './Editor';
import StatusBar from './StatusBar';
import ChatWindow from './FileTree/ChatWindow.jsx';

import { useUIStore } from '../store/uiStore';

const Layout = () => {
  const isSidebarOpen = useUIStore((state) => state.isSidebarOpen);
  const isChatFullScreen = useUIStore((state) => state.isChatFullScreen);

  if (isChatFullScreen) {
    return <ChatWindow isFullScreen={true} />;
  }

  

  return (
    <div className="flex flex-col h-screen w-screen bg-[#1e1e1e]">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        {isSidebarOpen && <Sidebar />}
        <main className="flex-1 flex flex-col bg-[#1e1e1e] overflow-hidden">
            <Editor />
            <StatusBar />
            <Terminal />
        </main>
      </div>
    </div>
  );
};

export default Layout;