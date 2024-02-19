from h2o_wave import cypress


@cypress("body_test")
def body_test(cy):
    cy.visit("/recommender")
    cy.locate("search_box_input").type("Batman Begins")
    cy.locate("search").click()
    cy.locate("msg_text").should(
        "contain.text", "If you like Batman Begins, you may also like!"
    )

    for i in range(1, 6):
        cy.locate(f"movie{i}").should("exist")

    cy.locate("find_movies").click()

    for i in range(1, 6):
        cy.locate(f"movie{i}").should("not.exist")
        cy.locate(f"movie_match{i}").should("exist")

    cy.locate("search_box_input").clear().type("abcdef")
    cy.locate("search").click()
    cy.locate("msg_text").should(
        "contain.text",
        '"abcdef" is not in our database or is an invalid movie name. Use the "Find Movie" button to find movies',
    )


@cypress("header_test")
def header_test(cy):
    cy.visit("/recommender")
    cy.locate("github").click()


@cypress("footer_test")
def footer_test(cy):
    cy.visit("/recommender")
    cy.locate("github").click()
    cy.locate("linkedin").click()