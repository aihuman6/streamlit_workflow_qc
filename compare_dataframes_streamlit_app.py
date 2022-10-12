from st_aggrid import AgGrid
import streamlit as st
import pandas as pd 


st.set_page_config(layout='wide') #Choose wide mode as the default setting

#Add a logo (optional) in the sidebar
#htp = "https://raw.githubusercontent.com/aihuman6/streamlit_apps/main/our_logo.png"
#response = requests.get(htp)
#logo = Image.open(BytesIO(response.content))
#logo.show()
#st.sidebar.image(logo, width=120)

#Add the expander to provide some information about the app
with st.sidebar.expander("About the App"):
     st.write("""
        This QC App was built by Branddelta using Streamlit and pandas package. You can use the app to compare the current and previous workflow aggregated outputs, and highlight any differences between them for QC purposes.Please note that datasets should have the same column names
     """)

#Add an app title. Use css to style the title
st.markdown(""" <style> .font {                                          
    font-size:30px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
st.markdown('<p class="font">Compare two datasets and highlight differences</p>', unsafe_allow_html=True)

#################################################################################################

uploaded_file1 = st.file_uploader("Upload your new aggregated workflow output:", type=['xlsx'])
uploaded_file2 = st.file_uploader("Upload your old aggregated workflow output:", type=['xlsx'])

if uploaded_file1 is not None and uploaded_file2 is not None:
    df1=pd.read_excel(uploaded_file1)
    df2=pd.read_excel(uploaded_file2)
#     latest_month = df1[(df1.Year==df1.Year.max())].Month.max()
#     latest_week = df1[(df1.Year==df1.Year.max()) & (df1.Month == latest_month)].Week.max()
#     latest_week_data = df1[(df1.Year==df1.Year.max()) & (df1.Month == latest_month) &
#                           (df1.Week == latest_week)]
#     df1 = df1[~df1.index.isin(list(latest_week_data.index))]
#     df1.reset_index(inplace=True, drop=True)
#     df2.reset_index(inplace=True, drop=True)
    
    option1=st.sidebar.radio(
     'What variables do you want to include in the report?',
     ('All variables', 'A subset of variables'))
    
    if option1=='All Variables':
        df1=df1
        df2=df2
    
    elif option1=='A subset of variables':
        var_list=list(df1.columns)
        option3=st.sidebar.multiselect(
            'Select variable(s) you want to include in the report.',
            var_list)
        df1=df1[option3]
        df2=df2[option3]
        
        
#########################################################################################

# =============================================================================
#     grid_response = AgGrid(
#         df,
#         editable=True, 
#         height=300, 
#         width='100%',
#         )
# 
#     updated = grid_response['data']
#     df1 = pd.DataFrame(updated) 
# =============================================================================

    if st.button('Compare datasets'):
        df_diff = pd.concat([df1,df2]).drop_duplicates(keep=False)
        if len(df_diff) == 0:
               st.text('Data matches for all weeks in the old file')
        else:
               grid_response = AgGrid(df_diff, editable=True, height=300, width='100%',)
               updated = grid_response['data']
               dff = pd.DataFrame(updated) 
          
  #      st.write(df_compare.columns)
  #      st.dataframe(df_compare.style.apply(apply_color, axis=None).hide_index())
        
        
