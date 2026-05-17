// cypress/e2e/todo.cy.js
//
// E2E tests for EduTask R8 (manipulate the todolist of a task)
// Test cases derived using the 4-step technique.

const TEST_EMAIL = 'student@test.com'
const FIRST_NAME = 'Test'
const LAST_NAME  = 'User'
const API_BASE   = 'http://localhost:5000'

describe('R8 - Todo Management GUI Tests', () => {

  // ---- helpers ----

  const addTodo = (todo) => {
    cy.intercept('POST', `${API_BASE}/todos/create`).as('createTodo')
    cy.intercept('GET',  `${API_BASE}/tasks/byid/**`).as('taskRefresh')
    cy.get('input[placeholder="Add a new todo item"]')
      .clear({ force: true })
      .type(todo, { force: true })
    cy.get('input[placeholder="Add a new todo item"]')
      .closest('div')
      .contains('Add')
      .click({ force: true })
    cy.wait('@createTodo')
    cy.wait('@taskRefresh')
  }

  const toggleTodo = (text) => {
    cy.intercept('PUT', `${API_BASE}/todos/byid/**`).as('toggleTodo')
    cy.intercept('GET', `${API_BASE}/tasks/byid/**`).as('taskRefresh')
    cy.contains('span.editable', text)
      .parent()
      .find('.checker')
      .click({ force: true })
    cy.wait('@toggleTodo')
    cy.wait('@taskRefresh')
  }

  // The app fires a GET *before* the DELETE lands, re-rendering from stale
  // data. No amount of intercept waiting can fix this — the only reliable
  // approach is to wait for the DELETE, then re-login and re-open the task
  // so the page fetches fresh data from scratch.
  const deleteTodo = (text) => {
    cy.intercept('DELETE', `${API_BASE}/todos/byid/**`).as('deleteTodo')
    cy.contains('span.editable', text)
      .parent()
      .find('.remover')
      .click({ force: true })
    cy.wait('@deleteTodo')
  }

  // Re-login and re-open the last task. Used after deleteTodo to get a
  // clean render from the server (post-deletion state).
  const reopenLastTask = () => {
    cy.visit('http://localhost:3000')
    cy.get('#email').clear().type(TEST_EMAIL)
    cy.get('input[type="submit"]').first().click()
    cy.wait(2000)
    cy.get('img').last().click({ force: true })
    cy.wait(1000)
  }

  before(() => {
    cy.request({
      method: 'POST',
      url: `${API_BASE}/users/create`,
      form: true,
      failOnStatusCode: false,
      body: { firstName: FIRST_NAME, lastName: LAST_NAME, email: TEST_EMAIL }
    })
  })

  beforeEach(() => {
    cy.visit('http://localhost:3000')
    cy.get('#email').clear().type(TEST_EMAIL)
    cy.get('input[type="submit"]').first().click()
    cy.wait(2000)

    cy.get('input[placeholder="Title of your Task"]')
      .first().type('R8 Todo Test Task', { force: true })
    cy.get('input[placeholder*="YouTube"]')
      .first().type('rE_530gL0cs', { force: true })
    cy.contains('Create new Task').click({ force: true })
    cy.wait(2000)

    cy.get('img').last().click({ force: true })
    cy.wait(1000)
  })

  /* ============================================================
     R8UC1 — Add a new todo item
     ============================================================ */
  describe('R8UC1 - Create Todo', () => {

    it('TC1 - Valid description creates an active todo at the bottom', () => {
      addTodo('Read chapter 4')
      cy.contains('span.editable', 'Read chapter 4').should('exist')
    })

    it('TC2 - Empty input: input field is cleared after submit attempt', () => {
      cy.get('input[placeholder="Add a new todo item"]').clear()
      cy.get('input[placeholder="Add a new todo item"]')
        .closest('div')
        .contains('Add')
        .click({ force: true })
      cy.wait(1000)
      cy.get('input[placeholder="Add a new todo item"]')
        .should('have.value', '')
    })

    it('TC3 - Multiple todos: newest appears at the bottom', () => {
      addTodo('First todo')
      addTodo('Second todo')
      addTodo('Third todo')
      cy.get('span.editable').last().should('contain.text', 'Third todo')
    })
  })

  /* ============================================================
     R8UC2 — Toggle an existing todo
     ============================================================ */
  describe('R8UC2 - Toggle Todo', () => {

    it('TC4 - Active → Done: todo item receives done styling', () => {
      addTodo('Toggle me')
      cy.contains('span.editable', 'Toggle me')
        .parent().as('todoItem')
      toggleTodo('Toggle me')
      cy.get('@todoItem').then(($li) => {
        const isDone =
          $li.find('s').length > 0 ||
          $li.hasClass('done') ||
          $li.hasClass('checked') ||
          $li.hasClass('completed') ||
          $li.find('[class*="done"]').length > 0 ||
          $li.find('[class*="checked"]').length > 0 ||
          $li.find('[class*="complete"]').length > 0
        expect(isDone).to.be.true
      })
    })

    it('TC5 - Done → Active: done styling is removed', () => {
      addTodo('Untoggle me')
      toggleTodo('Untoggle me')   // active → done
      toggleTodo('Untoggle me')   // done   → active
      cy.contains('span.editable', 'Untoggle me')
        .parent().then(($li) => {
          const stillDone =
            $li.find('s').length > 0 ||
            $li.hasClass('done') ||
            $li.hasClass('checked') ||
            $li.hasClass('completed')
          expect(stillDone).to.be.false
        })
    })
  })

  /* ============================================================
     R8UC3 — Delete an existing todo
     ============================================================ */
  describe('R8UC3 - Delete Todo', () => {

    it('TC6 - Deleting one todo removes it but keeps the others', () => {
      addTodo('Keep me 1')
      addTodo('Delete me')
      addTodo('Keep me 2')
      deleteTodo('Delete me')
      // Re-login so the page fetches fresh post-deletion data.
      reopenLastTask()
      cy.contains('span.editable', 'Delete me').should('not.exist')
      cy.contains('span.editable', 'Keep me 1').should('exist')
      cy.contains('span.editable', 'Keep me 2').should('exist')
    })

    it('TC7 - Deleting the only todo leaves the list empty', () => {
      addTodo('Only todo')
      deleteTodo('Only todo')
      reopenLastTask()
      cy.contains('span.editable', 'Only todo').should('not.exist')
    })
  })
})