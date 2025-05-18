describe('Assignment 4 – GUI Tests (R8UC1–R8UC3)', () => {
  const email = 'rama@test.com'
  const taskTitle = `Test Task ${Date.now()}`
  const todoTextToggle = `Auto-todo for toggle ${Date.now()}`
  const todoTextDelete = `Auto-todo to delete ${Date.now()}`

  beforeEach(() => {
    cy.visit('http://localhost:3000')

    // Login with test user
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)

    cy.get('form').submit()
    cy.wait(500)

    cy.get('h1').should('contain.text', 'Your tasks')

    // Create a unique task
    cy.get('input[placeholder="Title of your Task"]').type(taskTitle)
    cy.get('input[placeholder*="YouTube"]').type('50XKNKGPWs8')
    cy.contains('Create new Task').click()

    cy.contains('div.title-overlay', taskTitle).click()
  })
  
  it('R8UC1 – adds a new task', () => {
    cy.get('h1 span.editable').should('contain.text', taskTitle)

    // Only if video preview is expected
    // cy.get('.videoWrapper iframe', { timeout: 5000 }).should('exist')
  })
  it('R8UC2 – opens video and toggles a task checkbox', () => {
    // Add a checkbox todo
    cy.get('form.inline-form').scrollIntoView()
    cy.get('input[placeholder="Add a new todo item"]').type(todoTextToggle, { force: true })
    cy.get('input[type="submit"][value="Add"]').click({ force: true })
    cy.wait(500)
  
    // Toggle ON
    cy.contains('li.todo-item', todoTextToggle)
      .find('span.checker')
      .click({ force: true })
      .should('have.class', 'checked')
  
    // Toggle OFF
    cy.contains('li.todo-item', todoTextToggle)
      .find('span.checker')
      .click({ force: true })
      .should('have.class', 'unchecked')
  })
  
  it('R8UC3 – deletes a task', () => {
    // Add a todo item
    cy.get('form.inline-form').scrollIntoView()
    cy.get('input[placeholder="Add a new todo item"]').type(todoTextDelete, { force: true })
    cy.get('input[type="submit"][value="Add"]').click({ force: true })
    cy.wait(500)

    // Delete the todo item
    cy.contains('li.todo-item', todoTextDelete)
      .find('span.remover')
      .click({ force: true })

    // Reload and assert the todo no longer exists
    cy.reload()
    cy.contains('li.todo-item', todoTextDelete, { timeout: 8000 }).should('not.exist')
  })
})
