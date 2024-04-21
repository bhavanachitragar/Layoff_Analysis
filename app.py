import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(layout='wide',page_title='Layoff Analysis')

df = pd.read_csv('layoff_cleaned_data (1).csv')
df['Date'] = pd.to_datetime(df['Date'],errors='coerce')

# Analytics
def analysis():
    if option == 'Overall Analytics':
        st.title('Overall Analytics')

        # total invested amount
        total = round(df['Company'].nunique())
        stages_num=round(df['Stage'].nunique())
        ind_num=round(df['Industry'].nunique())
        fund=round(df['Funds_Raised'].sum())

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric('Total Companies', str(total))
        with col2:
            st.metric('Total Stages',str(stages_num))
        with col3:
            st.metric('Total Industries',str(ind_num))
        with col4:
            st.metric('Funds_Raised', str(fund) + 'Cr')



    # Piechart
    df['Year'] = df['Date'].dt.year
    layoffs_by_year = df.groupby('Year')['Layoffs'].sum().reset_index()
    fig = px.pie(data_frame=layoffs_by_year, values='Layoffs', names='Year', title='Distribution of Layoffs by Year')
    st.plotly_chart(fig, theme="streamlit")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        compa_df = df.groupby(['Year', 'Date', 'Company', 'Location_HQ', 'Industry', 'Stage', 'Country'])[
            'Layoffs'].sum().reset_index()
        selected_year = st.selectbox('Select Year', sorted(df['Year'].unique()))
        selected_year_df = compa_df[compa_df['Year'] == selected_year]

    # Barchart
    # Location
    layoffs_by_location = selected_year_df.groupby('Location_HQ')['Layoffs'].sum().sort_values(ascending=False).head(10).reset_index()
    fig1 = px.bar(data_frame=layoffs_by_location, x='Location_HQ', y='Layoffs', title='Locations with the Highest Number of Layoffs',labels={'Location_HQ': 'Location', 'Layoffs': 'Number of Layoffs'},color='Layoffs', color_continuous_scale=px.colors.sequential.RdBu)
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

    # Country
    layoffs_by_country= selected_year_df.groupby('Country')['Layoffs'].sum().sort_values( ascending=False).reset_index()
    fig_bar = px.bar(data_frame=layoffs_by_country,x='Country',y='Layoffs',title='Countries with the Highest Number of Layoffs',labels={'Country': 'Country', 'Layoffs': 'Number of Layoffs'},color='Layoffs',color_continuous_scale=px.colors.sequential.RdBu)
    st.plotly_chart(fig_bar, theme="streamlit", use_container_width=True)

    # Companies
    layoffs_by_company = selected_year_df.groupby('Company')['Layoffs'].sum().sort_values(ascending=False).reset_index().head(10)
    fig_bar1 = px.bar(data_frame=layoffs_by_company, x='Company', y='Layoffs', title='Companies with the Highest Number of Layoffs',labels={'Company': 'Company', 'Layoffs': 'Number of Layoffs'},color='Layoffs', color_continuous_scale=px.colors.sequential.RdBu)
    st.plotly_chart(fig_bar1, use_container_width=True)

    # Stages
    layoffs_by_stage = selected_year_df.groupby('Stage')['Layoffs'].sum().reset_index().sort_values(by='Layoffs', ascending=False)
    fig_bar2 = px.bar(data_frame=layoffs_by_stage, x='Stage', y='Layoffs', title='Layoffs by Stages',labels={'Stage': 'Stage', 'Layoffs': 'Number of Layoffs'},color='Layoffs',color_continuous_scale=px.colors.sequential.RdBu)
    st.plotly_chart(fig_bar2, use_container_width=True)

    # Industries
    layoffs_by_ind = selected_year_df.groupby('Industry')['Layoffs'].sum().reset_index().sort_values(by='Layoffs', ascending=False)
    fig_bar3 = px.bar(data_frame=layoffs_by_ind, x='Industry', y='Layoffs', title='Layoffs by Industries',labels={'Industry': 'Industries', 'Layoffs': 'Number of Layoffs'},color='Layoffs',color_continuous_scale=px.colors.sequential.RdBu)
    st.plotly_chart(fig_bar3, use_container_width=True)

    # Linechart
    layoffs_by_year2 = (selected_year_df.groupby('Date')['Layoffs'].sum().reset_index())
    fig_date = px.line(data_frame=layoffs_by_year2,x='Date',y='Layoffs',title='Total Layoffs by Year')
    fig_date.update_layout(title_x=0.5)
    fig_date.update_traces(line_color='white')
    st.plotly_chart(fig_date, theme="streamlit",use_container_width=True)

    # mapplot
    country_layoffs = selected_year_df.groupby('Country')['Layoffs'].sum()
    fig21 = px.choropleth(country_layoffs.reset_index(),
                         locations='Country',
                         locationmode='country names',
                         color='Layoffs',
                         hover_name='Country',
                         color_continuous_scale=px.colors.sequential.RdBu,
                         title='Number of Layoffs by Country')
    st.plotly_chart(fig21, use_container_width=True)

