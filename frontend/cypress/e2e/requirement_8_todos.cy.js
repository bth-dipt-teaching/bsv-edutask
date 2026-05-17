describe('Requirement R8: manipulate todo items of a task', () => {
  const backendUrl = Cypress.env('backendUrl') || 'http://localhost:5000'
  const videoKey = 'dQw4w9WgXcQ'

  let userId
  let user
  let taskTitle
  let initialTodo

  function createUserAndTask() {
    userId = undefined
    const unique = `${Date.now()}-${Cypress._.random(1000000)}`

    user = {
      email: `r8.gui.${unique}@example.com`,
      firstName: 'R8',
      lastName: 'Tester'
    }
    taskTitle = `R8 task ${unique}`
    initialTodo = `Initial todo ${unique}`

    cy.request({
      method: 'POST',
      url: `${backendUrl}/users/create`,
      form: true,
      body: user
    }).then((response) => {
      userId = response.body._id.$oid

      cy.request({
        method: 'POST',
        url: `${backendUrl}/tasks/create`,
        form: true,
        body: {
          userid: userId,
          title: taskTitle,
          description: 'Task created for Cypress R8 GUI testing',
          url: videoKey,
          todos: initialTodo
        }
      })
    })
  }

  function loginAndOpenTask() {
    cy.visit('/')

    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(user.email)

    cy.get('form').submit()

    cy.get('h1')
      .should('contain.text', `Your tasks, ${user.firstName} ${user.lastName}`)

    cy.contains('.container-element', taskTitle)
      .find('a')
      .click({ force: true })

    cy.get('.popup-inner').within(() => {
      cy.contains('h1', taskTitle).should('be.visible')
      cy.contains('li.todo-item', initialTodo).should('be.visible')
    })
  }

  beforeEach(() => {
    createUserAndTask()
    loginAndOpenTask()
  })

  afterEach(() => {
    if (userId) {
      cy.request({
        method: 'DELETE',
        url: `${backendUrl}/users/${userId}`,
        failOnStatusCode: false
      })
    }
  })

  it('R8UC1 keeps the Add button disabled while the todo description is empty', () => {
    cy.get('.popup-inner').within(() => {
      cy.get('.todo-list form.inline-form')
        .find('input[type=text]')
        .should('have.value', '')

      cy.get('.todo-list form.inline-form')
        .find('input[type=submit][value=Add]')
        .should('be.disabled')
    })
  })

  it('R8UC1 creates a new todo item for the opened task', () => {
    const newTodo = `New GUI todo ${Date.now()}`

    cy.get('.popup-inner').within(() => {
      cy.contains('li.todo-item', newTodo).should('not.exist')

      cy.get('.todo-list form.inline-form')
        .find('input[type=text]')
        .type(newTodo)

      cy.get('.todo-list form.inline-form')
        .find('input[type=submit][value=Add]')
        .click()

      cy.contains('li.todo-item', newTodo).should('be.visible')
    })
  })

  it('R8UC2 toggles a todo item between active and done', () => {
    cy.get('.popup-inner').within(() => {
      cy.contains('li.todo-item', initialTodo)
        .find('.checker')
        .should('have.class', 'unchecked')
        .click()

      cy.contains('li.todo-item', initialTodo)
        .find('.checker')
        .should('have.class', 'checked')

      cy.contains('li.todo-item', initialTodo)
        .find('.editable')
        .should('have.css', 'text-decoration-line', 'line-through')

      cy.contains('li.todo-item', initialTodo)
        .find('.checker')
        .click()

      cy.contains('li.todo-item', initialTodo)
        .find('.checker')
        .should('have.class', 'unchecked')

      cy.contains('li.todo-item', initialTodo)
        .find('.editable')
        .should('have.css', 'text-decoration-line', 'none')
    })
  })

  it('R8UC3 deletes an existing todo item from the opened task', () => {
    cy.get('.popup-inner').within(() => {
      cy.contains('li.todo-item', initialTodo)
        .find('.remover')
        .click()

      cy.contains('li.todo-item', initialTodo).should('not.exist')
    })
  })
})
