from flask import Flask, request, render_template
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import mysql.connector

app = Flask(__name__)

# Function to fetch data from MySQL
def fetch_data_from_mysql():
    config = {
        'user': 'root',
        'password': 'pass',
        'host': 'localhost',
        'database': 'flaskapp'
    }

    connection = mysql.connector.connect(**config)
    query = """
    SELECT 
        product_id, product_name, brand, processor, graphics,
        dimensions, weight, os, memory, storage, 
        power_supply, battery, price
    FROM product
    """

    df = pd.read_sql(query, connection)
    connection.close()
    return df

# Fetch data from MySQL
df = fetch_data_from_mysql()

# Rename columns to match your original DataFrame
df.columns = [
    'Product ID', 'Product Name', 'Brand', 'Processor', 'Graphics', 
    'Dimensions', 'Weight (g)', 'Operating System', 'Memory', 'Storage', 
    'Power Supply', 'Battery', 'Price (MYR)'
]

# Function to combine features
def combine_features(row):
    return (
        row['Brand'] + " " +
        row['Processor'] + " " +
        row['Graphics'] + " " +
        row['Dimensions'] + " " +
        row['Operating System'] + " " +
        row['Memory'] + " " +
        row['Storage'] + " " +
        row['Power Supply'] + " " +
        row['Battery']
    )

df["combined_features"] = df.apply(combine_features, axis=1)

# Creating the count matrix
cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])

# Computing the cosine similarity based on the count matrix
cosine_sim = cosine_similarity(count_matrix)

# Function to get the title from the index
def get_title_from_index(index):
    return df[df.index == index]["Product Name"].values[0]

# Function to get the index from the title
def get_index_from_title(title):
    return df[df["Product Name"] == title].index.values[0]

def classify_laptop(processor, graphics, memory, storage, battery, weight):
    # Determine the performance tier based on processor
    if 'i7' in processor or 'i9' in processor or 'Ryzen 7' in processor or 'Ryzen 9' in processor:
        cpu_tier = 'high-end'
    elif 'i5' in processor or 'Ryzen 5' in processor:
        cpu_tier = 'mid-tier'
    else:
        cpu_tier = 'low-end'

    # Determine the performance tier based on graphics
    if 'RTX' in graphics and any(num in graphics for num in ['3000', '4000']):
        gpu_tier = 'high-end'
    elif 'GTX' in graphics or 'RTX 2000' in graphics:
        gpu_tier = 'mid-tier'
    else:
        gpu_tier = 'low-end'

    # Determine the performance tier based on memory
    if memory >= 16:
        memory_tier = 'high-end'
    elif memory == 8:
        memory_tier = 'mid-tier'
    else:
        memory_tier = 'low-end'

    # Determine the performance tier based on storage
    if storage >= 1024:
        storage_tier = 'high-end'
    elif storage == 512:
        storage_tier = 'mid-tier'
    else:
        storage_tier = 'low-end'

    # Determine the performance tier based on battery
    if battery >= 70:
        battery_tier = 'high-end'
    elif battery >= 50:
        battery_tier = 'mid-tier'
    else:
        battery_tier = 'low-end'

    # Determine the portability based on weight
    if weight < 1500:
        weight_class = 'portable'
    elif weight <= 2500:
        weight_class = 'standard'
    else:
        weight_class = 'heavy'

    return {
        'cpu_tier': cpu_tier,
        'gpu_tier': gpu_tier,
        'memory_tier': memory_tier,
        'storage_tier': storage_tier,
        'battery_tier': battery_tier,
        'weight_class': weight_class
    }

def get_specs_from_survey(data):
    specs = {
        'Brand': '',
        'Processor': '',
        'Graphics': '',
        'Dimensions': '',
        'Operating System': '',
        'Memory': '',
        'Storage': '',
        'Power Supply': '',
        'Battery': ''
    }

    if data['primary_use'] == 'general-use':
        specs.update({'Processor': 'i3', 'Graphics': 'Integrated', 'Memory': '4GB'})
    
    elif data['primary_use'] == 'education':
        if data.get('education_activities') == 'writing':
            specs.update({'Processor': 'i3', 'Graphics': 'Integrated', 'Memory': '4GB'})
        elif data.get('education_activities') == 'programming':
            if data.get('high-performance') == 'yes':
                specs.update({'Processor': 'i7', 'Graphics': 'GTX 1660', 'Memory': '16GB'})
            else:
                specs.update({'Processor': 'i5', 'Graphics': 'Integrated', 'Memory': '8GB'})
        elif data.get('education_activities') == 'design':
            if data.get('high-performance') == 'yes':
                specs.update({'Processor': 'i7', 'Graphics': 'RTX 2060', 'Memory': '16GB'})
            else:
                specs.update({'Processor': 'i5', 'Graphics': 'GTX 1050', 'Memory': '8GB'})
    
    elif data['primary_use'] == 'gaming':
        if data.get('gaming_type') == 'high-end':
            specs.update({'Processor': 'i7', 'Graphics': 'RTX 3080', 'Memory': '16GB'})
        elif data.get('gaming_type') == 'mid-tier':
            specs.update({'Processor': 'i5', 'Graphics': 'GTX 1660', 'Memory': '8GB'})
        else:
            specs.update({'Processor': 'i3', 'Graphics': 'Intel HD', 'Memory': '4GB'})
    
    elif data['primary_use'] == 'professional-work':
        if data.get('professional_work') == 'graphic-design':
            specs.update({'Processor': 'i7', 'Graphics': 'RTX 2060', 'Memory': '16GB'})
        elif data.get('professional_work') == 'programming':
            specs.update({'Processor': 'i5', 'Graphics': 'Integrated', 'Memory': '8GB'})
        elif data.get('professional_work') == 'video-editing':
            specs.update({'Processor': 'i7', 'Graphics': 'RTX 3080', 'Memory': '32GB'})
    
    if data['brand'] != 'no-preference':
        specs['Brand'] = data['brand']
    
    if data['os'] != 'no-preference':
        specs['Operating System'] = data['os']
    
    if data['price'] == 'budget':
        specs['Price (MYR)'] = '<500'
    elif data['price'] == 'mid-range':
        specs['Price (MYR)'] = '500-1000'
    elif data['price'] == 'high-end':
        specs['Price (MYR)'] = '1000-2000'
    elif data['price'] == 'premium':
        specs['Price (MYR)'] = '>2000'
    
    return specs

@app.route('/', methods=['GET'])
def index():
    return render_template('Survey.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.form
    specs = get_specs_from_survey(data)
    combined_query = " ".join(specs.values())

    query_vector = cv.transform([combined_query])
    cosine_scores = cosine_similarity(query_vector, count_matrix)

    similar_products = list(enumerate(cosine_scores[0]))
    sorted_similar_products = sorted(similar_products, key=lambda x: x[1], reverse=True)[1:]

    recommendations = []
    for element in sorted_similar_products:
        recommendations.append(get_title_from_index(element[0]))
        if len(recommendations) >= 5:
            break

    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
