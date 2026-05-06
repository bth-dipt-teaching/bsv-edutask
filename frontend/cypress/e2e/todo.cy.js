describe('E2E test of to-do', () => {
  // Reused variables (code reused from login.cy.js)
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  // Code reused from login.cy.js
  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
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

  // Code reused from login.cy.js - changed to beforeEach for new test start state
  beforeEach('login to the system with an existing account', () => {
    // Make sure every test starts in a logged in state
    cy.visit('http://localhost:3000') // Added initial direction
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)

    cy.get('form')
      .submit()

    cy.get('h1')
      .should('contain.text', 'Your tasks, ' + name)
  })


  it('R8UC1: Create new to-do', () => {
    // Create task with title and youtube-affiliation
    cy.get('#title')
      .type('Test task from cypress test')
    cy.get('#url')
      .type('j_uu6bJ2IGI')
    cy.contains('input[type="submit"]', 'Create new Task')
      .click()

    // Navigate to created task
    cy.contains('.title-overlay', 'Test task from cypress test')
      .click()

    cy.get('.popup .todo-list', { timeout: 20000 })
      .should('be.visible')

    // Get created task, add to-do and verify visibility
    cy.get('.popup input[placeholder="Add a new todo item"]')
      .scrollIntoView()
      .type('Test-todo 1')
    cy.get('.popup input[value="Add"]')
      .scrollIntoView()
      .click()
    cy.contains('.todo-item', 'Test-todo 1')
      .should('be.visible')
  })

  it('R8UC2: Toggle to-do', () => {
    // Create task with title and youtube-affiliation
    cy.get('#title')
      .scrollIntoView()
      .type('Test task from cypress test')
    cy.get('#url')
      .scrollIntoView()
      .type('j_uu6bJ2IGI')
    cy.contains('input[type="submit"]', 'Create new Task')
      .scrollIntoView()
      .click()

    // Navigate to created task
    cy.contains('.title-overlay', 'Test task from cypress test')
      .scrollIntoView()
      .click()
    
    cy.get('.popup .todo-list', { timeout: 20000 })
      .should('be.visible')

    cy.contains('.todo-item', 'Watch video')
      .find('.checker')
      .should('have.class', 'unchecked')
    
    cy.contains('.todo-item', 'Watch video')
      .find('.checker')
      .click()
    
    cy.contains('.todo-item', 'Watch video')
      .find('.checker')
      .should('have.class', 'checked')
    
    cy.contains('.todo-item', 'Watch video')
      .find('.checker')
      .click()
    
    cy.contains('.todo-item', 'Watch video')
      .find('.checker')
      .should('have.class', 'unchecked')
  })

  it('R8UC3: Delete to-do', () => {
    // Create task with title and youtube-affiliation
    cy.get('#title')
      .type('Test task from cypress test')
    cy.get('#url')
      .type('j_uu6bJ2IGI')
    cy.contains('input[type="submit"]', 'Create new Task')
      .click()

    // Navigate to created task
    cy.contains('.title-overlay', 'Test task from cypress test')
      .click()

    cy.get('.popup .todo-list', { timeout: 20000 })
      .should('be.visible')
    
    cy.contains('.todo-item', 'Watch video')
      .find('.remover')
      .click()
    
      cy.contains('.todo-item', 'Watch video')
        .should('not.exist')    
  })

  // Code reused from login.cy.js to clear test-data
  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})
