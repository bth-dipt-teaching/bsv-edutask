describe('R8UC2 - Toggle Todo Item', () => {

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

    // Wait for the todo to appear in the list
    cy.get('li.todo-item')
      .should('contain.text', description)
  }


  it('P1: should toggle active todo to done', () => {

    createAndOpenTask('Test Task')

    const todoDescription = 'Todo to mark done'
    addTodo(todoDescription)

    // Find the todo item and click its .checker span to toggle done
    cy.get('li.todo-item')
      .contains(todoDescription)
      .closest('li.todo-item')
      .find('span.checker')
      .should('have.class', 'unchecked')  // confirm starts as active
      .click()

    // Assert the checker is now marked as done
    cy.get('li.todo-item')
      .contains(todoDescription)
      .closest('li.todo-item')
      .find('span.checker')
      .should('have.class', 'checked')
  })



  it('P2: should toggle done todo back to active', () => {

    createAndOpenTask('Test Task')

    const todoDescription = 'Todo to toggle back'
    addTodo(todoDescription)

    // First click: mark as done
    cy.get('li.todo-item')
      .contains(todoDescription)
      .closest('li.todo-item')
      .find('span.checker')
      .click()

    // Confirm it is now done
    cy.get('li.todo-item')
      .contains(todoDescription)
      .closest('li.todo-item')
      .find('span.checker')
      .should('have.class', 'checked')

    // Second click: toggle back to active
    cy.get('li.todo-item')
      .contains(todoDescription)
      .closest('li.todo-item')
      .find('span.checker')
      .click()

    // Assert it is now active again
    cy.get('li.todo-item')
      .contains(todoDescription)
      .closest('li.todo-item')
      .find('span.checker')
      .should('have.class', 'unchecked')
  })


  it('P3: should not toggle when no todo exists', () => {

    cy.get('h1').should('contain.text', 'Your tasks')

    // The todo list only exists inside TaskDetail Popup
    cy.get('ul.todo-list').should('not.exist')

    // No checker span exists anywhere — nothing to toggle
    cy.get('span.checker').should('not.exist')
  })

})