describe('Assignment 4 GUI Tests', () => {

  let uid
  let name
  let email

  before(function () {
    cy.fixture('user.json').then((user) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
      }).then((response) => {
        uid = response.body._id.$oid
        name = user.firstName + ' ' + user.lastName
        email = user.email
      })
    })
  })
  
  beforeEach(function () {
    cy.visit('http://localhost:3000')
    cy.contains('div', 'Email Address')

    .find('input[type=text]')

    .type(email)

    cy.get('form').submit()
    cy.contains('Your tasks').should('be.visible')

  })

  after(function () {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })

  // R8UC1 - CREATE TODO ITEM
  it('Create Todo Example 1', () => {
    cy.get('body').then(($body) => {
      if ($body.find('input[placeholder="Title of your Task"]').length > 0) {
        cy.get('input[placeholder="Title of your Task"]')
          .first().clear().type('Python Tutorial for Beginners')
        cy.get('input[placeholder*="Viewkey"]')
          .first().clear({ force: true }).type('_uQrJ0TkZlc', { force: true })
        cy.contains('Create new Task').click()
      }
    })
  })

  it('Create Todo Example 2', () => {
    cy.get('body').then(($body) => {
      if ($body.find('input[placeholder="Title of your Task"]').length > 0) {
        cy.get('input[placeholder="Title of your Task"]')
          .first().clear().type('JavaScript Tutorial for Beginners')
        cy.get('input[placeholder*="Viewkey"]')
          .first().clear({ force: true }).type('W6NZfCO5SIk', { force: true })
        cy.contains('Create new Task').click()
      }
    })
  })

  it('Create Todo Example 3', () => {
    cy.get('body').then(($body) => {
      if ($body.find('input[placeholder="Title of your Task"]').length > 0) {
        cy.get('input[placeholder="Title of your Task"]')
          .first().clear().type('React Tutorial for Beginners')
        cy.get('input[placeholder*="Viewkey"]')
          .first().clear({ force: true }).type('Ke90Tje7VS0', { force: true })
        cy.contains('Create new Task').click()
      }
    })
  })

  // R8UC2 - TOGGLE TODO ITEM
  it('Toggle Todo Example 1', () => {
    cy.get('body').then(($body) => {
      if ($body.find('input[type="checkbox"]').length > 0) {
        cy.get('input[type="checkbox"]').first().click({ force: true })
      }
    })
  })

  it('Toggle Todo Example 2', () => {
    cy.get('body').then(($body) => {
      if ($body.find('input[type="checkbox"]').length > 1) {
        cy.get('input[type="checkbox"]').eq(1).click({ force: true })
      }
    })
  })

  it('Toggle Todo Example 3', () => {
    cy.get('body').then(($body) => {
      if ($body.find('input[type="checkbox"]').length > 0) {
        cy.get('input[type="checkbox"]').last().click({ force: true })
      }
    })
  })

  // R8UC3 - DELETE TODO ITEM
  it('Delete Todo Example 1', () => {
    cy.get('body').then(($body) => {
      if ($body.text().includes('Delete')) {
        cy.contains('Delete').first().click({ force: true })
      }
    })
  })

  it('Delete Todo Example 2', () => {
    cy.get('body').then(($body) => {
      if ($body.text().includes('Delete')) {
        cy.contains('Delete').eq(1).click({ force: true })
      }
    })
  })

  it('Delete Todo Example 3', () => {
    cy.get('body').then(($body) => {
      if ($body.text().includes('Delete')) {
        cy.contains('Delete').last().click({ force: true })
      }
    })
  })

})