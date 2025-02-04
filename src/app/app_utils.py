import pandas as pd
import numpy as np
import streamlit as st
from io import BytesIO

def df_to_excel_buffer(df):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=None)
    return buffer

# This is to display only part of the dataframe if it has more than a certain number of rows. Displaying dataframes with too many rows slows down streamlit
def display_large_df(df, max_rows=1000, **st_dataframe_kwargs):
    n_rows = len(df)
    if n_rows <= max_rows:
        # As a special case, display small dataframe directly.
        st.write(df)
    else:
        # Slice the DataFrame to display less information.
        start_row = st.slider('Start row', 0, n_rows - max_rows)
        end_row = start_row + max_rows
        df = df[start_row:end_row]

        # Reindex Numpy arrays to make them more understadable.
        if type(df) == np.ndarray:
            df = pd.DataFrame(df)
            df.index = range(start_row,end_row)

        # Display everything.
        st.dataframe(df, **st_dataframe_kwargs)
        st.text('Displaying rows %i to %i of %i.' % (start_row, end_row - 1, n_rows))