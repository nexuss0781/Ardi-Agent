import React from 'react';
import { Maximize, Minimize } from 'lucide-react';
import { useUIStore } from '../store/uiStore';

const ChatWindow = ({ isFullScreen = false }) => {
    const toggleChatFullScreen = useUIStore((state) => state.toggleChatFullScreen);
  
    return (
      <div className={`bg-[#252526] flex flex-col flex-1 ${isFullScreen ? 'h-screen w-screen' : ''}`}>
        <div className="flex items-center p-2 border-b border-b-[#333333] shrink-0">
          <h3 className="flex-1 text-sm font-bold text-gray-400 uppercase tracking-wider">
            Agent Chat
          </h3>
          <button 
            onClick={toggleChatFullScreen}
            className="text-gray-400 hover:text-white"
            title={isFullScreen ? "Exit Full Screen" : "Enter Full Screen"}
          >
            {isFullScreen ? <Minimize size={18} /> : <Maximize size={18} />}
          </button>
        </div>
  
        <div className="flex-1 p-4 overflow-y-auto">
          <p className="text-gray-400 text-sm">
            This is the placeholder for the agent chat window.
          </p>
          <p className="text-gray-500 text-xs mt-4">
            The full agentic workflow will be implemented in a future version.
          </p>
        </div>

        <div className="p-2 border-t border-t-[#333333]">
            <input 
                type="text"
                placeholder="Send a message..."
                className="w-full bg-[#3c3c3c] text-gray-200 border border-[#444] rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
        </div>
      </div>
    );
  };
  
  export default ChatWindow;