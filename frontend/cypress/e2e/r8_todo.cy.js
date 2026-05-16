describe('R8 Todo Tests', () => {

  beforeEach(() => {

    cy.visit('http://localhost:3000')

    // Open signup page
    cy.contains('Click here to sign up')
      .click()

    // Fill signup form
    cy.get('input').eq(0)
      .type(`test${Date.now()}@example.com`)

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

    cy.get('input[placeholder="Add a new todo item"]')
      .type('Toggle Todo')

    cy.contains('Add')
      .click()

    cy.contains('Toggle Todo')
      .should('exist')

    cy.contains('Toggle Todo')
      .click({ force: true })

  })

  // R8UC3 - Delete Todo
  it('deletes a todo item', () => {

    cy.get('input[placeholder="Add a new todo item"]')
      .type('Delete Todo')

    cy.contains('Add')
      .click()

    cy.contains('Delete Todo')
      .should('exist')

    cy.get('button')
      .last()
      .click({ force: true })

  })

    // Validation Test - Empty Todo
  it('should not add an empty todo item', () => {

    // Click Add without entering text
    cy.contains('Add')
      .click()

    // Expect no todo to be added
    cy.contains('')
      .should('not.exist')

  })

})