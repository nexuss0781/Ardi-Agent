import { create } from 'zustand';

// A helper function to recursively scan the directory
const scanDirectory = async (dirHandle) => {
  const entries = {};
  for await (const [name, handle] of dirHandle.entries()) {
    if (name.startsWith('.')) continue; // Ignore hidden files/folders

    if (handle.kind === 'directory') {
      entries[name] = {
        name,
        handle,
        kind: 'directory',
        children: await scanDirectory(handle),
      };
    } else {
      entries[name] = {
        name,
        handle,
        kind: 'file',
      };
    }
  }
  return entries;
};

export const useFileStore = create((set, get) => ({
  projectHandle: null,
  fileTree: {},
  activeFile: {
    handle: null,
    content: null,
    path: null,
  },
  isLoading: false,

  openProject: async () => {
    try {
      const dirHandle = await window.showDirectoryPicker();
      if (!dirHandle) return;

      set({ isLoading: true, fileTree: {}, projectHandle: dirHandle, activeFile: { handle: null, content: null, path: null } });
      const tree = await scanDirectory(dirHandle);
      set({ fileTree: tree, isLoading: false });
    } catch (e) {
      if (e.name !== 'AbortError') {
        console.error("Error opening directory:", e);
      }
      set({ isLoading: false });
    }
  },

  setActiveFile: async (fileHandle, filePath) => {
    try {
        set({ isLoading: true });
        const file = await fileHandle.getFile();
        const content = await file.text();
        set({ activeFile: { handle: fileHandle, content, path: filePath }, isLoading: false });
    } catch (e) {
        console.error("Error reading file:", e);
        set({ isLoading: false });
    }
  },
  
  updateActiveFileContent: (newContent) => {
    set((state) => ({
        activeFile: {
            ...state.activeFile,
            content: newContent,
        }
    }));
  },
}));