describe('Todo tests', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user
    let taskId // task id

    const taskTitle = 'Test todo'
    const youtubeURL = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

    beforeEach(() => {

  cy.intercept('POST', '**/tasks/create').as('createTask')
  cy.intercept('GET', '**/tasks/byid/*').as('tasksById')

  cy.fixture('user.json').then((user) => {

    cy.request({
      method: 'POST',
      url: 'http://localhost:5000/users/create',
      form: true,
      body: user
    }).then((response) => {

      uid = response.body._id.$oid
      email = user.email

      cy.visit('http://localhost:3000')

      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type(email)

      cy.get('form').submit()

      return cy.fixture('task.json')
    })
    .then((task) => {

      return cy.request({
        method: 'POST',
        url: 'http://localhost:5000/tasks/create',
        form: true,
        body: {
          ...task,
          userid: uid
        }
      })
    })
    .then((response) => {

      taskId = response.body._id

      cy.visit('http://localhost:3000')

      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type(email)

      cy.get('form').submit()

      cy.get('.title-overlay').first().click()
    })
  })
})
    it('Test add valid todo item', () => {
        const todoName = 'watch vid at 2x speed'

        cy.get('.inline-form > [type="text"]')
            .type(todoName)

        cy.get('.inline-form > [type="submit"]')
            .click()

        cy.get('.todo-list .todo-item')
            .last()
            .should('contain.text', todoName)
    })

    it('Test empty description', () => {
        cy.get('.inline-form > [type="submit"]')
            .should('be.disabled')
    })

// it('toggles todo correctly', () => {

//   // ALWAYS re-query fresh DOM
//   cy.get('.todo-item').first().as('item')

//   cy.get('@item')
//     .find('.checker')
//     .click()

//   cy.get('@item')
//     .should('have.class', 'checked')

//   // re-query AGAIN (viktigt!)
//   cy.get('.todo-item').first()
//     .find('.checker')
//     .click()

//   cy.get('.todo-item').first()
//     .should('not.have.class', 'checked')
// })

    
    it('Test toggle on and off strikethrough todo item name', () => {
        
        cy.get('.todo-item')
            .first()
            .find('.checker')
            .click()
        
        cy.get('.todo-item')
        .first()
        .find('.editable')
        .should('have.css', 'text-decoration-line', 'line-through')

        cy.get('.todo-item')
            .first()
            .find('.checker')
            .click()
        
        cy.get('.todo-item')
        .first()
        .find('.editable')
        .should('not.have.css', 'text-decoration-line', 'line-through')
    })

    // it('Test untoggle strikethrough todo item name', () => {

    //     cy.get('.todo-item')
    //         .first()
    //         .find('.checker')
    //         .click()
        
    //     cy.get('.todo-item')
    //     .first()
    //     .find('.editable')
    //     .should('not.have.css', 'text-decoration-line', 'line-through')
    // })

    it('Test delete todo item', () => {

    cy.contains('.todo-item', 'Watch the video')
        .find('.remover')
        .click()

    cy.wait('@tasksById')

    cy.get('.todo-list > li.todo-item')
        .should('have.length', 0)
})

    afterEach(function () {

    // delete task
    if (taskId) {
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/tasks/${taskId}`,
            failOnStatusCode: false
        }).then((response) => {
            cy.log(response.body)
        })
    }

    // delete user
    if (uid) {
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`,
            failOnStatusCode: false
        }).then((response) => {
            cy.log(response.body)
        })
    }
})
})