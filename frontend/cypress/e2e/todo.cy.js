describe("Requirement R8 : Manipulate todo items", () => {
    let uid, name, email;
    let taskId, taskTitle;
    let baseTodoDesc, todoItemsLength;

    before(function () {
        // Create user once before all tests
        return cy.fixture("user.json")
        .then((user) => {
            return cy.request({
                method: "POST",
                url: "http://localhost:5000/users/create",
                form: true,
                body: user
            }).then((response) => {
                uid = response.body._id.$oid;
                name = user.firstName + ' ' + user.lastName;
                email = user.email;
            });
        });
    });

    beforeEach(() => {
        
        cy.viewport(1080, 1920);

        // Create a fresh task.json
        return cy.fixture("task.json")
            .then((task) => {
                task.userid = uid;
                return cy.request({
                    method: "POST",
                    url: "http://localhost:5000/tasks/create",
                    form: true,
                    body: task,
                }).then((response) => {
                    let tasks = response.body;
                    let lastIdx = tasks.length - 1;
                    todoItemsLength = tasks[lastIdx].todos.length;
                    baseTodoDesc = tasks[lastIdx].todos[0].description;
                    taskId = tasks[lastIdx]._id.$oid;
                    taskTitle = tasks[lastIdx].title;
                });
            }).then(() => {
                // Login and navigate to the task
                cy.visit("http://localhost:3000");
                cy.reload();
                cy.get("#email").type(email);
                cy.get("input[value=Login]").click();

                cy.contains(".title-overlay", taskTitle)
                    .parent("a")
                    .click();
            });
    });

    describe("[R8UC1] : Add Todo Items", () => {

        it("Test Add Description filled", () => {
            // Arrange
            let newInputText = "new test todo";
            let expectedLength = todoItemsLength + 1;
            cy.get(".inline-form > [type='text']").should("be.visible");
            // Act
            cy.get(".inline-form > [type='text']").type(newInputText);
            cy.get(".inline-form > [type='submit']").click();
            // Assert - new item appended to bottom of list
            cy.get(".todo-list li.todo-item").should("have.length", expectedLength);
            cy.get(".todo-list li.todo-item").last().should("contain.text", newInputText);
        });


        it("Test Add Description empty", () => {
            // Arrange / Act / Assert
            cy.get(".inline-form > [type='text']").should("have.value", "");
            cy.get(".inline-form > [type='submit']").should("be.disabled");
        });
    });

    describe("[R8UC2] : Toggle Todo Item", () => {

        it("Test toggle done", () => {
            // Act - click checker to set item to done
            cy.get(".todo-list li.todo-item").first().within(() => {
                cy.get(".checker").should("not.have.class", "checked");
                cy.get(".checker").click({ force: true });
                // Assert - item is struck through and marked as done
                cy.get(".checker").should("have.class", "checked");
                cy.get(".editable").should("have.css", "text-decoration-line", "line-through");
            });
        });

        it("Test toggle active", () => {
            cy.get(".todo-list li.todo-item").first().within(() => {
                // Arrange - set item to done first
                cy.get(".checker").click({ force: true });
                // Wait for UI to update before clicking again 
                cy.get(".checker").should("have.class", "checked");

                // Act - click again to set back to active
                cy.get(".checker").click({ force: true });

                // Assert
                cy.get(".checker").should("not.have.class", "checked");
                cy.get(".editable").should("not.have.css", "text-decoration-line", "line-through");
            });
        });
    });

    describe("[R8UC3] : Delete Todo Item", () => {

        it("Test remove todo item", () => {
            // Arrange
            const expectedLength = todoItemsLength > 0 ? todoItemsLength - 1 : 0;

            // Act
            cy.get(".todo-list li.todo-item").first().within(() => {
                cy.get(".remover").click();
            });

            // Assert
            cy.get(".todo-list li.todo-item").should("have.length", expectedLength);
            cy.get(".todo-list").contains(baseTodoDesc).should("not.exist");
        });
    });

    afterEach(function () {
        cy.request("DELETE", `http://localhost:5000/tasks/byid/${taskId}`);
    });

    after(function () {
        cy.request("DELETE", `http://localhost:5000/users/${uid}`);
    });
});
