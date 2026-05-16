describe('R8 Todo Tests', () => {

  beforeEach(() => {
    cy.visit('http://localhost:3000')
  })

  it('creates a todo', () => {

    cy.get('[data-cy=todo-input]')
      .type('Testing task')

    cy.get('[data-cy=add-todo]')
      .click()

    cy.contains('Testing task')
      .should('exist')
  })

  it('toggles a todo', () => {

    cy.get('[data-cy=todo-checkbox]')
      .first()
      .click()

    cy.get('[data-cy=todo-item]')
      .first()
      .should('have.class', 'completed')
  })

  it('deletes a todo', () => {

    cy.get('[data-cy=delete-btn]')
      .first()
      .click()

    cy.contains('Testing task')
      .should('not.exist')
  })

})