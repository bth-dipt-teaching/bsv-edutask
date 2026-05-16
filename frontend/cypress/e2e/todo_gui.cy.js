/// <reference types="cypress" />
/* global cy */

describe('R8 Todo GUI tests', () => {
  let uid
  let name
  let email

  const taskTitle = 'Cypress Task'
  const videoKey = 'dQw4w9WgXcQ'
  const todoText = `Cypress Todo ${Date.now()}`

  beforeEach(function () {
      cy.fixture('user.json')
    .then((user) => {
      user.email = `mon.doe.${Date.now()}@gmail.com`

      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
      }).then((response) => {
        uid = response.body._id.$oid
        name = user.firstName + ' ' + user.lastName
        email = user.email
        cy.visit('http://localhost:3000')

        cy.contains('div', 'Email Address')
          .find('input[type=text]')
          .type(email)

        cy.get('form')
          .submit()

        cy.get('h1')
          .should('contain.text', 'Your tasks, ' + name)
      })
    })
  })

  function createAndOpenTask() {
    cy.get('input[name="title"]').type(taskTitle)
    cy.get('input[name="url"]').type(videoKey)
    cy.get('input[type="submit"][value="Create new Task"]').click()

    cy.contains(taskTitle).should('exist')
    cy.contains(taskTitle).click()

    cy.get('input[placeholder="Add a new todo item"]').should('exist')
  }

  it('R8UC1: user can create a todo item', () => {
    createAndOpenTask()

    cy.get('input[placeholder="Add a new todo item"]').type(todoText)
    cy.get('input[type="submit"][value="Add"]').click()

    cy.contains(todoText).should('exist')
  })

  it('R8UC2: user can toggle a todo item', () => {
  createAndOpenTask()

  cy.get('input[placeholder="Add a new todo item"]')
      .last()
      .type(todoText, { force: true })

  cy.get('input[type="submit"][value="Add"]')
      .last()
      .click({ force: true })

  cy.contains('li.todo-item', todoText)
      .find('.checker')
      .click({ force: true })

  cy.contains('li.todo-item', todoText)
      .find('.checker')
      .should('have.class', 'checked')
  })

it('R8UC3: user can delete a todo item', () => {
  createAndOpenTask()

  cy.get('input[placeholder="Add a new todo item"]')
    .last()
    .type(todoText, { force: true })

  cy.get('input[type="submit"][value="Add"]')
    .last()
    .click({ force: true })

  cy.contains('li.todo-item', todoText).should('exist')

  cy.wait(500)

  cy.contains('li.todo-item', todoText)
    .find('.remover')
    .click({ force: true })

  // cy.contains('li.todo-item', todoText)
  //   .find('.remover')
  //   .click({ force: true })

  cy.contains('li.todo-item', todoText, { timeout: 8000 })
    .should('not.exist')
})

  afterEach(function () {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    })
  })
})