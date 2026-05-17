describe("Todo item GUI tests", () => {

  it("should create, toggle and delete a todo item for a task", () => {
    const userEmail = "cypress4@test.com"
    const taskTitle = "Cypress task " + Date.now()
    const todoTitle = "Cypress todo " + Date.now()

    cy.visit("http://localhost:3000")

    cy.get("input").eq(0)
      .clear()
      .type(userEmail + "{enter}")

    cy.contains("Your tasks", { timeout: 10000 })
      .should("exist")

    cy.get("input").eq(0)
      .clear()
      .type(taskTitle)

    cy.get("input").eq(1)
      .clear()
      .type("dQw4w9WgXcQ")

    cy.contains("Create new Task")
      .click({ force: true })

    cy.wait(2000)

    cy.get("img")
      .first()
      .click({ force: true })

    cy.wait(2000)

    cy.get('input[placeholder="Add a new todo item"]')
      .type(todoTitle, { force: true })

    cy.contains("Add")
      .click({ force: true })

    cy.contains(todoTitle)
      .should("exist")

    cy.contains("span", todoTitle)
      .prev()
      .click({ force: true })

    cy.wait(1000)

    cy.get(".todo-item")
      .last()
      .children()
      .last()
      .click({ force: true })

    cy.contains(todoTitle)
      .should("not.exist")
  })

})