const BACKEND = 'http://localhost:5000'
const FRONTEND = 'http://localhost:3000'

describe('R8: Todo Item Management', () => {

  beforeEach(() => {
    cy.fixture('user.json').then((user) => {
      cy.request({
        method: 'POST',
        url: `${BACKEND}/users/create`,
        form: true,
        body: {
          firstName: user.firstName,
          lastName: user.lastName,
          email: user.email
        },
        failOnStatusCode: false
      }).then((userResp) => {
        const userId = userResp.body._id.$oid

        cy.fixture('task.json').then((task) => {
          const body =
            `title=${encodeURIComponent(task.title)}` +
            `&description=${encodeURIComponent(task.description)}` +
            `&url=${encodeURIComponent(task.url)}` +
            `&userid=${encodeURIComponent(userId)}` +
            task.todos.map(t => `&todos=${encodeURIComponent(t)}`).join('')

          cy.request({
            method: 'POST',
            url: `${BACKEND}/tasks/create`,
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: body,
            failOnStatusCode: false
          }).then(() => {
            cy.visit(FRONTEND)
            cy.get('input#email').type(user.email)
            cy.get('input[type=submit]').click()
            cy.contains(task.title, { timeout: 8000 }).click()
            cy.get('ul.todo-list').should('exist')
          })
        })
      })
    })
  })

  afterEach(() => {
    cy.fixture('user.json').then((user) => {
      cy.request({
        method: 'GET',
        url: `${BACKEND}/users/bymail/${user.email}`,
        failOnStatusCode: false
      }).then((resp) => {
        if (resp.status === 200 && resp.body && resp.body._id) {
          cy.request('DELETE', `${BACKEND}/users/${resp.body._id.$oid}`)
        }
      })
    })
  })

  describe('R8UC1 - Create a to-do item', () => {

    it('TC1: creates a new to-do item when a non-empty description is submitted', () => {
      cy.get('input[placeholder="Add a new todo item"]').type('Buy groceries')
      cy.get('input[type=submit][value=Add]').click({ force: true })
      cy.get('ul.todo-list').contains('Buy groceries').should('exist')
    })

    it('TC2: does not create a to-do item when the description is empty', () => {
      cy.get('ul.todo-list li.todo-item').then(($before) => {
        const countBefore = $before.length
        cy.get('input[placeholder="Add a new todo item"]').clear()
        cy.get('input[type=submit][value=Add]').click({ force: true })
        cy.wait(1500)
        cy.get('ul.todo-list li.todo-item').should('have.length', countBefore)
      })
    })

  })

  describe('R8UC2 - Toggle a to-do item', () => {

    beforeEach(() => {
      cy.get('input[placeholder="Add a new todo item"]')
        .scrollIntoView()
        .type('Read a book', { force: true })
      cy.get('input[type=submit][value=Add]').click({ force: true })
      cy.get('ul.todo-list').contains('Read a book').should('exist')
    })

    it('TC3: marks an undone to-do item as done when its checker is clicked', () => {
      cy.contains('li.todo-item', 'Read a book')
        .find('span.checker')
        .should('have.class', 'unchecked')
        .click()
      cy.contains('li.todo-item', 'Read a book')
        .find('span.checker')
        .should('have.class', 'checked')
    })

    it('TC4: marks a done to-do item as undone when its checker is clicked again', () => {
      cy.contains('li.todo-item', 'Read a book')
        .find('span.checker').click()
      cy.contains('li.todo-item', 'Read a book')
        .find('span.checker').should('have.class', 'checked')

      cy.contains('li.todo-item', 'Read a book')
        .find('span.checker').click()
      cy.contains('li.todo-item', 'Read a book')
        .find('span.checker').should('have.class', 'unchecked')
    })

  })

  describe('R8UC3 - Delete a to-do item', () => {

    beforeEach(() => {
      cy.get('input[placeholder="Add a new todo item"]')
        .scrollIntoView()
        .type('Go for a run', { force: true })
      cy.get('input[type=submit][value=Add]').click({ force: true })
      cy.get('ul.todo-list').contains('Go for a run').should('exist')
    })

    it('TC5: removes the to-do item from the list when the remover is clicked', () => {
      cy.contains('li.todo-item', 'Go for a run')
        .find('span.remover')
        .click()
      cy.get('ul.todo-list', { timeout: 6000 })
        .contains('Go for a run')
        .should('not.exist')
    })

    it('TC6: other to-do items remain in the list after one is deleted', () => {
      cy.get('input[placeholder="Add a new todo item"]')
        .scrollIntoView()
        .type('Study for exam', { force: true })
      cy.get('input[type=submit][value=Add]').click({ force: true })
      cy.get('ul.todo-list').contains('Study for exam').should('exist')

      cy.contains('li.todo-item', 'Go for a run')
        .find('span.remover')
        .click()

      cy.get('ul.todo-list', { timeout: 6000 })
        .contains('Go for a run')
        .should('not.exist')
      cy.get('ul.todo-list').contains('Study for exam').should('exist')
    })

  })

})
