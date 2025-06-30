from Libraries import *
import streamlit as st
import requests


display_modes = ["Table", "Line Chart", "Area Chart", "Bar Chart"]
countries = ["China", "India", "Finland", "Iceland", "Nepal", "United Arab Emirates", "United States", "United Kingdom", "Yemen", "Russia", "Ukraine", "Andorra", "Afghanistan", "Antigua and Barbuda", "Anguilla", "Armenia", "Angola", "Argentina", "Austria", "Australia", "Aruba", "Azerbaijan", "Bosnia and Herzegovina", "Barbados", "Belgium", "Burkina Faso", "Bulgaria", "Bahrain", "Burundi", "Cabo Verde", "Benin", "Bermuda", "Brunei", "Bolivia", "Caribbean Netherlands", "Brazil", "Bahamas", "Bhutan", "Botswana", "Belarus", "Belize", "Canada", "DRC", "Congo", "Central African Republic", "Switzerland", "Côte d'Ivoire", "Cook Islands", "Chile", "Cameroon", "Colombia", "Costa Rica", "Cuba", "Curaçao", "Cyprus", "Czechia", "Germany", "Djibouti", "Denmark", "Dominica", "Dominican Republic", "Algeria", "Ecuador", "Estonia", "Egypt", "Western Sahara", "Eritrea", "Spain", "Ethiopia", "Fiji", "Falkland Islands", "Micronesia", "Faroe Islands", "France", "Gabon", "Ireland", "Grenada", "Georgia", "French Guiana", "Ghana", "Gibraltar", "Greenland", "Gambia", "Guinea", "Guadeloupe", "Equatorial Guinea", "Greece"  "Georgia", "Guatemala", "Guinea-Bissau", "Guyana", "Hong Kong", "Honduras", "Croatia", "Haiti", "Hungary", "Indonesia", "Ireland", "Israel", "Isle of Man", "Iraq", "Iran", "Italy", "Jamaica", "Jordan", "Japan", "Kyrgyzstan", "Kenya", "Cambodia", "Kiribati", "Comoros", "Saint Kitts and Nevis", "North Korea", "South Korea", "Kuwait", "Cayman Islands", "Kazakhstan", "Lebanon", "Saint Lucia", "Liechtenstein", "Liberia", "Lesotho", "Lithuania", "Luxembourg", "Latvia", "Libyan Arab Jamahiriya", "Morocco", "Madagascar", "Monaco", "Moldova", "Montenegro", "Saint Martin", "Marshall Islands", "Macedonia", "Mali", "Myanmar", "Mongolia", "Macao", "Martinique", "Mauritania", "Montserrat", "Malta", "Mauritius", "Maldives", "Malawi", "Mexico", "Malaysia", "Mozambique", "Namibia", "New Caledonia", "Nigeria", "Niger", "Nicaragua", "Netherlands", "Norway", "Nauru", "Niue", "New Zealand", "Oman", "Panama", "Peru", "French Polynesia", "Papua New Guinea", "Philippines", "Pakistan", "Poland", "Saint Pierre Miquelon", "Palestine", "Portugal", "Palau", "Paraguay", "Qatar", "Réunion", "Romania", "Serbia", "Rwanda", "Saudi Arabia", "Solomon Islands", "Seychelles", "South Sudan", "Sudan", "Singapore", "Sweden", "Saint Helena", "Slovenia", "Slovakia", "Sierra Leone", "San Marino", "Senegal", "Somalia", "Suriname", "South Sudan", "Sao Tome and Principe", "El Salvador", "Sint Maarten", "Syrian Arab Republic", "Swaziland", "Turks and Caicos Islands", "Channel Islands", "Chad", "Togo", "Thailand", "Tajikistan", "Tokelau", "Timor-Leste", "Tunisia", "Tonga", "Turkey", "Trinidad and Tobago", "Tuvalu", "Taiwan", "Tanzania", "Uganda", "Uruguay", "Uzbekistan", "Vatican city", "Saint Vincent and the Grenadines", "Venezuela", "British Virgin Islands", "Vietnam", "Vanuatu", "Wallis and Futuna", "Samoa", "Mayotte", "South Africa", "Zambia", "Zimbabwe", "Albania"]

#Sidebar
country = st.sidebar.selectbox('Pick a Country', countries) #Dropdown
days = st.sidebar.slider('days', min_value = 50, max_value = 100, step = 1) #Slider
display_mode = st.sidebar.selectbox('Pick a Data Type', display_modes) #Select display mode
Refresh = False
if st.button("Click if error occurs"):
    Refresh = True

#Request
API = requests.get(f"https://disease.sh/v3/covid-19/countries/{country}")
Data = API.json()

#Total cases
total_cases = get_historic_cases(country, str(days))
total_deaths = get_historic_deaths(country, str(days))
total_recoveries = get_historic_recoveries(country, str(days))

#Total cases dataframe
total_df = pd.concat([total_cases, total_deaths, total_recoveries], axis=1).astype(int)

#Yesterday cases
yesterday_cases = get_yesterday_cases(country)
yesterday_deaths = get_yesterday_deaths(country)
yesterday_recoveries = get_yesterday_recoveries(country)

#Yesterday cases dataframe
#yesterday_df = pd.concat([yesterday_cases, yesterday_deaths, yesterday_recoveries], axis=1).astype(int)

#Daily cases
daily_cases = get_daily_cases(country, str(days))
daily_deaths = get_daily_deaths(country, str(days))
daily_recoveries = get_daily_recoveries(country, str(days))

#Daily cases 
daily_df = pd.concat([daily_cases, daily_deaths, daily_recoveries], axis=1).astype(int)
##st.write(total_df)

#Display
st.title('Covid 19 Visualization Dashboard') #Title
st.subheader("Country Details") #Sub-heading
col5, col4 = st.columns(2)
col5.metric('Selected Country', country) #Print selected country
col4.image(Data["countryInfo"]["flag"]) #Flag image
col8, col9 = st.columns(2)
col8.metric("Latitude", Data["countryInfo"]["lat"])
col9.metric("Longtitude", Data["countryInfo"]["long"])
st.subheader("Data")
col1, col2, col3 = st.columns(3)
col1.metric("Yesterday's Cases", yesterday_cases) #Mentions
col2.metric("Yesterday's Deaths", yesterday_deaths) #Mentions
col3.metric("Yesterday's Recoveries", yesterday_recoveries) #Mentions
if display_mode == "Line Chart":
    st.line_chart(daily_df) #Line chart
elif display_mode == "Table":
    st.table(daily_df) #Table
elif display_mode == "Area Chart":
    st.area_chart(daily_df)
elif display_mode == "Bar Chart":
    st.bar_chart(daily_df)
else:
    st.write("Display mode not chosen!")
st.divider() #Divider
st.subheader("About Covid 19")
col7, col6 = st.columns(2)
col6.video("https://www.youtube.com/watch?v=zME-84Vwjuo") #Video
col7.image("Picture.png", caption = "Ways to prevent covid 19") #Picture
with open("Picture.png", "rb") as file:
    btn = st.download_button(label = "Download Poster", data = file, file_name="Corona poster.png", mime="image/png")
