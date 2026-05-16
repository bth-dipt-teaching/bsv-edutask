describe("R8 - Todo GUI Testing", () => {
  let task;

  beforeEach(() => {
    cy.fixture("task").then((taskdata) => {
      task = taskdata;

      cy.visit("/");

      const uniqueEmail = `test${Date.now()}@gmail.com`;

      // switch to signup mode
      cy.contains("Have no account yet? Click here to sign up.").click();

      cy.get("#email").type(uniqueEmail);

      cy.get("#firstname").type("Mon");

      cy.get("#lastname").type("Doe");

      cy.contains("Sign Up").click();

      cy.contains("Your tasks", { timeout: 10000 }).should("exist");
    });
  });

  const createAndOpenTask = () => {
    cy.get("#title").type(task.title);

    const videoKey = task.url.includes("watch?v=")
      ? task.url.split("watch?v=")[1]
      : "dQw4w9WgXcQ";

    cy.get("#url").type(videoKey);

    cy.contains("Create new Task").click();

    cy.contains(task.title, { timeout: 10000 }).should("exist");

    cy.contains(task.title).click();

    cy.get('input[placeholder="Add a new todo item"]').should("exist");
  };

  // -------------------------
  // R8UC1 - End Condition
  // -------------------------
  it("R8UC1 - should create a todo item", () => {
    createAndOpenTask();

    cy.get('input[placeholder="Add a new todo item"]').type("Todo 1");

    cy.contains("Add").click();

    cy.contains("Todo 1").should("exist");
  });

  // -------------------------
  // R8UC1 - Alternative Scenario
  // -------------------------
  it("R8UC1 - should not create an empty todo item", () => {
    createAndOpenTask();

    cy.get('input[placeholder="Add a new todo item"]').should("have.value", "");

    cy.get(".todo-item").then(($itemsBefore) => {
      const countBefore = $itemsBefore.length;

      cy.contains("Add").click();

      cy.get(".todo-item").should("have.length", countBefore);
    });
  });

  // -------------------------
  // R8UC2 - Toggle Todo
  // -------------------------
  it("R8UC2 - should toggle a todo item", () => {
    createAndOpenTask();

    cy.get('input[placeholder="Add a new todo item"]').type("Toggle todo");

    cy.contains("Add").click();

    cy.contains("Toggle todo").parents(".todo-item").find(".checker").click();

    cy.contains("Toggle todo")
      .parents(".todo-item")
      .find(".checker")
      .should("have.class", "checked");
  });

  // -------------------------
  // R8UC3 - Delete Todo
  // -------------------------
  it("R8UC3 - should delete a todo item", () => {
    createAndOpenTask();

    cy.get('input[placeholder="Add a new todo item"]').type("Delete me");

    cy.contains("Add").click();

    cy.contains("Delete me").should("exist");

    cy.contains("Delete me").parents(".todo-item").find(".remover").click();

    cy.contains("Delete me").should("not.exist");
  });
});
