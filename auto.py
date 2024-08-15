import os
import mysql.connector

# Define categories and associated keywords
categories = {
    'Productivity': ['onedrive', 'keynote', 'onenote', 'microsoft word', 'microsoft excel', 'microsoft powerpoint', 'calendar', 'numbers', 'pages', 'draw.io', 'canva', 'apspace'],
    'Media': ['audacity', 'ffmpeg', 'media player', 'photo viewer', 'imovie', 'garageband', 'bandicam'],
    'Development': ['visual studio code', 'netbeans', 'azure data studio', 'git', 'obs-studio', 'mysqlworkbench', 'swi-prolog', 'docker', 'rapidminer studio'],
    'Utilities': ['teams', 'bonjour', 'windows defender', 'windows mail', 'putty', 'hp', 'wsl', '7-zip', 'dotnet', 'faceit', 'nzxt cam', 'streamlabs', 'testproject', 'winpcap'],
    'Games': ['game', 'launcher', 'hoyoplay', 'steam', 'wildgames', 'riot vanguard', 'easyanticheat'],
    'Other': []
}

def detect_top_level_apps(directory):
    apps = []
    
    try:
        for entry in os.listdir(directory):
            subdir_path = os.path.join(directory, entry)
            
            if os.path.isdir(subdir_path):
                try:
                    for file in os.listdir(subdir_path):
                        if file.endswith('.exe'):
                            apps.append(os.path.join(subdir_path, file))
                            break
                except (PermissionError, OSError):
                    print(f"Permission denied or OS error for {subdir_path}. Skipping.")
                
    except (PermissionError, OSError):
        print(f"Permission denied or OS error for {directory}. Skipping.")

    return apps

def categorize_app(app_path):
    app_name = os.path.basename(app_path).lower()
    app_path_lower = app_path.lower()
    
    for category, keywords in categories.items():
        if any(keyword in app_name or keyword in app_path_lower for keyword in keywords):
            return category
    
    return 'Other'

def get_laptops_from_db():
    config = {
        'user': 'root',
        'password': 'pass',
        'host': 'localhost',
        'database': 'flaskapp'
    }
    
    query = """
        SELECT 
            product_id, product_name, brand, processor, graphics, 
            dimensions, weight, os, memory, storage, 
            power_supply, battery, price
        FROM product
    """
    
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    laptops = cursor.fetchall()
    conn.close()
    
    return laptops

def recommend_laptops(category_counts):
    laptops = get_laptops_from_db()
    
    category_priority = {
        'Productivity': 5,
        'Media': 4,
        'Development': 3,
        'Utilities': 2,
        'Games': 1,
        'Other': 0
    }
    
    recommendations = []
    
    for laptop in laptops:
        basic_score = sum(category_counts.get(category, 0) * category_priority.get(category, 0) for category in categories)
        
        score_adjustment = 0
        if 'gaming' in laptop['product_name'].lower():
            score_adjustment += 10  
        if 'productivity' in laptop['product_name'].lower():
            score_adjustment += 5 
        
        price = laptop['price']
        normalized_price = max(1, price / 1000)  
        final_score = basic_score + score_adjustment - normalized_price
        
        recommendations.append((laptop, final_score))
    
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    # Normalize the scores between 1 and 100
    max_score = recommendations[0][1]
    min_score = recommendations[-1][1]
    score_range = max_score - min_score

    for i in range(len(recommendations)):
        normalized_score = ((recommendations[i][1] - min_score) / score_range) * 99 + 1
        recommendations[i] = (recommendations[i][0], normalized_score)
    
    return recommendations[:30]  # Return top 30 recommendations