# Country
def Country_analysis(country):
    if option == 'Country':
        st.title('Analytics')
        st.subheader(country)


        in_total = round(df[df['Country'].str.contains(country)]['Company'].nunique())
        in_stages_num = round(df[df['Country'].str.contains(country)]['Stage'].nunique())
        in_ind_num = round(df[df['Country'].str.contains(country)]['Industry'].nunique())
        in_state= round(df[df['Country'].str.contains(country)]['Location_HQ'].nunique())
        in_fund = round(df[df['Country'].str.contains(country)]['Funds_Raised'].sum())
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric('Companies', str(in_total))
        with col2:
            st.metric('Stages', str(in_stages_num))
        with col3:
            st.metric('Industry', str(in_ind_num))
        with col4:
            st.metric('States', str(in_state))

# Barchart
    # Location
    country_location = df[df['Country'].str.contains(country)].groupby('Location_HQ')['Layoffs'].sum()
    top_10_locations = country_location.sort_values(ascending=False).head(10).reset_index()
    fig10 = px.bar(data_frame=top_10_locations, x='Location_HQ', y='Layoffs', title='Locations with the Highest Number of Layoffs',labels={'Location_HQ': 'Location', 'Layoffs': 'Number of Layoffs'},color='Layoffs', color_continuous_scale=px.colors.sequential.Jet)
    st.plotly_chart(fig10, theme="streamlit", use_container_width=True)

    # Company
    country_company = df[df['Country'].str.contains(country)].groupby('Company')['Layoffs'].sum()
    top_10_locations = country_company.sort_values(ascending=False).head(10).reset_index()
    fig10 = px.bar(data_frame=top_10_locations, x='Company', y='Layoffs',title='Companies with the Highest Number of Layoffs',labels={'Company': 'Company', 'Layoffs': 'Number of Layoffs'}, color='Layoffs',color_continuous_scale=px.colors.sequential.Jet)
    st.plotly_chart(fig10, theme="streamlit", use_container_width=True)

    # Stage
    country_stage = df[df['Country'].str.contains(country)].groupby('Stage')['Layoffs'].sum().reset_index()
    top_10_stage = country_stage.sort_values(by='Layoffs', ascending=False)
    fig_bar2 = px.bar(top_10_stage, x='Stage', y='Layoffs', title='Layoffs by Stages',labels={'Stage': 'Stage', 'Layoffs': 'Number of Layoffs'}, color='Layoffs',color_continuous_scale=px.colors.sequential.Jet)
    st.plotly_chart(fig_bar2, use_container_width=True)

    # Industry
    country_ind = df[df['Country'].str.contains(country)].groupby('Industry')['Layoffs'].sum().reset_index()
    top_10_companies = country_ind.sort_values(by='Layoffs', ascending=False).head(10)
    fig_bar3 = px.bar(top_10_companies, x='Industry', y='Layoffs', title='Layoffs by Industries',labels={'Industry': 'Industry', 'Layoffs': 'Number of Layoffs'}, color='Layoffs',color_continuous_scale=px.colors.sequential.Jet)
    st.plotly_chart(fig_bar3, use_container_width=True)

    # Linechart
    # Year
    layoffs_by_year2 = df[df['Country'].str.contains(country)].groupby('Date')['Layoffs'].sum().reset_index()
    fig_date = px.line(layoffs_by_year2, x='Date', y='Layoffs', title='Total Layoffs by Year')
    fig_date.update_layout(title_x=0.5)
    fig_date.update_traces(line_color='white')
    st.plotly_chart(fig_date, theme="streamlit", use_container_width=True)

