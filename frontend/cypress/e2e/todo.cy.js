describe("Requirement R8 : Manipulate todo items", () => {
    let uid, name, email;
    let taskId, taskTitle
    let baseTodoDesc, todoItemsLength;
    before(function () {
        //Copied from login.cy.js creating user.
        return cy.fixture("user.json")
        .then((user) => {
            return cy.request({
            method: "POST",
            url: "http://localhost:5000/users/create",
            form: true,
            body: user
            }).then((response) => {
            uid = response.body._id.$oid
            name = user.firstName + ' ' + user.lastName
            email = user.email
            })
        })
    });

    beforeEach(() => {
        //Override the view port settings, otherwise cypress cant find items that go out of its bounds in cypress tooling.
        //Found at https://docs.cypress.io/api/commands/viewport
        cy.viewport(1080, 1920);

        //Creating task from task.json 
        return cy.fixture("task.json")
            .then((task) => {
                //Adding required user id.
                task.userid = uid;
                return cy.request({
                    method: "POST",
                    url: "http://localhost:5000/tasks/create",
                    form: true,
                    body: task,
                }).then((response) => {
                    let tasks = response.body;
                    let lastIdx = tasks.length -1;
                    todoItemsLength = tasks[lastIdx].todos.length;
                    baseTodoDesc = tasks[lastIdx].todos[0].description;
                    taskId = tasks[lastIdx]._id.$oid;
                    taskTitle = tasks[lastIdx].title;
                
                })
            }).then(() => {
                // // Ensure login
                cy.visit("http://localhost:3000");
                cy.reload();
                cy.get("#email").type(email);
                cy.get("input[value=Login]").click();

                // // Ensure Task is selected
                cy.contains(".title-overlay", taskTitle)
                .parent("a")
                .click()
            })
        }
       
)
    
    describe("[R8UC1] : Add Todo Items", () => {
        it("Test Add Description filled", () => {
            //Arrange
            let newInputText = "new test todo"
            let expectedLength = todoItemsLength + 1;
            cy.get(".inline-form > [type='text']").should("be.visible")
            //Act
            cy.get(".inline-form > [type='text']").type(newInputText);
            cy.get(".inline-form > [type='submit']").click();
            
            //Assert
            cy.get(".todo-list li.todo-item").should("have.length", expectedLength);
            cy.get(".todo-list li.todo-item").last().should("contain.text", newInputText);
             
        });

        it("Test Add Description empty", () => {
            //Arrange
            //Act
            //Assert
            cy.get(".inline-form > [type='text']").should("contain.text", "");
            cy.get(".inline-form > [type='submit']").should("be.disabled");
        });
    });

    describe("[R8UC2] : Toggle Todo Item", () => {
   
        it("Test toggle done", () => {
            //Arrange
            //Act
            cy.get(".todo-list li.todo-item").first().find(".checker").click({force : true});
            //Assert
            cy.get(".todo-list li.todo-item").first().find(".checker").should("have.class", "checked");
            cy.get(".todo-list li.todo-item").first().find(".editable").should("have.css", "text-decoration-line", "line-through");
        });

        it("Test toggle active", () => {
            //Arrange
            cy.get(".todo-list li.todo-item").first().find(".checker").click({force : true});
      
            //Act
            cy.get(".todo-list li.todo-item").first().find(".checker").click({force : true});
            //Assert
            cy.get(".todo-list li.todo-item").first().find(".checker").should("have.class", "unchecked");
            cy.get(".todo-list li.todo-item").first().find(".editable").should("not.have.css", "text-decoration-line", "line-through");
        });
    });

    describe("[R8UC3] : Delete Todo Item", () => {
     
        it("Test remove todo item", () => {
            //Arrange
            const expectedLength = todoItemsLength > 0 ? (todoItemsLength) - 1 : 0;
           
            //Act
            cy.get(".todo-list li.todo-item").first().find(".remover").click({force : true});
            //For me the click only registers correctly if I add two of the same command.
            //Unsure why but I assume its a react+cypress timing issue, for triggering the event.
            // cy.get(".todo-list li.todo-item").first().find(".remover").click({force : true});
      
            // Assert
            cy.get(".todo-list li.todo-item").should("have.length", expectedLength);
            cy.get(".todo-list").contains(baseTodoDesc).should("not.exist");
  
         });
    });
    afterEach(function () {
       
        cy.request("DELETE",`http://localhost:5000/tasks/byid/${taskId}`)   
        
    })
    after(function () {
        cy.request("DELETE", `http://localhost:5000/users/${uid}`)
    });
});

