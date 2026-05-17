describe('R8UC3 - Delete Todo Item', () => {

  let uid
  let email


  beforeEach(function () {
    cy.fixture('user.json').then((user) => {
      email = user.email

      cy.request({
        method: 'GET',
        url: `http://localhost:5000/users/bymail/${email}`,
        failOnStatusCode: false
      }).then((res) => {
        if (res.status === 200 && res.body?._id) {
          cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${res.body._id.$oid}`,
            failOnStatusCode: false
          })
        }
      })

      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
      }).then((response) => {
        uid = response.body._id.$oid
      })

      // Intercept BEFORE visit to catch the first /tasks/ofuser fetch
      cy.intercept('GET', '**/tasks/ofuser/**', (req) => {
        req.continue((res) => {
          if (res.statusCode === 500) {
            res.send(200, [])
          }
        })
      }).as('getTasks')

      cy.visit('http://localhost:3000')

      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type(email)

      cy.get('form').submit()

      cy.get('h1').should('contain.text', 'Your tasks')
    })
  })

  afterEach(function () {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`,
      failOnStatusCode: false
    })
  })


  function createAndOpenTask(title) {
    cy.get('input[placeholder="Title of your Task"]')
      .type(title)

    cy.get('input[placeholder*="Viewkey"]')
      .type('dQw4w9WgXcQ')

    cy.get('input[value="Create new Task"]').click()

    cy.contains('.title-overlay', title)
      .should('exist')
      .click()

    cy.get('ul.todo-list').should('exist')
  }


  function addTodo(description) {
    cy.get('input[placeholder="Add a new todo item"]')
      .type(description)

    cy.get('input[value="Add"]')
      .should('not.be.disabled')
      .click()

    cy.get('li.todo-item')
      .should('contain.text', description)
  }

  it('P1: should delete an existing todo', () => {

    cy.intercept('GET', '**/tasks/byid/**').as('taskRefresh')

    createAndOpenTask('Test Task')

    // Wait for initial task load
    cy.wait('@taskRefresh')

    const todoDescription = 'Todo to Delete'

    cy.get('input[placeholder="Add a new todo item"]')
      .type(todoDescription)

    cy.get('input[value="Add"]').click()

    // Wait for re-fetch after adding todo
    cy.wait('@taskRefresh')

    // Confirm our todo is there
    cy.get('li.todo-item')
      .contains(todoDescription)
      .should('exist')

    // Record count AFTER our todo was added and UI settled
    cy.get('li.todo-item').then(($items) => {
      const countAfterAdd = $items.length

      // Click remover on our specific todo
      cy.get('li.todo-item')
        .contains(todoDescription)
        .closest('li.todo-item')
        .find('span.remover')
        .click()

      // Wait for re-fetch AFTER deletion specifically
      cy.wait('@taskRefresh')

      // Assert count decreased by exactly 1
      cy.get('ul.todo-list')
        .find('li.todo-item')
        .should('have.length', countAfterAdd - 1)

      // Assert our specific todo is gone
      cy.contains(todoDescription).should('not.exist')
    })
  })
 

  it('P2: should not attempt to delete when no todo exists', () => {

    // Stay on dashboard — do not open any task
    cy.get('h1').should('contain.text', 'Your tasks')

    // The todo list only renders inside the TaskDetail Popup
    cy.get('ul.todo-list').should('not.exist')

    // No remover span exists — deletion is impossible
    cy.get('span.remover').should('not.exist')
  })

})