def load_company(company):
    st.title(company)
    st.subheader('Basic Information:')

    col1, col2 = st.columns(2)
    with col1:
        company_name = df[df['Company'].str.contains(company)]['Industry'].iloc[0]
        st.info(f'**Industry:** {company_name}')

        company_year = df[df['Company'].str.contains(company)]['Year'].iloc[0]
        st.info(f'**Layoff Year:** {company_year}')

        company_lay = df[df['Company'].str.contains(company)]['Layoffs'].iloc[0]
        if pd.isna(company_lay):
            company_lay = 'Undisclosed'
        else:
            company_lay = int(company_lay)
        st.info(f'**Layoff Count:** {company_lay}')
        company_cou = df[df['Company'].str.contains(company)]['Country'].iloc[0]
        st.info(f'**Company Location:** {company_cou}')
        company_fun = df[df['Company'].str.contains(company)]['Funds_Raised'].iloc[0]
        if company_fun == 0.0:
            company_fun = 'Undisclosed'
        else:
            company_fun = str(int(company_fun)) + 'Cr'
        st.info(f'**Fund Raised:** {company_fun}')
        company_stage = df[df['Company'].str.contains(company)]['Stage'].iloc[0]
        st.info(f'**Stage:** {company_stage}')

    yr_series = (df[df['Company'].str.contains(company)].groupby('Date')['Layoffs'].sum().reset_index())
    fig_date = px.line(data_frame=yr_series, x='Date', y='Layoffs', title='Total Layoffs by Year')
    fig_date.update_layout(title_x=0.5)
    fig_date.update_traces(line_color='white')
    st.plotly_chart(fig_date, theme="streamlit",use_container_width=True)

    # MAP
    country_layoffs = df[df['Company'].str.contains(company)].groupby('Country')['Layoffs'].sum()
    fig21 = px.choropleth(country_layoffs.reset_index(),
                          locations='Country',
                          locationmode='country names',
                          color='Layoffs',
                          hover_name='Country',
                          color_continuous_scale=px.colors.sequential.Jet,
                          title='Layoffs by Country')
    st.plotly_chart(fig21, use_container_width=True)

# Sidebar
st.sidebar.title('Layoff Analysis')
option=st.sidebar.selectbox('Menu',['Select one','Overall Analytics','Country','Company'])

if option == 'Overall Analytics':
    analysis()
elif option == 'Country':
    country = st.sidebar.selectbox('Select Country', sorted(set(df['Country'].str.split(',').sum())))
    btn1 = st.sidebar.button('Find Country')
    if btn1:
        Country_analysis(country)
elif option == 'Company':
    comp = st.sidebar.selectbox('Select Company', sorted(set(df['Company'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Company')
    if btn2:
        load_company(comp)
else:
    st.title('Layoff Data Analysis')
    st.write("**Project Overview:**")
    st.write('This Streamlit app is designed for Layoff Analysis. It allows users to explore and analyze layoff data from different perspectives, including overall analytics, country-specific insights, and individual company details.')
    st.write()
    st.write('An overview of the features:')
    st.write("""
    ## **1. Overall Analytics:**
    - Displays total companies, stages, industries, and funds raised across all data.
    - Includes a pie chart showing the distribution of layoffs by year.

    ## **2. Country Analysis:**
    - Allows users to select a specific country and view analytics related to layoffs in that country.
    - Provides information such as the total number of companies, stages, industries, and states affected by layoffs in the selected country.
    - Includes bar charts showing the top locations, companies, stages, and industries with the highest number of layoffs in the selected country.
    - Shows a line chart depicting the total layoffs by year in the selected country.
    - Presents a choropleth map displaying the distribution of layoffs by country.

    ## **3. Company Analysis:**
    - Enables users to select a specific company and view detailed information about it.
    - Provides basic information about the company, including its industry, layoff year, count, location, funds raised, and stage.
    - Displays a line chart showing the total layoffs by year for the selected company.
    - Shows a choropleth map indicating the distribution of layoffs by country for the selected company.
    """)
