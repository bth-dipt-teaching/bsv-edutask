
describe('Test UI-R8UC', () => {

  let user
  let task

  before(() => {

    cy.createUser().then((createdUser) => {

      user = createdUser

    })
  })

  beforeEach(() => {

    cy.createTask(user.id).then((createdTask) => {

      task = createdTask

    })

    const name = user.firstName + ' ' + user.lastName
    cy.visit('http://localhost:3000')

    cy.get('#email')
      .type(user.email)

    cy.get('form').submit()

    cy.get('h1').should('contain.text', 'Your tasks, ' + name)
    cy.get('.title-overlay').click()
  })

  afterEach(() => {

    cy.deleteTask(task.id)

  })

  after(() => {

    cy.deleteUser(user.id)

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

  it('if an item can be removed', () => {
    cy.get('.todo-item').should('have.length.at.least', 1)

    cy.get('.todo-item').last().within(() => {
      cy.get('.remover').click()
      cy.get('.todo-item').should('not.exist')
    })
  })

  it('check if active todo-item is done correctly', () => {
    cy.get('.todo-item').should('have.length.at.least', 1)

    cy.get('.todo-item').last().within(() => {
      cy.get('.checker').should('have.class', 'unchecked')
      cy.get('.checker').click()

      cy.get('.checker').should('have.class', 'checked')
    })
  })

  it('check if done todo-item is actived correctly', () => {
    cy.get('.todo-item').should('have.length.at.least', 1)

    cy.get('.todo-item').last().within(() => {
      cy.get('.checker').should('have.class', 'unchecked')
      cy.get('.checker').click()

      cy.get('.checker').should('have.class', 'checked')
      cy.get('.checker').click()

      cy.get('.checker').should('have.class', 'unchecked')
    })
  })
})