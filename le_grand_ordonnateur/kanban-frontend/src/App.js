import React from 'react';
import KanbanBoard from './KanbanBoard';

function App() {
  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <h1 className="text-2xl font-bold mb-4">Kanban Board</h1>
      <KanbanBoard />
    </div>
  );
}

export default App;
