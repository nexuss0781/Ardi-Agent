import React from 'react';
import { useFileStore } from '../store/fileStore';
import { Save, CheckCircle } from 'lucide-react';

const StatusBar = () => {
  const { isSaving, activeFilePath } = useFileStore((state) => ({
    isSaving: state.isSaving,
    activeFilePath: state.activeFile.path,
  }));

  return (
    <div className="flex items-center h-6 px-4 bg-[#007acc] text-white text-xs shrink-0">
      <div className="flex items-center">
        {isSaving ? (
          <>
            <Save size={14} className="mr-2 animate-pulse" />
            <span>Saving...</span>
          </>
        ) : (
          <>
            <CheckCircle size={14} className="mr-2" />
            <span>Saved</span>
          </>
        )}
      </div>
      <div className="flex-1 text-center">
        {activeFilePath && <span>{activeFilePath}</span>}
      </div>
      <div className="w-24 text-right">
        <span>UTF-8</span>
      </div>
    </div>
  );
};

export default StatusBar;