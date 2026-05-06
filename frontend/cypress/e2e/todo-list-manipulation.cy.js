describe('R8 - Manipulate todo list of a task', () => {
  const backendUrl = 'http://localhost:5000'

  let uid
  let user
  let taskTitle
  let initialTodo

  beforeEach(() => {
    uid = null

    const unique = Date.now()

    cy.fixture('user.json')
      .then((dummyUser) => {
        user = {
          ...dummyUser,
          email: `sabr-r8-test-${unique}@gmail.com`
        }

        return cy.request({
          method: 'POST',
          url: `${backendUrl}/users/create`,
          form: true,
          body: user
        })
      })
      .then((response) => {
        uid = response.body._id.$oid

        return cy.fixture('task.json')
      })
      .then((dummyTask) => {
        taskTitle = `${dummyTask.title} ${unique}`
        initialTodo = dummyTask.todos

        return cy.request({
          method: 'POST',
          url: `${backendUrl}/tasks/create`,
          form: true,
          body: {
            ...dummyTask,
            title: taskTitle,
            userid: uid
          }
        })
      })
      .then(() => {
        // visit frontend and log in through the GUI
        cy.visit('/')

        cy.contains('div', 'Email Address')
          .find('input[type=text]')
          .type(user.email)

        cy.get('form')
          .submit()

        cy.get('h1')
          .should('contain.text', `Your tasks, ${user.firstName} ${user.lastName}`)

        // open the created task in detail view / popup
        cy.get('.container .container-element')
          .first()
          .should('contain.text', taskTitle)
          .find('a')
          .click()

        cy.get('.popup')
          .should('be.visible')

        cy.get('.todo-list')
          .should('be.visible')

        cy.contains('.todo-item', initialTodo)
          .should('be.visible')
      })
  })

  afterEach(() => {
    // clean up, deleting the user also deletes the user's tasks and todos
    if (uid) {
      cy.request({
        method: 'DELETE',
        url: `${backendUrl}/users/${uid}`,
        failOnStatusCode: false
      })
    }
  })

  it('R8UC1 - creates a new active todo item and appends it to the bottom of the list', () => {
    const newTodo = 'Read the documentation'

    cy.get('.todo-list .todo-item')
      .its('length')
      .then((oldTodoCount) => {
        cy.get('input[placeholder="Add a new todo item"]')
          .type(newTodo)

        cy.get('.inline-form input[type="submit"][value="Add"]')
          .click()

        cy.get('.todo-list .todo-item')
          .should('have.length', oldTodoCount + 1)

        cy.get('.todo-list .todo-item')
          .last()
          .within(() => {
            cy.get('.editable')
              .should('have.text', newTodo)

            cy.get('.checker')
              .should('have.class', 'unchecked')
          })
      })
  })

  it('R8UC1 alternative - keeps the Add button disabled when the todo description is empty', () => {
    cy.get('input[placeholder="Add a new todo item"]')
      .should('have.value', '')

    cy.get('.inline-form input[type="submit"][value="Add"]')
      .should('be.disabled')
  })

  it('R8UC2 - toggles an active todo item to done and strikes it through', () => {
    cy.contains('.todo-item', initialTodo)
      .find('.checker')
      .should('have.class', 'unchecked')
      .click()

    cy.contains('.todo-item', initialTodo)
      .find('.checker')
      .should('have.class', 'checked')

    cy.contains('.todo-item', initialTodo)
      .find('.editable')
      .should('have.css', 'text-decoration-line', 'line-through')
  })

  it('R8UC2 alternative - toggles a done todo item back to active', () => {
    cy.contains('.todo-item', initialTodo)
      .find('.checker')
      .click()

    cy.contains('.todo-item', initialTodo)
      .find('.checker')
      .should('have.class', 'checked')

    cy.contains('.todo-item', initialTodo)
      .find('.checker')
      .click()

    cy.contains('.todo-item', initialTodo)
      .find('.checker')
      .should('have.class', 'unchecked')

    cy.contains('.todo-item', initialTodo)
      .find('.editable')
      .should('not.have.css', 'text-decoration-line', 'line-through')
  })

  it('R8UC3 - deletes an existing todo item from the todo list', () => {
    cy.intercept('DELETE', `${backendUrl}/todos/byid/*`).as('deleteTodo')

    cy.contains('.todo-item', initialTodo)
      .find('.remover')
      .click()

    cy.wait('@deleteTodo')
      .its('response.statusCode')
      .should('eq', 200)

    cy.contains('.todo-item', initialTodo)
      .should('not.exist')
  })
})