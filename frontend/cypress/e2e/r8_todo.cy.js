describe('R8 Todo Tests', () => {

  beforeEach(() => {

    cy.visit('http://localhost:3001')

    // Open signup page
    cy.contains('Click here to sign up')
      .click()

    // Fill signup form
    cy.get('input').eq(0)
      .type('test@example.com')

    cy.get('input').eq(1)
      .type('Test')

    cy.get('input').eq(2)
      .type('User')

    // Signup
    cy.contains('Sign Up')
      .click()

    // Create task
    cy.get('input[placeholder="Title of your Task"]')
      .type('Testing task')

    cy.get('input[placeholder*="Viewkey"]')
      .type('7wtfhZwyrcc')

    cy.contains('Create new Task')
      .click()

    // Open created task
    cy.contains('Testing task')
      .click({ force: true })

  })

  // R8UC1 - Create Todo
  it('creates a todo item', () => {

    cy.get('input[placeholder="Add a new todo item"]')
      .type('My Todo')

    cy.contains('Add')
      .click()

    cy.contains('My Todo')
      .should('exist')

  })

  // R8UC2 - Toggle Todo
  it('toggles a todo item', () => {

    // Create todo first
    cy.get('input[placeholder="Add a new todo item"]')
      .type('Toggle Todo')

    cy.contains('Add')
      .click()

    // Click todo item to toggle
    cy.contains('Toggle Todo')
      .click({ force: true })

  })

  // R8UC3 - Delete Todo
  it('deletes a todo item', () => {

    // Create todo first
    cy.get('input[placeholder="Add a new todo item"]')
      .type('Delete Todo')

    cy.contains('Add')
      .click()

    // Delete todo
    cy.get('button')
      .last()
      .click({ force: true })

  })

})