describe('E2E test of to-do failures', () => {
  // Reused variables (code reused from login.cy.js)
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user
  let char_limit = 'oyehpfiyegtzapwvmjltladnwhrjcihkiborfbilclttgyzfcymjesjgyliajrlfgrojyqfyotljlnugjyncabgwbejxqvydsbag'
  let char_limit_breach = 'oyehpfiyegtzapwvmjltladnwhrjcihkiborfbilclttgyzfcymjesjgyliajrlfgrojyqfyotljlnugjyncabgwbejxqvydsbaga'
  let alternate_char = 'ด5ดуดпкดเ!@р2กเด2ดกк2рк2ดкй252пดп@@прเ!у!пกด2!к2кดкดกดйук!ดпр5куп@йку@'

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

  it('R8UC1: TC1.2 Create new to-do with alternate chars', () => {
    // Create task with title and youtube-affiliation
    cy.get('#title')
      .type('TC1.2 Create new to-do with alternate chars')
    cy.get('#url')
      .type('j_uu6bJ2IGI')
    cy.contains('input[type="submit"]', 'Create new Task')
      .click()

    // Navigate to created task
    cy.contains('.title-overlay', 'TC1.2 Create new to-do with alternate chars')
      .click()

    cy.get('.popup .todo-list', { timeout: 20000 })
      .should('be.visible')

    // Get created task, add to-do and verify visibility
    cy.get('.popup input[placeholder="Add a new todo item"]')
      .scrollIntoView()
      .type(alternate_char)
    cy.get('.popup input[value="Add"]')
      .scrollIntoView()
      .click()
    cy.contains('.todo-item', alternate_char)
      .should('be.visible')
  })

  it('R8UC1: TC1.3 Create new to-do with no input', () => {
    // Create task with title and youtube-affiliation
    cy.get('#title')
      .type('TC1.3 Create new to-do with no input')
    cy.get('#url')
      .type('j_uu6bJ2IGI')
    cy.contains('input[type="submit"]', 'Create new Task')
      .click()

    // Navigate to created task
    cy.contains('.title-overlay', 'TC1.3 Create new to-do with no input')
      .click()

    cy.get('.popup .todo-list', { timeout: 20000 })
      .should('be.visible')

    // Get created task, add to-do and verify visibility
    cy.get('.popup input[placeholder="Add a new todo item"]')
      .scrollIntoView()
      .clear()
    cy.get('.popup input[value="Add"]')
      .scrollIntoView()
      .click()
    cy.get('.popup .todo-item').should('have.length', 1)
    cy.contains('.todo-item', 'Watch video').should('be.visible')
      .should('be.visible')
  })

  it('R8UC1: TC1.4 Create new to-do with max char breach (100+)', () => {
    // Create task with title and youtube-affiliation
    cy.get('#title')
      .type('TC1.4 Create new to-do with max char breach (100+)')
    cy.get('#url')
      .type('j_uu6bJ2IGI')
    cy.contains('input[type="submit"]', 'Create new Task')
      .click()

    // Navigate to created task
    cy.contains('.title-overlay', 'TC1.4 Create new to-do with max char breach (100+)')
      .click()

    cy.get('.popup .todo-list', { timeout: 20000 })
      .should('be.visible')

    // Get created task, add to-do and verify visibility
    cy.get('.popup input[placeholder="Add a new todo item"]')
      .scrollIntoView()
      .type(char_limit_breach)
    cy.get('.popup input[value="Add"]')
      .scrollIntoView()
      .click()
    cy.contains('.todo-item', char_limit_breach)
      .should('not.exist')
  })

  it('R8UC1: TC1.5 Create new to-do with max char (100)', () => {
    // Create task with title and youtube-affiliation
    cy.get('#title')
      .type('TC1.5 Create new to-do with max char (100)')
    cy.get('#url')
      .type('j_uu6bJ2IGI')
    cy.contains('input[type="submit"]', 'Create new Task')
      .click()

    // Navigate to created task
    cy.contains('.title-overlay', 'TC1.5 Create new to-do with max char (100)')
      .click()

    cy.get('.popup .todo-list', { timeout: 20000 })
      .should('be.visible')

    // Get created task, add to-do and verify visibility
    cy.get('.popup input[placeholder="Add a new todo item"]')
      .scrollIntoView()
      .type(char_limit)
    cy.get('.popup input[value="Add"]')
      .scrollIntoView()
      .click()
    cy.contains('.todo-item', char_limit)
      .should('be.visible')
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
