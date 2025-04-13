document.addEventListener("DOMContentLoaded", () => {
    const taskInput = document.getElementById("taskInput");
    const addTaskButton = document.getElementById("addTaskButton");
    const taskList = document.getElementById("taskList");

    addTaskButton.addEventListener("click", addTask);
    taskInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            addTask();
        }
    });

    function addTask() {
        const taskText = taskInput.value.trim();
        if (taskText === "") return;

        const li = document.createElement("li");
        li.textContent = taskText;

        const editButton = document.createElement("button");
        editButton.textContent = "Edit";
        editButton.className = "edit";
        editButton.addEventListener("click", () => editTask(li));

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.className = "delete";
        deleteButton.addEventListener("click", () => {
            taskList.removeChild(li);
        });

        li.appendChild(editButton);
        li.appendChild(deleteButton);
        li.addEventListener("click", () => {
            li.classList.toggle("completed");
        });

        taskList.appendChild(li);
        taskInput.value = "";
    }

    function editTask(li) {
        const currentTaskText = li.textContent.split('EditDelete')[0].trim();
        taskInput.value = currentTaskText;
        taskList.removeChild(li);
        taskInput.focus();
    }
});