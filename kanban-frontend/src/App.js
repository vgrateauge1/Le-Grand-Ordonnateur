import React from 'react';
import KanbanBoard from './KanbanBoard';
import Navbar from './Navbar';

function App() {
  return (
    <div className="min-h-screen bg-background text-on-background p-4">

      <Navbar />
      <KanbanBoard />
    </div>
    
  );
}

export default App;
