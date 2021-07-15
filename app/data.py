
def upper_country(counr):
    # return (counr.upper(), counr)
    return (counr, counr)

def choiscountry():

    country = ['Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola',
               'Anguilla', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia',
               'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus',
               'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire, Sint Eustatius and Saba',
               'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'British Virgin Islands', 'Brunei',
               'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
               'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros',
               'Congo', 'Costa Rica', 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark',
               'Djibouti', 'Dominica', 'Dominican Republic', 'DR Congo', 'East Timor', 'Ecuador', 'Egypt',
               'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia',
               'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'Gabon',
               'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada',
               'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti',
               'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland',
               'Isle of Man', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jersey', 'Jordan',
               'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Lao', 'Latvia', 'Lebanon',
               'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Madagascar',
               'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Martinique', 'Mauritania', 'Mauritius',
               'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique',
               'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua',
               'Niger', 'Nigeria', 'North Korea', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palestine',
               'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal',
               'Puerto Rico', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Barthélemy', 'Saint Kitts and Nevis',
               'Saint Lucia', 'Saint Martin', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino',
               'São Tomé and Príncipe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone',
               'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa',
               'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland',
               'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago',
               'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Uganda', 'Ukraine',
               'United Arab Emirates', 'United Kingdom', 'Uruguay', 'US Virgin Islands', 'USA', 'Uzbekistan',
               'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Wallis and Futuna', 'Yemen', 'Zambia',
               'Zimbabwe']

    country_choises = list(map(upper_country, country))

    return country_choises