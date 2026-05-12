describe('Manipulating todos of the system', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5001/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email
          
          // create a fabricated task from a fixture
          cy.fixture('task.json').then((task) => {
            cy.request({
              method: 'POST',
              url: 'http://localhost:5001/tasks/create',
              form: true,
              body: { ...task, userid: uid }
            })
          })
        })
      })
  })

  beforeEach(function () {
      // enter the main page
      cy.visit('http://localhost:3001')

      // login
      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type(email)
      cy.get('form')
        .submit()

      // click detailed view
      cy.get('.container-element a')
        .first()
        .click()
  })

  it('R8UC1: Add a todo to the task', () => {
    // detect the input field for the todo description and type in a description
    cy.get('input[placeholder="Add a new todo item"]')
      .type('New todo')
      .closest('form')
      .submit()

    // check that the new todo is in the list of todos and that it is the last entry in the list
    cy.get('ul.todo-list')
      .find('li.todo-item')
      .last()
      .should('contain.text', 'New todo')
  })

  // check that the "Add" button is disabled when the input field is empty
  it('R8UC1: Add todo disabled', () => {
    cy.get('input[type="submit"][value="Add"]')
      .should('be.disabled')
  })

  // check that the todo item can be set to done
  it('R8UC2: Toggle todo status', () => {
    cy.get('ul.todo-list')
      .find('li.todo-item')
      .first()
      .find('span.checker')
      .click()
      .should('have.class', 'checked')
  })

  // check that the todo item can be toggled back to active
  it('R8UC2: Untoggle todo status', () => {
    cy.get('ul.todo-list')
      .find('li.todo-item')
      .first()
      .find('span.checker')
      .click()
      .should('have.class', 'unchecked')
  })

  // check that todo item can be deleted
  it('R8UC3: Delete a todo item', () => {
    cy.get('ul.todo-list li.todo-item').last().find('span.remover').click()

    // assert that the deleted todo item is no longer in the list of todos
    cy.get('ul.todo-list li.todo-item .editable').each((element) => {
      expect(element.text()).to.not.equal('New todo')
    })
  })

  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5001/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})