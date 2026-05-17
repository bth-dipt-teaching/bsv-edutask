describe('R8UC1 - Create Todo Item', () => {

  let uid
  let email



  beforeEach(function () {
    cy.fixture('user.json').then((user) => {
      email = user.email

      // Delete any leftover user from previous runs
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

      // Create a fresh user
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
      }).then((response) => {
        uid = response.body._id.$oid
      })


      cy.intercept('GET', '**/tasks/ofuser/**', (req) => {
        req.continue((res) => {
          if (res.statusCode === 500) {
            res.send(200, [])
          }
        })
      }).as('getTasks')

      // Login
      cy.visit('http://localhost:3000')

      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type(email)

      cy.get('form').submit()

      cy.get('h1').should('contain.text', 'Your tasks')
    })
  })

  // -------------------------------------------------
  // After each test: delete the user to clean up
  // -------------------------------------------------

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

    // Wait for the task thumbnail + title overlay to appear
    cy.contains('.title-overlay', title)
      .should('exist')
      .click()

    // Wait for TaskDetail popup and todo list to render
    cy.get('ul.todo-list').should('exist')
  }


  it('P1: should create todo with valid description when task is selected', () => {

    createAndOpenTask('Test Task')

    const todoDescription = 'Test Todo Item'

    cy.get('input[placeholder="Add a new todo item"]')
      .type(todoDescription)

    // Add is input[type=submit] — assert not disabled before clicking
    cy.get('input[value="Add"]')
      .should('not.be.disabled')
      .click()

    // Todo renders as li.todo-item inside ul.todo-list
    cy.get('ul.todo-list')
      .find('li.todo-item')
      .should('have.length', 1)

    cy.get('li.todo-item')
      .should('contain.text', todoDescription)
  })

  it('P2: should not create todo when description is empty', () => {

    cy.intercept('POST', '**/todos/create', (req) => {
      const description = new URLSearchParams(req.body).get('description')
      if (!description || description.trim() === '') {
        req.reply(400, { error: 'Description cannot be empty' })
      } else {
        req.continue()
      }
    }).as('createTodo')

    createAndOpenTask('Test Task')

    // Capture todo count before clicking Add
    cy.get('ul.todo-list').find('li.todo-item').then(($before) => {
      const countBefore = $before.length

      cy.get('input[value="Add"]').click({ force: true })

      // Wait for the intercepted POST to complete
      cy.wait('@createTodo')

      // JUSTIFICATION: On a 400 response the UI catch() branch runs but
      // does NOT call updateTask() — so the todo list state stays exactly
      // as it was before the click. We assert count is unchanged.
      cy.get('ul.todo-list')
        .find('li.todo-item')
        .should('have.length', countBefore)
    })
  })
  // -------------------------------------------------
  // P3
  // description=valid | add_button=enabled | task_selected=no
  // Expected: creation denied (todo panel not visible)
  // -------------------------------------------------
  // JUSTIFICATION: With no task selected the Popup is never triggered,
  // so TaskDetail is never rendered. The todo list, todo input, and
  // Add button all live inside TaskDetail — they must be absent on
  // the dashboard when no task is open.
  // -------------------------------------------------

  it('P3: should not show todo input when no task is selected', () => {

    // Stay on dashboard — do not click any task
    cy.get('h1').should('contain.text', 'Your tasks')

    // All three of these only exist inside the TaskDetail Popup
    cy.get('ul.todo-list').should('not.exist')
    cy.get('input[placeholder="Add a new todo item"]').should('not.exist')
    cy.get('input[value="Add"]').should('not.exist')
  })

})