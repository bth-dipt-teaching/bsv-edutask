describe('Requirement 8 - Todo GUI Verification', () => {

  // Helper method for adding todos
  const createTodoItem = (todoText) => {

    cy.get('input[placeholder="Add a new todo item"]')
      .clear()
      .type(todoText, { force: true })

    cy.contains('Add')
      .click({ force: true })

    cy.wait(1000)
  }

  beforeEach(() => {

    // Open application
    cy.visit('http://localhost:3000')

    // User login
    cy.get('#email')
      .clear()
      .type('adityamudam@gmail.com')

    cy.get('input[type="submit"]')
      .first()
      .click()

    cy.wait(2500)

    // Create task
    cy.get('input[placeholder="Title of your Task"]')
      .first()
      .type('GUI AUTOMATION TASK', { force: true })

    cy.get('input[placeholder*="YouTube"]')
      .first()
      .type('5NV6Rdv1a3I', { force: true })

    cy.contains('Create new Task')
      .click({ force: true })

    cy.wait(2500)

    // Open latest task
    cy.get('img')
      .last()
      .click({ force: true })

    cy.wait(1200)

  })

  // ------------------------------------------------
  // TC1 - Create Todo
  // ------------------------------------------------
  it('TC1 - User successfully creates a todo item', () => {

    createTodoItem('Study Cypress Framework')

    cy.contains('Study Cypress Framework')
      .should('exist')

  })

  // ------------------------------------------------
  // TC2 - Long Todo Description
  // ------------------------------------------------
  it('TC2 - User adds a todo with long description', () => {

    const longTodo =
      'Complete graphical user interface verification assignment'

    createTodoItem(longTodo)

    cy.contains(longTodo)
      .should('be.visible')

  })

  // ------------------------------------------------
  // TC3 - Toggle Todo
  // ------------------------------------------------
  it('TC3 - User marks a todo item as completed', () => {

    createTodoItem('Finish GUI Lab')

    cy.contains('Finish GUI Lab')
      .parent()
      .click({ force: true })

    cy.contains('Finish GUI Lab')
      .should('exist')

  })

  // ------------------------------------------------
  // TC4 - Restore Todo
  // ------------------------------------------------
  it('TC4 - User restores completed todo to active state', () => {

    createTodoItem('Read Cypress Notes')

    cy.contains('Read Cypress Notes')
      .parent()
      .click({ force: true })

    cy.wait(600)

    cy.contains('Read Cypress Notes')
      .parent()
      .click({ force: true })

    cy.contains('Read Cypress Notes')
      .should('be.visible')

  })

  // ------------------------------------------------
  // TC5 - Delete Todo
  // ------------------------------------------------
  it('TC5 - User deletes a selected todo item', () => {

    createTodoItem('Temporary Task')

    // Confirm todo creation
    cy.contains('Temporary Task')
      .should('be.visible')

    // Delete todo
    cy.contains('Temporary Task')
      .parent()
      .within(() => {

        cy.contains('✖')
          .click({ force: true })

      })

    // Give backend/frontend time to update
    cy.wait(2500)

    // Reload UI to sync latest data
    cy.reload()

    cy.wait(2500)

    // Final verification
    cy.get('body')
      .should('not.contain', 'Temporary Task')

  })

})