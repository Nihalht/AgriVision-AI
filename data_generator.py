import pandas as pd
import numpy as np
import random

def generate_crop_data(num_samples=2200):
    # Crops: Rice, Maize, Chickpea, Kidneybeans, Pigeonpeas, Mothbeans, Mungbean, Blackgram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, Coffee
    crops = {
        'rice': {'N': (60, 90), 'P': (35, 60), 'K': (35, 45), 'temp': (20, 27), 'humidity': (80, 85), 'ph': (6, 7), 'rain': (200, 300)},
        'maize': {'N': (60, 100), 'P': (40, 60), 'K': (15, 25), 'temp': (18, 27), 'humidity': (50, 70), 'ph': (5.5, 7.0), 'rain': (60, 110)},
        'chickpea': {'N': (20, 60), 'P': (55, 80), 'K': (75, 85), 'temp': (17, 20), 'humidity': (14, 18), 'ph': (5.5, 6.0), 'rain': (60, 90)},
        'kidneybeans': {'N': (10, 40), 'P': (55, 80), 'K': (15, 25), 'temp': (15, 25), 'humidity': (18, 25), 'ph': (5.5, 6.0), 'rain': (60, 150)},
        'pigeonpeas': {'N': (10, 40), 'P': (55, 80), 'K': (15, 25), 'temp': (18, 38), 'humidity': (14, 18), 'ph': (4.5, 7.5), 'rain': (90, 155)},
        'mothbeans': {'N': (10, 40), 'P': (35, 60), 'K': (15, 25), 'temp': (24, 32), 'humidity': (40, 65), 'ph': (3.5, 9.5), 'rain': (30, 80)},
        'mungbean': {'N': (10, 40), 'P': (35, 60), 'K': (15, 25), 'temp': (27, 30), 'humidity': (60, 65), 'ph': (6.0, 7.2), 'rain': (35, 60)},
        'blackgram': {'N': (20, 60), 'P': (55, 80), 'K': (15, 25), 'temp': (25, 35), 'humidity': (60, 70), 'ph': (6.5, 7.5), 'rain': (60, 80)},
        'lentil': {'N': (10, 40), 'P': (55, 80), 'K': (15, 25), 'temp': (18, 30), 'humidity': (60, 70), 'ph': (5.5, 6.5), 'rain': (35, 55)},
        'pomegranate': {'N': (10, 50), 'P': (10, 40), 'K': (35, 45), 'temp': (18, 25), 'humidity': (85, 95), 'ph': (5.5, 7.2), 'rain': (100, 115)},
        'banana': {'N': (80, 120), 'P': (70, 95), 'K': (45, 55), 'temp': (25, 30), 'humidity': (75, 85), 'ph': (5.5, 6.5), 'rain': (90, 120)},
        'mango': {'N': (10, 40), 'P': (15, 40), 'K': (25, 35), 'temp': (27, 35), 'humidity': (45, 55), 'ph': (4.5, 7.0), 'rain': (85, 100)},
        'grapes': {'N': (10, 50), 'P': (120, 145), 'K': (195, 205), 'temp': (10, 40), 'humidity': (80, 83), 'ph': (5.5, 6.5), 'rain': (65, 75)},
        'watermelon': {'N': (80, 120), 'P': (5, 30), 'K': (45, 55), 'temp': (24, 27), 'humidity': (80, 90), 'ph': (6.0, 7.0), 'rain': (40, 60)},
        'muskmelon': {'N': (80, 120), 'P': (5, 30), 'K': (45, 55), 'temp': (27, 30), 'humidity': (90, 95), 'ph': (6.0, 6.8), 'rain': (20, 30)},
        'apple': {'N': (10, 50), 'P': (120, 145), 'K': (195, 205), 'temp': (21, 24), 'humidity': (90, 95), 'ph': (5.5, 6.5), 'rain': (100, 120)},
        'orange': {'N': (10, 40), 'P': (5, 30), 'K': (5, 15), 'temp': (10, 35), 'humidity': (90, 95), 'ph': (6.0, 8.0), 'rain': (100, 120)},
        'papaya': {'N': (30, 70), 'P': (45, 70), 'K': (45, 55), 'temp': (23, 44), 'humidity': (90, 95), 'ph': (6.5, 7.0), 'rain': (40, 250)},
        'coconut': {'N': (10, 40), 'P': (5, 30), 'K': (25, 35), 'temp': (25, 28), 'humidity': (90, 95), 'ph': (5.5, 6.5), 'rain': (150, 230)},
        'cotton': {'N': (100, 140), 'P': (35, 60), 'K': (15, 25), 'temp': (22, 26), 'humidity': (75, 85), 'ph': (6.0, 8.0), 'rain': (60, 100)},
        'jute': {'N': (60, 100), 'P': (35, 60), 'K': (35, 45), 'temp': (23, 26), 'humidity': (70, 80), 'ph': (6.0, 7.5), 'rain': (150, 200)},
        'coffee': {'N': (80, 120), 'P': (15, 40), 'K': (25, 35), 'temp': (23, 28), 'humidity': (50, 70), 'ph': (6.0, 7.5), 'rain': (115, 200)}
    }

    data = []
    samples_per_crop = num_samples // len(crops)
    
    for crop, params in crops.items():
        for _ in range(samples_per_crop):
            row = {
                'N': int(np.random.normal((params['N'][0] + params['N'][1])/2, (params['N'][1] - params['N'][0])/6)),
                'P': int(np.random.normal((params['P'][0] + params['P'][1])/2, (params['P'][1] - params['P'][0])/6)),
                'K': int(np.random.normal((params['K'][0] + params['K'][1])/2, (params['K'][1] - params['K'][0])/6)),
                'temperature': round(np.random.uniform(params['temp'][0], params['temp'][1]), 2),
                'humidity': round(np.random.uniform(params['humidity'][0], params['humidity'][1]), 2),
                'ph': round(np.random.uniform(params['ph'][0], params['ph'][1]), 2),
                'rainfall': round(np.random.uniform(params['rain'][0], params['rain'][1]), 2),
                'label': crop
            }
            # Clip values to be realistic
            row['N'] = max(0, row['N'])
            row['P'] = max(0, row['P'])
            row['K'] = max(0, row['K'])
            data.append(row)
            
    df = pd.DataFrame(data)
    df.to_csv('crop_recommendation.csv', index=False)
    print("Generated crop_recommendation.csv")

