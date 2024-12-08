import streamlit as st
# from back import df, Price_vs_Number_of_pieces, theme_hist
import back

st.title("Dataset")

st.dataframe(back.df)


with st.form("lin") as form:
    st.markdown(
        """
                # Scatterplot
        """
    )
    
    on = st.toggle("Show linear regression")
    
    options = back.df.theme_name.unique()[1:-1]
    selection = st.pills("Themes of lego sets", options, selection_mode="multi")
    
    options_of_con = back.df.country.unique()
    selection_of_con = st.pills("country", options_of_con, selection_mode="single")
    
    b_lin = st.form_submit_button("Show plot")
        

if b_lin:
    if not selection_of_con:
        st.markdown(
        """
            ## You have to choose a coutry
        """
        )
    elif not selection:
        st.markdown(
            '''
                ## You have to choose at least one theme
            '''
        )
    else:
        fig = back.Price_vs_Number_of_pieces(back.df, selection, country=selection_of_con, on=on)
        st.pyplot(fig)
        
    
st.header('Themes in dataset', divider='red')
hist = back.theme_hist()
st.pyplot(hist)

with st.form("min_max") as form:
    
    st.markdown(
        """
                # Lolypop
        """
    )
    
    options_of_col = ['list_price', 'piece_count']
    selection_of_col = st.pills("Columns", options_of_col, selection_mode="single")
    
    options_of_mode = ['min', 'max', 'mean']
    selection_of_mode = st.pills("Function", options_of_mode, selection_mode="single")
    
    
    b_min_max = st.form_submit_button("Show plot")
    
    if b_min_max:
        if selection_of_col and selection_of_mode:
            Lol = back.Lol(back.df, selection_of_col, selection_of_mode)
            st.pyplot(Lol)
        else:
            st.markdown(
            '''
                ## You have to choose function and column
            '''
            )   
            
            
    
st.header('Average price per piece', divider='violet')
bar = back.av()
st.pyplot(bar)