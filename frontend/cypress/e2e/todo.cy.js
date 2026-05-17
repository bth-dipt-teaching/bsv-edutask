describe('R8 - Todo item management on a task', () => {
  let uid
  let user
  let task

  beforeEach(function () {
    const unique = Date.now()

    cy.fixture('user.json')
      .then((fixtureUser) => {
        user = {
          ...fixtureUser,
          email: `cypress.${unique}@example.com`
        }

        return cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        })
      })
      .then((response) => {
        uid = response.body._id.$oid
        return cy.fixture('task.json')
      })
      .then((fixtureTask) => {
        task = {
          ...fixtureTask,
          title: `${fixtureTask.title} ${unique}`
        }

        return cy.request({
          method: 'POST',
          url: 'http://localhost:5000/tasks/create',
          form: true,
          body: {
            title: task.title,
            description: task.description,
            url: task.url,
            userid: uid,
            todos: task.todos
          }
        })
      })
      .then(() => {
        cy.visit('/')

        cy.contains('div', 'Email Address')
          .find('input[type=text]')
          .type(user.email)

        cy.get('form').submit()
        cy.get('h1').should('contain.text', `Your tasks, ${user.firstName} ${user.lastName}`)

        cy.contains('.title-overlay', task.title).click()
        cy.get('.todo-list').should('be.visible')
        cy.contains('li.todo-item', 'Watch video').should('be.visible')
      })
  })

  afterEach(function () {
    if (uid) {
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${uid}`,
        failOnStatusCode: false
      })
    }
  })

  it('TC-R8UC1-ALT: keeps empty todo submissions unavailable', () => {
    cy.get('input[placeholder="Add a new todo item"]').should('have.value', '')
    cy.get('input[type="submit"][value="Add"]').should('be.disabled')
  })

  it('TC-R8UC1-MAIN: adds a todo with user-entered text', () => {
    const newTodo = 'Read the lecture slides'

    cy.intercept('POST', '**/todos/create').as('createTodo')

    cy.get('input[placeholder="Add a new todo item"]').type(newTodo)
    cy.get('input[type="submit"][value="Add"]').click()

    cy.wait('@createTodo')
    cy.contains('li.todo-item', newTodo).should('be.visible')
  })

  it('TC-R8UC2-MAIN: switches a todo to done and back again', () => {
    cy.intercept('PUT', '**/todos/byid/*').as('toggleTodo')

    cy.contains('li.todo-item', 'Watch video')
      .find('span.checker')
      .should('have.class', 'unchecked')
      .click()

    cy.wait('@toggleTodo')

    cy.contains('li.todo-item', 'Watch video')
      .find('span.checker')
      .should('have.class', 'checked')

    cy.contains('li.todo-item', 'Watch video')
      .find('span.checker')
      .click()

    cy.wait('@toggleTodo')

    cy.contains('li.todo-item', 'Watch video')
      .find('span.checker')
      .should('have.class', 'unchecked')
  })

  it('TC-R8UC3-MAIN: removes an existing todo from the visible list', () => {
    cy.intercept('DELETE', '**/todos/byid/*').as('deleteTodo')

    cy.contains('li.todo-item', 'Watch video')
      .find('span.remover')
      .click()

    cy.wait('@deleteTodo')
    cy.contains('li.todo-item', 'Watch video').should('not.exist')
  })
})
