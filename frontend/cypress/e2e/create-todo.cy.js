describe('task — create', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000')
    cy.get('#email').type('mon.doe@gmail.com')
    cy.get('input[type="submit"]').click()

    cy.get('img').click()
  })

  it('getting detail page', () => {
    cy.get('.todo-item').should('be.visible')
  })

  it('add with non empty description', () => {
    cy.get('.inline-form input[type="text"]').type('this is good')
    cy.get('.inline-form input[type="submit"]').click()

    cy.get('.todo-item').should('have.length', 2)
  })

  it('add with empty description', () => {
    cy.get('.inline-form input[type="text"]').should('have.value', '')
    cy.get('.inline-form input[type="submit"]').should('be.disabled')
  })
})