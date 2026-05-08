// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

Cypress.Commands.add('createUser', (fixture = 'user.json') => {
  cy.fixture(fixture).then((user) => {
    // create user
    cy.request({
      method: 'POST',
      url: 'http://localhost:5000/users/create',
      form: true,
      body: user
    }).then((response) => {

      return {
        ...user,
        id: response.body._id.$oid
      }
    })
  })
})

Cypress.Commands.add("deleteUser", (userId) => {
  cy.request({
    method: "DELETE",
    url: `http://localhost:5000/users/${userId}`
  })
})

Cypress.Commands.add('createTask', (userId, fixture= 'task.json') => {
  cy.fixture(fixture).then((task) => {
    const taskObject = {
      ...task,
      userid: userId
    }

    cy.request({
      method: 'POST',
      url: `http://localhost:5000/tasks/create`,
      form: true,
      body: taskObject
    }).then((response) => {

      const createdTask = response.body.find(
        t => t.title === taskObject.title
      )

      return {
        ...taskObject,
        id: createdTask._id.$oid,
        todoId: createdTask.todos[0]._id.$oid
      }
    })
  })
})

Cypress.Commands.add('deleteTask', (taskId) => {
  cy.request({
    method: 'DELETE',
    url: `http://localhost:5000/tasks/byid/${taskId}`
  })
})

Cypress.Commands.add('tryTask', (title, url, userid) => {
  const data = new URLSearchParams()

  data.append('title', title)
  data.append('description', '(add a description here)')
  data.append('userid', userid)
  data.append('url', url)

  data.append('todos', JSON.stringify(['Watch video']))

  cy.request({
    method: 'POST',
    url: 'http://localhost:5000/tasks/create',
    body: data.toString(),
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    failOnStatusCode: false
  })

})