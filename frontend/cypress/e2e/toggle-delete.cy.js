describe('task — toggle and delete', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000')
    cy.get('#email').type('mon.doe@gmail.com')
    cy.get('input[type="submit"]').click()

    cy.get('img').click()
  })

  it('check if unchecked todo-item is checked correctly', () => {
    cy.get('.todo-item').should('have.length.at.least', 1)

    cy.get('.todo-item').last().within(() => {
      cy.get('.checker').should('have.class', 'unchecked')
      cy.get('.checker').click()

      cy.get('.checker').should('have.class', 'checked')
    })
  })

  it('check if checked todo-item is unchecked correctly', () => {
    cy.get('.todo-item').last().within(() => {
      cy.get('.checker').should('have.class', 'checked')
      cy.get('.checker').click()

      cy.get('.checker').should('have.class', 'unchecked')
    })
  })

  it('if an item can be removed', () => {
    cy.get('.todo-item').last().within(() => {
      cy.get('.remover').click()
      cy.get('.todo-item').should('not.exist')
    })
  })
})
