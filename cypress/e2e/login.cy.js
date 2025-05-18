describe('Logging into the system', () => {
  before(function () {
    return cy.fixture('userdata.json').then((user) => {
      return cy.request({
        method: 'POST',
        url: 'http://localhost:3000/users/create',
        form: true,
        body: user
      }).then((response) => {
        cy.wrap(response.body._id.$oid).as('uid')
        cy.wrap(user.firstName + ' ' + user.lastName).as('name')
        cy.wrap(user.email).as('email')
      })
    })
  })

  beforeEach(function () {
    cy.visit('http://localhost:3000')
  })

  it('starting out on the landing screen', () => {
    cy.get('h1').should('contain.text', 'Login')
  })

  it('login to the system with an existing account', function () {
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(this.email)

    cy.get('form').submit()

    cy.get('h1').should('contain.text', 'Your tasks, ' + this.name)
  })

  after(function () {
    if (this.uid) {
      cy.request({
        method: 'DELETE',
        url: `http://localhost:3000/users/${this.uid}`
      }).then((res) => {
        cy.log('User deleted:', res.body)
      })
    } else {
      cy.log('User ID not available, skip deletion')
    }
  })
})
