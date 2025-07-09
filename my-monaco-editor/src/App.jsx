import React from 'react';
import Layout from './components/Layout';
import WelcomeScreen from './components/WelcomeScreen';
import { useFileStore } from './store/fileStore';

function App() {
  const projectHandle = useFileStore((state) => state.projectHandle);

  return (
    <div className="h-full w-full">
      {projectHandle ? <Layout /> : <WelcomeScreen />}
    </div>
  );
}

export default App;