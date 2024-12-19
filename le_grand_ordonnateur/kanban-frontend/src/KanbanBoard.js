import React, { useState, useEffect } from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import api from './api';

const KanbanBoard = () => {
  const [columns, setColumns] = useState([]);

  useEffect(() => {
    api.get('columns/')
      .then(response => setColumns(response.data))
      .catch(error => console.error("Erreur lors du chargement des colonnes :", error));
  }, []);

  const handleDragEnd = async (result) => {
    if (!result.destination) return;

    const { source, destination } = result;

    const sourceColumn = columns.find(col => col.id === parseInt(source.droppableId));
    const destinationColumn = columns.find(col => col.id === parseInt(destination.droppableId));

    const sourceTasks = Array.from(sourceColumn.tasks);
    const [movedTask] = sourceTasks.splice(source.index, 1);

    const destinationTasks = Array.from(destinationColumn.tasks);
    destinationTasks.splice(destination.index, 0, movedTask);

    setColumns(columns.map(col => {
      if (col.id === sourceColumn.id) return { ...col, tasks: sourceTasks };
      if (col.id === destinationColumn.id) return { ...col, tasks: destinationTasks };
      return col;
    }));

    try {
      await api.patch(`tasks/${movedTask.id}/`, {
        column: destinationColumn.id,
        position: destination.index,
      });
    } catch (error) {
      console.error("Erreur lors de la mise à jour de la tâche :", error);
    }
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <div className="flex space-x-4 p-4">
        {columns.map(column => (
          <Droppable key={column.id} droppableId={`${column.id}`}>
            {(provided) => (
              <div
                {...provided.droppableProps}
                ref={provided.innerRef}
                className="w-64 bg-gray-100 p-4 rounded-lg shadow-md"
              >
                <h2 className="text-xl font-bold">{column.name}</h2>
                {column.tasks.map((task, index) => (
                  <Draggable key={task.id} draggableId={`${task.id}`} index={index}>
                    {(provided) => (
                      <div
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                        ref={provided.innerRef}
                        className="bg-white p-2 rounded-md shadow-sm my-2"
                      >
                        {task.title}
                      </div>
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        ))}
      </div>
    </DragDropContext>
  );
};

export default KanbanBoard;
