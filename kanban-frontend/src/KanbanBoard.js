import React, { useState, useEffect } from "react";
import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";
import axios from "axios";

const KanbanBoard = () => {
  const [columns, setColumns] = useState({
  });
  const [editingTask, setEditingTask] = useState(null);

  // Récupérer les colonnes et les tâches depuis l'API
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/columns/")
      .then(response => {
        const columnsData = response.data;
        const updatedColumns = { ...columns };

        columnsData.forEach((column) => {
          updatedColumns[column.id] = {
            name: column.name,
            tasks: column.tasks.map(task => ({
              ...task,
              id: String(task.id),  // Convertir l'ID en string
            })),
            newTaskTitle: "", // Initialiser le champ de saisie pour chaque colonne
          };
        });

        setColumns(updatedColumns);
      })
      .catch(error => {
        console.error("Erreur de récupération des colonnes :", error);
      });
  }, []);
  const addTask = (columnId) => {
    const newTaskTitle = columns[columnId].newTaskTitle.trim();
  
    if (newTaskTitle) {
      // Assurez-vous que `columnId` contient l'ID de la colonne sous forme d'un nombre
      const columnIdNumeric = parseInt(columnId.replace('column-', ''), 10); // Extrait l'ID numérique
  
      const newTask = {
        title: newTaskTitle,
        column: columnIdNumeric, // L'ID numérique de la colonne
        position: columns[columnId].tasks.length, // La position de la tâche dans la colonne
      };
  
      // Ajouter la tâche au backend
      axios.post("http://127.0.0.1:8000/api/tasks/", newTask)
        .then(response => {
          const newTaskData = { ...response.data, id: String(response.data.id) }; // Convertir l'ID en string
          const updatedColumns = {
            ...columns,
            [columnId]: {
              ...columns[columnId],
              tasks: [...columns[columnId].tasks, newTaskData],
              newTaskTitle: "", // Réinitialiser le champ de saisie après l'ajout
            },
          };
          setColumns(updatedColumns);
        })
        .catch(error => {
          console.error("Erreur lors de l'ajout de la tâche :", error.response || error.message);
        });
    }
  };
    

  // Fonction pour modifier une tâche
  const handleTaskEdit = (columnId, taskId, value) => {
    const updatedColumns = {
      ...columns,
      [columnId]: {
        ...columns[columnId],
        tasks: columns[columnId].tasks.map((task) =>
          task.id === taskId ? { ...task, title: value } : task
        ),
      },
    };

    setColumns(updatedColumns);

    // Mettre à jour la tâche via l'API
    axios.patch(`http://127.0.0.1:8000/api/tasks/${taskId}/`, { title: value })
      .then((response) => {
        console.log("Tâche mise à jour :", response.data);
      })
      .catch((error) => {
        console.error("Erreur lors de la mise à jour de la tâche :", error.response || error.message);
      });
  };

  // Fonction pour supprimer une tâche
  const handleTaskDelete = (taskId, columnId) => {
    // Appel API pour supprimer la tâche
    axios.delete(`http://127.0.0.1:8000/api/tasks/${taskId}/`)
      .then(response => {
        console.log("Tâche supprimée :", response.data);

        // Mettre à jour l'état pour supprimer la tâche de la colonne
        const updatedColumns = {
          ...columns,
          [columnId]: {
            ...columns[columnId],
            tasks: columns[columnId].tasks.filter(task => task.id !== taskId),
          },
        };
        setColumns(updatedColumns);
      })
      .catch(error => {
        console.error("Erreur lors de la suppression de la tâche :", error.response || error.message);
      });
  };

  // Fonction de gestion du drag-and-drop
  const onDragEnd = (result) => {
    const { source, destination } = result;

    if (!destination) return; // Si aucune destination, on ne fait rien

    const sourceColumn = columns[source.droppableId];
    const destinationColumn = columns[destination.droppableId];

    const sourceTasks = Array.from(sourceColumn.tasks);
    const [movedTask] = sourceTasks.splice(source.index, 1);

    const destinationTasks = Array.from(destinationColumn.tasks);
    destinationTasks.splice(destination.index, 0, movedTask);

    setColumns({
      ...columns,
      [source.droppableId]: { ...sourceColumn, tasks: sourceTasks },
      [destination.droppableId]: { ...destinationColumn, tasks: destinationTasks },
    });

    // Déplacement entre les colonnes
    axios.patch(`http://127.0.0.1:8000/api/tasks/${movedTask.id}/`, {
      column: Number(destination.droppableId.replace('column-', '')), // Conversion de l'ID de la colonne en nombre
      position: destination.index,
    })
      .then(response => {
        console.log("Réponse de l'API pour le déplacement :", response.data);
      })
      .catch(error => {
        console.error("Erreur lors du déplacement de la tâche :", error.response || error.message);
      });
  };

  return (
    <div className="min-h-screen  from-background p-6">
      <h1 className="text-4xl font-bold mb-8 text-center  text-on-surface">Kanban Board</h1>
      <DragDropContext onDragEnd={onDragEnd}>
        <div className="flex flex-row justify-center gap-6">
          {Object.entries(columns).map(([columnId, column]) => (
            <Droppable key={columnId} droppableId={columnId}>
              {(provided) => (
                <div
                  {...provided.droppableProps}
                  ref={provided.innerRef}
                  className="w-72 bg-surface rounded-xl shadow-lg p-4"
                >
                  <h2 className="text-lg font-semibold mb-4 text-center text-on-surface">
                    {column.name}
                  </h2>
                  <div className="space-y-4">
                    {column.tasks.map((task, index) => (
                      <Draggable key={task.id} draggableId={task.id} index={index}>
                        {(provided) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className="p-4 bg-surface  text-on-surface hover:bg-surface-100 rounded-lg shadow-md border border-blue-200 transition-transform transform hover:scale-105"
                          >
                            <span>{task.title}</span>

                            {/* Bouton de suppression */}
                            <button
                              onClick={() => handleTaskDelete(task.id, columnId)}
                              className="mt-2 p-1 text-red-600 hover:text-red-800"
                            >
                              Supprimer
                            </button>
                          </div>
                        )}
                      </Draggable>
                    ))}
                  </div>

                  {/* Ajouter une tâche */}
                  <div className="mt-4">
                    <input
                      type="text"
                      value={column.newTaskTitle}
                      onChange={(e) => {
                        const updatedColumns = {
                          ...columns,
                          [columnId]: {
                            ...columns[columnId],
                            newTaskTitle: e.target.value,
                          },
                        };
                        setColumns(updatedColumns);
                      }}
                      placeholder="Ajouter une tâche"
                      className="w-full p-2 bg-surface  text-on-surface border border-gray-300 rounded focus:outline-none focus:ring focus:ring-blue-200"
                    />
                    <button
                      onClick={() => addTask(columnId)}
                      className="mt-2 p-2 bg-green-500  text-on-surface rounded w-full"
                    >
                      Ajouter
                    </button>
                  </div>

                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          ))}
        </div>
      </DragDropContext>
    </div>
  );
};

export default KanbanBoard;
