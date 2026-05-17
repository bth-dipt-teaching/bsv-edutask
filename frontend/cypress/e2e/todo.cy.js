/**
 * Assignment 4 – GUI Testing
 * Requirement 8 use cases: create, toggle, and delete to-do items of a task.
 *
 * Test cases are derived using Equivalence Partitioning / Boundary-Value Analysis
 * on the three use cases:
 *
 *  R8UC1 – Create a to-do item
 *    TC1: Create a to-do with a non-empty description  → item appears in list
 *    TC2: Attempt to submit an empty description        → item is NOT added
 *
 *  R8UC2 – Toggle the done-state of a to-do item
 *    TC3: Click checker on an undone item  → item becomes checked
 *    TC4: Click checker on a done item     → item becomes unchecked (toggle back)
 *
 *  R8UC3 – Delete a to-do item
 *    TC5: Click the remove button on an existing item → item is removed from the list
 */

describe('R8 – To-do management', () => {
  let uid
  let email
  let taskId

  // ─── Setup ─────────────────────────────────────────────────────────────────

  before(() => {
    cy.fixture('user.json').then((user) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user,
      }).then((response) => {
        uid = response.body._id.$oid
        email = user.email
      })
    })
  })

  beforeEach(() => {
    // Create a fresh task via the API before each test.
    //
    // Two backend constraints to work around:
    //
    // 1. The blueprint uses request.form.to_dict(flat=False). The controller
    //    does `for todo in data['todos']`, so 'todos' MUST be present.
    //    Cypress's form:true uses the qs library, which encodes a JS array as
    //    todos[0]=val&todos[1]=val — keys the backend never finds → KeyError → 500.
    //    Fix: send task.todos[0] as a plain string. parse_qs then produces
    //    { todos: ['Watch video'] }, a list the controller can iterate.
    //
    // 2. The endpoint returns ALL tasks for the user, not just the new one.
    //    We find ours by title to extract the _id.
    cy.fixture('task.json').then((task) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/tasks/create',
        form: true,
        body: {
          title: task.title,
          description: task.description,
          userid: uid,
          url: task.url,
          todos: task.todos[0],   // send as string, not array (see note above)
        },
      }).then((resp) => {
        // resp.body is the list of all tasks for this user; find ours by title
        const created = resp.body.find((t) => t.title === task.title)
        taskId = created._id.$oid

        cy.visit('http://localhost:3000')
        cy.contains('div', 'Email Address')
          .find('input[type=text]')
          .type(email)
        cy.get('form').submit()

        cy.contains(task.title).click()
      })
    })
  })

  afterEach(() => {
    if (taskId) {
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/tasks/byid/${taskId}`,
        failOnStatusCode: false,
      })
    }
  })

  after(() => {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`,
    })
  })
// ─── R8UC1 – Create a to-do item ───────────────────────────────────────────

  describe('R8UC1 – Create a to-do item', () => {
    it('TC1: creates a to-do item with a valid description', () => {
      const description = 'Watch the introduction video'

      cy.get('input[placeholder="Add a new todo item"]').type(description)
      cy.contains('input[type=submit]', 'Add').click()

      cy.get('.todo-list').should('contain.text', description)
    })

    it('TC2: does not add a to-do item when description is empty', () => {
      cy.get('input[placeholder="Add a new todo item"]').clear()

      cy.get('.todo-list li').then((listBefore) => {
        const countBefore = listBefore.length
        cy.get('.inline-form').submit()
        cy.get('.todo-list li').should('have.length', countBefore)
      })
    })
  })

  // ─── R8UC2 – Toggle the done-state of a to-do item ─────────────────────────

  describe('R8UC2 – Toggle the done-state of a to-do item', () => {
    beforeEach(() => {
      cy.get('input[placeholder="Add a new todo item"]').type('Toggle me')
      cy.contains('input[type=submit]', 'Add').click()
      cy.get('.todo-list').should('contain.text', 'Toggle me')
    })

    it('TC3: marks an undone item as done when its checker is clicked', () => {
      cy.contains('.todo-item', 'Toggle me')
        .find('.checker')
        .should('have.class', 'unchecked')
        .click()

      cy.contains('.todo-item', 'Toggle me')
        .find('.checker')
        .should('have.class', 'checked')
    })

    it('TC4: unmarks a done item when its checker is clicked again', () => {
      cy.contains('.todo-item', 'Toggle me').find('.checker').click()
      cy.contains('.todo-item', 'Toggle me')
        .find('.checker')
        .should('have.class', 'checked')

      cy.contains('.todo-item', 'Toggle me').find('.checker').click()
      cy.contains('.todo-item', 'Toggle me')
        .find('.checker')
        .should('have.class', 'unchecked')
    })
  })

  // ─── R8UC3 – Delete a to-do item ───────────────────────────────────────────

  describe('R8UC3 – Delete a to-do item', () => {
    it('TC5: removes a to-do item when the remove button is clicked', () => {
      const description = 'Item to be deleted'

      cy.get('input[placeholder="Add a new todo item"]').type(description)
      cy.contains('input[type=submit]', 'Add').click()
      cy.get('.todo-list').should('contain.text', description)

      cy.contains('.todo-item', description).find('.remover').click()

      cy.get('.todo-list').should('not.contain.text', description)
    })
  })
})
