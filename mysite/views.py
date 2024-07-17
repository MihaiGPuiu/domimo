import os
import django
import pandas as pd
import re
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed,HttpResponse
from django.views.decorators.http import require_POST
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# Read the Excel file
excel_file = 'apartment.xlsx'
df = pd.read_excel(excel_file)

def remove_numbers(text):
    # Define a regular expression pattern to match digits
    pattern = r'\d+'
    # Use the sub() function to replace digits with an empty string
    return re.sub(pattern, '', text)

# Apply the remove_numbers function to the "District" column
df['District'] = df['District'].apply(remove_numbers)

def display_columns(request):
    # Get the search query and filters from the request
    query = request.GET.get("search", "")
    filter_title = request.GET.get("filter_title", "")
    filter_city = request.GET.get("filter_city", "")
    filter_surface = request.GET.get("filter_city", "")
    
    print("Search Query:", query)
    print("Filter Title:", filter_title)
    print("Filter City:", filter_city)

    # Filter DataFrame based on the search query and filters
    filtered_df = df.copy()
    
    if query:
        filtered_df = filtered_df[filtered_df['Title'].str.contains(query, case=False, na=False)]
    
    if filter_title:
        filtered_df = filtered_df[filtered_df['Title'].str.contains(filter_title, case=False, na=False)]
    
    if filter_city:
        filtered_df = filtered_df[filtered_df['City'].str.contains(filter_city, case=False, na=False)]
    
    if filter_surface:
        filtered_df = filtered_df[filtered_df['Surface'].str.contains(filter_city, case=False, na=False)]
    
    print("Filtered DataFrame:", filtered_df)

    # Convert filtered DataFrame to a list of dictionaries
    apartments = []
    for index, row in filtered_df.iterrows():
        apartment = {
            'title': row['Title'],
            'city': row['City'],
            'surface': row['Surface'],
            'price': row['Price'],
            'image': row['Image_links'],
        }
        apartments.append(apartment)

    # Get the list of unique cities for the dropdown filter
    cities = df['City'].unique()

    # Pass data to the template
    return render(request, 'search_results.html', {'apartments': apartments, 'query': query, 'filter_title': filter_title,"filter_surface": filter_surface,'filter_city': filter_city, 'cities': cities})


