# app.py
from rec_sys.rec_func import recommender
from h2o_wave import Q, main, app, ui
from fuzzywuzzy import process
from typing import Any


def search_movies(movie_name: str) -> list[tuple[Any, Any | int, Any] | tuple[Any, Any | int]]:
    """
    Find similar movies name wise (using Levenshtein distance).
    """
   
    return process.extract(movie_name, recommender.movie_names)


@app("/recommender")
async def serve(q: Q):
    """
    Displays the recommended movies according to the input.
    If the user cannot find the movie, they can find movies that match the given input.
    """
    msg = ""

    if not q.client.initialized:
        q.client.initialized = True

    if q.args.search:
        del q.page["movies"]
        q.args.search_box_input = q.args.search_box_input.strip()
       
        if q.args.search_box_input in recommender.movie_names:
            result = recommender.recommend(q.args.search_box_input)

            msg = f"If you like {q.args.search_box_input}, you may also like!"
            add_movie_cards(result, q)

        elif q.args.search_box_input is None or q.args.search_box_input == "":
            msg = "Movie name cannot be blank."

        else:
            msg = f'"{q.args.search_box_input}" is not in our database or is an invalid movie name.\
            Use the "Find Movie" button to find movies'

    if q.args.find_movies:
        q.args.search_box_input = q.args.search_box_input.strip()
        if q.args.search_box_input is None or q.args.search_box_input == "":
            msg = "Movie name cannot be blank."
        else:
            for i in range(1, 6):
                del q.page[f"movie{i}"]
            add_similar_movies(q)

    add_search_box(q, msg)
    add_header(q)
    add_footer(q)

    await q.page.save()


def add_similar_movies(q: Q):
    similar_movies = search_movies(q.args.search_box_input)
    q.page["movies"] = ui.form_card(
        box="2 4 10 7",
        items=[
            ui.copyable_text(
                value=movie[0],
                name=f"movie_match{i+1}",
                label=f"{movie[1]}% match",
            )
            for i, movie in enumerate(similar_movies)
        ],
    )


def add_movie_cards(result, q: Q):
    for i in range(1, 6):
        q.page[f"movie{i}"] = ui.tall_article_preview_card(
            box=f"{2*i} 4 2 7",
            title=f"{result[i-1].title}",
            subtitle=f"{result[i-1].director}",  # Assuming 'director' is available for movies
            value=f"{result[i-1].release_year}",  # Assuming 'release_year' is available for movies
            name="tall_article",
            image=f"{result[i-1].poster}",  # Assuming 'poster' URL is available for movies
            items=[
                ui.text(f"{result[i-1].genre}", size="l"),  # Assuming 'genre' is available for movies
                ui.text(f"Rating: {result[i-1].rating}", size="m"),  # Assuming 'rating' is available for movies
            ],
        )


def add_search_box(q: Q, msg):
    q.page["search_box"] = ui.form_card(
        box="2 2 10 2",
        items=[
            ui.textbox(
                name="search_box_input",
                label="Movie Name",
                value=q.args.search_box_input,
            ),
            ui.buttons(
                items=[
                    ui.button(
                        name="search",
                        label="Search",
                        primary=True,
                        icon="Movie",
                    ),
                    ui.button(name="find_movies", label="Show Recommendation", primary=False),
                ]
            ),
            ui.text(msg, size="m", name="msg_text"),
        ],
    )


def add_footer(q: Q):
    caption = """___Developed by Chamika Srimantha__ <br /> using __[h2o Wave](https://wave.h2o.ai/docs/getting-started).__"""
    q.page["footer"] = ui.footer_card(
        box="2 11 10 2",
        caption=caption,
        items=[
            ui.inline(
                justify="end",
                items=[
                    ui.links(
                        label="Contact Me",
                        width="200px",
                        items=[
                            ui.link(
                                name="github",
                                label="GitHub",
                                path="https://github.com/chamikasrimantha/h2o-wave-app",
                                target="_blank",
                            ),
                            ui.link(
                                name="linkedin",
                                label="LinkedIn",
                                path="https://www.linkedin.com/in/chamika-srimantha/",
                                target="_blank",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )