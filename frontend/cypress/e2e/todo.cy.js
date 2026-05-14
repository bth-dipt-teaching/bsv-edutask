describe('Todo functionality', () => {

    let uid
    let tid
    let email

    before(function () {

        cy.fixture('user.json')
            .then((user) => {

                email = user.email

                cy.request({
                    method: 'POST',
                    url: 'http://localhost:5000/users/create',
                    form: true,
                    body: user
                }).then((response) => {

                    uid = response.body._id.$oid

                    cy.fixture('task.json')
                        .then((task) => {

                            task.userid = uid

                            cy.request({
                                method: 'POST',
                                url: 'http://localhost:5000/tasks/create',
                                form: true,
                                body: task
                            }).then((taskresponse) => {

                                tid = taskresponse.body[0]._id.$oid

                            })
                        })
                })
            })

    })

    beforeEach(function () {

        cy.visit('http://localhost:3000')

        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)

        cy.get('form')
            .submit()

        cy.contains('Learn React')
            .click()

    })

    // TC1
    it('creates a new todo item', () => {

        cy.get('input[placeholder="Add a new todo item"]')
            .type('Finish Cypress assignment')

        cy.contains('Add')
            .click()

        cy.contains('Finish Cypress assignment')
            .should('exist')

    })

    // TC2
    it('does not allow creating an empty todo item', () => {

        cy.contains('Add')
            .should('be.disabled')

    })

    // TC3
    it('toggles an active todo item to done', () => {

        cy.contains('Watch video')
            .parent()
            .find('.checker')
            .click()

        cy.contains('Watch video')
            .should('have.css', 'text-decoration')

    })

    // TC4
    it('toggles a done todo item back to active', () => {

        cy.contains('Watch video')
            .parent()
            .find('.checker')
            .click()

        cy.contains('Watch video')
            .parent()
            .find('.checker')
            .click()

        cy.contains('Watch video')
            .should('exist')

    })

    // TC5
    it('deletes a todo item', () => {

        cy.contains('Watch video')
            .parent()
            .find('.remover')
            .click()

        cy.contains('Watch video')
            .should('not.exist')

    })

    after(function () {

        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/tasks/byid/${tid}`
        })

        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        })

    })

})