describe('Add todo', () => {
  beforeEach(() => {
    cy.visit('/')

    cy.get('#email').type('zoe@gmail.com')

     cy.get('input[type="submit"]')
  .should('be.enabled')
  .click()
  })

  it('should create a new todo item', () => {
    const description = 'HEHEUE'

    cy.get('#title').type(description)

     cy.get('input[type="submit"]')
    .should('be.enabled')
    .click()

    cy.get('.title-overlay')
    .last()
    .should('contain.text', description)
  })

  it('should not create a new todo', () => {
    cy.get('input[type="submit"]')
      .should('be.disabled')
  })
  it('If icon is pressed and todo item is active, it should set the item to done and todo item is struck through', () => {
    cy.get('.container-element')
    .eq(-2)
    .click()

    cy.get('.checker.unchecked')
    .click()

    cy.get('.close-btn')
    .click({ force: true })
  })
  it('If icon is pressed and todo item is done, the item should be set to active', () => {
    cy.get('.container-element')
    .eq(-2)
    .click()

    cy.get('.checker.checked')
    .click()

    cy.get('.close-btn')
    .click({ force: true })
  })
  it('should delete todo item when X is pressed', () => {
    cy.get('.container-element').then(($before) => {
      const countBefore = $before.length
      cy.get('.container-element')
      .eq(-2)
      .click()

      cy.get('.popup')
        .should('be.visible')

      cy.contains('.popup .todo-item', 'Watch video')
        .find('.remover')
        .click({ force: true })

      cy.get('.container-element')
        .should('have.length', countBefore - 1)
    })
  })
})