def save_recommendations_to_db(username, recommendations):
    config = {
        'user': 'root',
        'password': 'pass',
        'host': 'localhost',
        'database': 'flaskapp'
    }
    
    conn = None
    cursor = None
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Prepare the insert/update query
    # Assuming the upsert_query is defined somewhere above this code
    upsert_query = """
    INSERT INTO user_recommendations (
        username, product_id_1, score_1, product_id_2, score_2, product_id_3, score_3, 
        product_id_4, score_4, product_id_5, score_5, product_id_6, score_6, 
        product_id_7, score_7, product_id_8, score_8, product_id_9, score_9, 
        product_id_10, score_10, product_id_11, score_11, product_id_12, score_12, 
        product_id_13, score_13, product_id_14, score_14, product_id_15, score_15, 
        product_id_16, score_16, product_id_17, score_17, product_id_18, score_18, 
        product_id_19, score_19, product_id_20, score_20, product_id_21, score_21, 
        product_id_22, score_22, product_id_23, score_23, product_id_24, score_24, 
        product_id_25, score_25, product_id_26, score_26, product_id_27, score_27, 
        product_id_28, score_28, product_id_29, score_29, product_id_30, score_30, 
        last_updated
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, NOW()
    ) ON DUPLICATE KEY UPDATE 
        product_id_1 = VALUES(product_id_1), score_1 = VALUES(score_1),
        product_id_2 = VALUES(product_id_2), score_2 = VALUES(score_2),
        product_id_3 = VALUES(product_id_3), score_3 = VALUES(score_3),
        product_id_4 = VALUES(product_id_4), score_4 = VALUES(score_4),
        product_id_5 = VALUES(product_id_5), score_5 = VALUES(score_5),
        product_id_6 = VALUES(product_id_6), score_6 = VALUES(score_6),
        product_id_7 = VALUES(product_id_7), score_7 = VALUES(score_7),
        product_id_8 = VALUES(product_id_8), score_8 = VALUES(score_8),
        product_id_9 = VALUES(product_id_9), score_9 = VALUES(score_9),
        product_id_10 = VALUES(product_id_10), score_10 = VALUES(score_10),
        product_id_11 = VALUES(product_id_11), score_11 = VALUES(score_11),
        product_id_12 = VALUES(product_id_12), score_12 = VALUES(score_12),
        product_id_13 = VALUES(product_id_13), score_13 = VALUES(score_13),
        product_id_14 = VALUES(product_id_14), score_14 = VALUES(score_14),
        product_id_15 = VALUES(product_id_15), score_15 = VALUES(score_15),
        product_id_16 = VALUES(product_id_16), score_16 = VALUES(score_16),
        product_id_17 = VALUES(product_id_17), score_17 = VALUES(score_17),
        product_id_18 = VALUES(product_id_18), score_18 = VALUES(score_18),
        product_id_19 = VALUES(product_id_19), score_19 = VALUES(score_19),
        product_id_20 = VALUES(product_id_20), score_20 = VALUES(score_20),
        product_id_21 = VALUES(product_id_21), score_21 = VALUES(score_21),
        product_id_22 = VALUES(product_id_22), score_22 = VALUES(score_22),
        product_id_23 = VALUES(product_id_23), score_23 = VALUES(score_23),
        product_id_24 = VALUES(product_id_24), score_24 = VALUES(score_24),
        product_id_25 = VALUES(product_id_25), score_25 = VALUES(score_25),
        product_id_26 = VALUES(product_id_26), score_26 = VALUES(score_26),
        product_id_27 = VALUES(product_id_27), score_27 = VALUES(score_27),
        product_id_28 = VALUES(product_id_28), score_28 = VALUES(score_28),
        product_id_29 = VALUES(product_id_29), score_29 = VALUES(score_29),
        product_id_30 = VALUES(product_id_30), score_30 = VALUES(score_30),
        last_updated = NOW()
    """

    # Prepare the values
    values = [username]
    for i in range(30):
        if i < len(recommendations):
            laptop, score = recommendations[i]
            values.extend([laptop['product_id'], score])
        else:
            values.extend([None, None])

    # Ensure we have the correct number of values
    if len(values) != 61:
        raise ValueError(f"Expected 61 values, but got {len(values)}")

    try:
        # Execute the upsert query
        cursor.execute(upsert_query, tuple(values))
        conn.commit()
        print(f"Recommendations for {username} saved to database.")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        if conn:
            conn.rollback()
    except ValueError as err:
        print(f"Value error: {err}")

        print("Recommendations saved to database.")

def main():
    program_files_dirs = [
        r"C:\Program Files",
        r"C:\Program Files (x86)"
    ]
    
    categorized_apps = {category: 0 for category in categories}
    categorized_apps['Other'] = 0
    
    for directory in program_files_dirs:
        if os.path.exists(directory):
            apps_in_dir = detect_top_level_apps(directory)
            for app in apps_in_dir:
                category = categorize_app(app)
                categorized_apps[category] += 1
    
    username = "user1"  # Replace with the actual username
    
    recommendations = recommend_laptops(categorized_apps)
    save_recommendations_to_db(username, recommendations)
    
    print("Recommendations saved to database.")

if __name__ == "__main__":
    main()