def generate_fertilizer_data(num_samples=1000):
    # Fertilizer: Urea, DAP, 14-35-14, 28-28, 17-17-17, 20-20, 10-26-26
    # Features: Temperature, Humidity, Moisture, Soil Type, Crop Type, Nitrogen, Potassium, Phosphorous
    
    # Soil types: Sandy, Loamy, Black, Red, Clayey
    # Crop types: Maize, Sugarcane, Cotton, Tobacco, Paddy, Barley, Wheat, Millets, Oil seeds, Pulses, Ground Nuts
    
    fertilizers = ['Urea', 'DAP', '14-35-14', '28-28', '17-17-17', '20-20', '10-26-26']
    soil_types = ['Sandy', 'Loamy', 'Black', 'Red', 'Clayey']
    
    data = []
    for _ in range(num_samples):
        temp = np.random.randint(25, 40)
        humidity = np.random.randint(50, 85)
        moisture = np.random.randint(25, 65)
        soil_type = random.choice(soil_types)
        
        # Simplified logic for synthetic purpose, relating NPK loosely to fertilizer content
        # Real-world logic would be more complex based on soil deficiency
        
        # Target Fertilizer
        fert = random.choice(fertilizers)
        
        # Generate NPK based on fertilizer (reverse engineering for synthetic data)
        if fert == 'Urea': # High N
            N = np.random.randint(30, 60) # Soil needs N
            P = np.random.randint(0, 30)
            K = np.random.randint(0, 30)
        elif fert == 'DAP': # Needs P
            N = np.random.randint(0, 30)
            P = np.random.randint(30, 60)
            K = np.random.randint(0, 30)
        elif fert == '14-35-14':
            N = np.random.randint(10, 20)
            P = np.random.randint(30, 40)
            K = np.random.randint(10, 20)
        elif fert == '28-28':
            N = np.random.randint(20, 30)
            P = np.random.randint(20, 30)
            K = np.random.randint(0, 10)
        elif fert == '17-17-17':
            N = np.random.randint(10, 25)
            P = np.random.randint(10, 25)
            K = np.random.randint(10, 25)
        elif fert == '20-20':
            N = np.random.randint(15, 25)
            P = np.random.randint(15, 25)
            K = np.random.randint(0, 10)
        elif fert == '10-26-26':
            N = np.random.randint(5, 15)
            P = np.random.randint(20, 30)
            K = np.random.randint(20, 30)
            
        # Random crop type (less important for this synthetic generation but needed for model)
        crop_type = random.choice(['Maize', 'Sugarcane', 'Cotton', 'Tobacco', 'Paddy', 'Barley', 'Wheat', 'Millets', 'Oil seeds', 'Pulses', 'Ground Nuts'])

        data.append({
            'Temperature': temp,
            'Humidity': humidity,
            'Moisture': moisture,
            'Soil Type': soil_type,
            'Crop Type': crop_type,
            'Nitrogen': N,
            'Potassium': K,
            'Phosphorous': P,
            'Fertilizer Name': fert
        })
        
    df = pd.DataFrame(data)
    df.to_csv('fertilizer_recommendation.csv', index=False)
    print("Generated fertilizer_recommendation.csv")

if __name__ == "__main__":
    generate_crop_data()
    generate_fertilizer_data()
