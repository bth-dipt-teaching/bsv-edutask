describe('R8 - Todo list manipulation', () => {
  // define variables that we need on multiple occasions
  let uid   // user id
  let name  // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  beforeEach(function () {
    // create a fabricated user from a fixture, log in, create a task, and open its detail view
    cy.fixture('user.json').then((user) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
      }).then((response) => {
        uid   = response.body._id.$oid
        name  = user.firstName + ' ' + user.lastName
        email = user.email

        // visit the app and log in with the registered email address
        cy.visit('http://localhost:3000')
        cy.contains('div', 'Email Address')
          .find('input[type=text]')
          .type(email)
        cy.get('form').submit()

        // wait until the task overview is visible
        cy.get('h1').should('contain.text', 'Your tasks, ' + name)

        // fill in the task creation form using the exact field ids
        cy.get('.submit-form').find('#title').type('Test task for Todos')
        cy.get('.submit-form').find('#url').type('KSX4cwWRzis')
        cy.get('[type="submit"]').click()

        // open the task detail popup by clicking the newly created task card
        cy.contains('Test task for Todos').click()
      })
    })
  })

  afterEach(function () {
    // clean up by deleting the user and all associated data from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
 
  //   EC2 (invalid input): empty description     → submit button stays disabled (alt 2.b)

  it('R8UC1-EC1: appends a new todo item to the list when description is non-empty', () => {
    // force: true is required because the input is hidden behind the popup scroll area
    cy.get('.inline-form > [type="text"]').type('Take notes!!!', { force: true })
    cy.get('.inline-form > [type="submit"]').click({ force: true })

    // assert the new item appears as the last entry in the todo list
    cy.get('.todo-item').last().should('contain.text', 'Take notes!!!')
  })

  it('R8UC1-EC2: keeps the submit button disabled when description is empty', () => {
    // no text typed — button must remain disabled (alternative scenario 2.b)
    // SYSTEM FAILURE DETECTED: the submit button is not disabled when input is empty,
    // which violates requirement R8UC1 alternative scenario 2.b
    cy.get('.inline-form > [type="submit"]').should('be.disabled')
  })

  // ── R8UC2: Toggling a todo item ───────────────────────────────────────────
  // Test design: equivalence partitioning
  //   EC1 (active → done): checker clicked once  → item is struck through
  //   EC2 (done → active): checker clicked twice → strikethrough is removed (alt 2.b)

  it('R8UC2-EC1: strikes through a todo item when toggled from active to done', () => {
    // .first() is required because .find('.checker') matches multiple elements in the list
    cy.contains('.todo-list', 'Watch video').find('.checker').first().click()

    // assert the item text is now struck through
    cy.contains('Watch video')
      .should('have.css', 'text-decoration-line', 'line-through')
  })

  it('R8UC2-EC2: removes the strikethrough when a done item is toggled back to active', () => {
    // first click: active → done
    cy.contains('.todo-list', 'Watch video').find('.checker').first().click()
    cy.contains('Watch video')
      .should('have.css', 'text-decoration-line', 'line-through')

    // second click: done → active (alternative scenario 2.b)
    cy.contains('.todo-list', 'Watch video').find('.checker').first().click()
    cy.contains('Watch video')
      .should('have.css', 'text-decoration-line', 'none')
  })

  // ── R8UC3: Deleting a todo item ───────────────────────────────────────────
  // Test design: equivalence partitioning
  //   EC1 (delete one item): x clicked → item is removed from the list

  it('R8UC3-EC1: removes the todo item from the list when x is clicked', () => {
    // .first() is required because .find('.remover') matches multiple elements in the list
    cy.contains('.todo-list', 'Watch video').find('.remover').first().click()

    // assert the item no longer exists in the list
    cy.get('.todo-list').should('not.contain', 'Watch video')
  })

})