import { create } from 'zustand';

export const useUIStore = create((set) => ({
  isSidebarOpen: false,
  isTerminalOpen: true,
  sidebarView: 'files', // 'files' or 'chat'
  isChatFullScreen: false,
  
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  toggleTerminal: () => set((state) => ({ isTerminalOpen: !state.isTerminalOpen })),
  setSidebarView: (view) => set({ sidebarView: view }),
  toggleChatFullScreen: () => set((state) => ({ isChatFullScreen: !state.isChatFullScreen })),
}));