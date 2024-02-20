from h2o_wave import ui, app, main, data
import pandas as pd
import sys

# Function to handle file operations and read the CSV file
def read_csv_file():
    file_name = './data/movies.csv'
    try:
        with open(file_name, 'r') as file:
            return pd.read_csv(file_name)
    except FileNotFoundError:
        print(f"File {file_name} not found. Aborting")
        sys.exit(1)
    except OSError:
        print(f"OS error occurred trying to open {file_name}")
        sys.exit(1)
    except Exception as err:
        print(f"Unexpected error opening {file_name}: {repr(err)}")
        sys.exit(1)



# Function to process and prepare the data for display
def prepare_data():
    data_frame = read_csv_file()
    data_frame.title = data_frame.title.interpolate(
        method='linear',
        limit_direction='forward',
        axis=0
    )
    data_frame.title = data_frame.title.fillna(method='bfill')
    data_list = list(data_frame.itertuples(index=False, name=None))
    return data_list[:1100]

# Set variable dataSet
data_set = prepare_data()

# Function to convert all elements in the tuples to strings
def stringify_content(int_list):
    return [list(map(str, i)) for i in int_list]

# Indicate that a function is a query handler.
@app('/')
async def controller(q):
    if not q.client.initialized:
        main_app(q)
        table_view(q)
        actor_view(q)
    
    # Finally, save the page.
    await q.page.save()

# Main app setup
def main_app(q):
    q.page['active_page_controller'] = ui.meta_card(
        theme='h2o-light',
        box='activePageController',
        layouts=[
            ui.layout(
                breakpoint='l',
                zones=[
                    ui.zone('header'),
                    ui.zone('content'),
                    ui.zone('footer'),
                ]),
        ])

    q.page['header'] = ui.header_card(
        box='header',
        subtitle="by Chamika Srimantha",
        icon='MyMoviesTV',
        title='''Movie Recommendation System''',
    )
    
    q.page['footer'] = ui.footer_card(
        box='footer',
        caption='''
        Chamika Srimantha
        ©2024 All rights reserved.'''
    )

    q.client.initialized = True

# Table view setup
def table_view(q):
    string_data_set = stringify_content(data_set)
    q.page['table_view'] = ui.form_card(
        box='content',
        items=[
            ui.text_xl(content='All Movies'),
            ui.table(
                name="data_table",
                columns=[
                    ui.table_column(
                        name='title', label='Movie Name', sortable=True, searchable=True, max_width='400'),
                    ui.table_column(
                        name='hero', label='Actor Name', searchable=True, sortable=True),
                    ui.table_column(
                        name='genre', label='Genre', searchable=True, sortable=True),
                    ui.table_column(
                        name='year', label='Released Year', searchable=True, sortable=True),
                    ui.table_column(
                        name='rating', label='Rating', searchable=True, sortable=True),
                ],
                rows=[
                    ui.table_row(
                        name=str(i + 1),
                        cells=string_data_set[i]
                    ) for i in range(len(string_data_set))
                ],
                downloadable=True,
                width="100%",
                height='500px',
                resettable=True,
            ),
        ],
    )






# Actor view setup
def actor_view(q):
    # Read the result from the CSV file
    result_df = pd.read_csv('./data/result.csv')

    # Convert the DataFrame to a list of tuples
    data_set = [(row['Name'], row['Rating']) for index, row in result_df.iterrows()]

    # string_data_set = stringify_content(data_set)

    q.page['analysis'] = ui.plot_card(
        box='content',
        title='Predicted rating for 2024',
        data=data('actor rating', 5, rows=data_set),
        plot=ui.plot([ui.mark(type='interval', x='=actor', y='=rating', y_min=0)])
    )

