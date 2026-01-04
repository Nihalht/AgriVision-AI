from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load Models
def load_models():
    models = {}
    try:
        with open('models/crop_model.pkl', 'rb') as f:
            models['crop'] = pickle.load(f)
        with open('models/crop_label_encoder.pkl', 'rb') as f:
            models['crop_le'] = pickle.load(f)
        with open('models/fertilizer_model.pkl', 'rb') as f:
            models['fert'] = pickle.load(f)
        with open('models/fertilizer_label_encoder.pkl', 'rb') as f:
            models['fert_le'] = pickle.load(f)
        with open('models/input_encoders.pkl', 'rb') as f:
            models['input_les'] = pickle.load(f)
    except Exception as e:
        print(f"Error loading models: {e}")
    return models

models = load_models()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crop')
def crop():
    return render_template('crop.html')

@app.route('/fertilizer')
def fertilizer():
    return render_template('fertilizer.html')

@app.route('/predict-crop', methods=['POST'])
def predict_crop():
    try:
        data = request.json
        
        # Validation
        validate_input(data, 'crop')

        features = [
            data['N'], data['P'], data['K'], 
            data['temperature'], data['humidity'], data['ph'], data['rainfall']
        ]
        
        prediction = models['crop'].predict([features])
        predicted_crop = models['crop_le'].inverse_transform(prediction)[0]
        
        # Generate detailed info
        info = get_crop_details(predicted_crop, data)
        
        return jsonify({
            'prediction': predicted_crop,
            'description': info['desc'],
            'yield_outcome': info['yield'],
            'link': info['link']
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/predict-fertilizer', methods=['POST'])
def predict_fertilizer():
    try:
        data = request.json
        
        # Validation
        validate_input(data, 'fertilizer')

        soil_type = models['input_les']['soil'].transform([data['Soil Type']])[0]
        crop_type = models['input_les']['crop'].transform([data['Crop Type']])[0]
        
        features = [
            data['Temperature'], data['Humidity'], data['Moisture'], 
            soil_type, crop_type, 
            data['Nitrogen'], data['Potassium'], data['Phosphorous']
        ]
        
        prediction = models['fert'].predict([features])
        predicted_fert = models['fert_le'].inverse_transform(prediction)[0]
        
        # Generate detailed info
        info = get_fertilizer_details(predicted_fert, data)
        
        return jsonify({
            'prediction': predicted_fert,
            'description': info['desc'],
            'yield_outcome': info['yield'],
            'link': info['link']
        })
    except Exception as e:
        return jsonify({'error': str(e)})

def validate_input(data, form_type):
    # Common checks
    if 'temperature' in data and (data['temperature'] > 60 or data['temperature'] < -10):
        raise ValueError(f"🌡️ Temperature {data['temperature']}°C is too extreme for agriculture! Most crops die above 50°C.")
    if 'Temperature' in data and (data['Temperature'] > 60 or data['Temperature'] < -10):
         raise ValueError(f"🌡️ Temperature {data['Temperature']}°C is too extreme for agriculture! Most crops die above 50°C.")

    if 'humidity' in data and (data['humidity'] < 0 or data['humidity'] > 100):
        raise ValueError(f"💧 Humidity {data['humidity']}% is physically impossible. It must be between 0% and 100%.")
    if 'Humidity' in data and (data['Humidity'] < 0 or data['Humidity'] > 100):
        raise ValueError(f"💧 Humidity {data['Humidity']}% is physically impossible. It must be between 0% and 100%.")
        
    if 'ph' in data and (data['ph'] < 0 or data['ph'] > 14):
        raise ValueError(f"🧪 pH {data['ph']} is chemically impossible! The scale ranges from 0 to 14.")
        
    # Crop specific
    if form_type == 'crop':
        if data['N'] > 200: raise ValueError("⚠️ Nitrogen levels over 200 are toxic to most plants.")
        if data['P'] > 200: raise ValueError("⚠️ Phosphorous levels over 200 can lock up other nutrients.")
        if data['K'] > 250: raise ValueError("⚠️ Potassium levels over 250 are unusually high.")
        if data['rainfall'] < 0: raise ValueError("☔ Rainfall cannot be negative. Are you in a reverse dimension?")
        
    # Fertilizer specific
    if form_type == 'fertilizer':
        if data['Nitrogen'] > 200: raise ValueError("⚠️ Soil Nitrogen is already dangerously high.")
        if data['moisture'] if 'moisture' in data else data.get('Moisture', 0) < 0:
             raise ValueError("💧 Moisture cannot be negative.")

def get_crop_details(crop, data):
    # Dynamic analysis based on inputs
    analysis = []
    if data['N'] > 100: analysis.append("High Nitrogen levels detected.")
    elif data['N'] < 20: analysis.append("Nitrogen levels are low.")
    
    if data['rainfall'] > 200: analysis.append("Heavy rainfall region suitable for water-intensive crops.")
    elif data['rainfall'] < 50: analysis.append("Low rainfall region, drought-resistant qualities needed.")
    
    cond_str = " ".join(analysis) if analysis else "Soil and climate conditions are balanced."

    details = {
        'rice': {
            'desc': f"Rice is a staple food crop. {cond_str} It thrives in these high-humidity conditions. Ensure standing water is maintained during the vegetative stage to suppress weeds and ensure optimal growth.",
            'yield': 'Expected Yield: 4-5 tons/hectare under optimal management.',
            'link': 'https://kare.fa.org/crops/rice' 
        },
        'maize': {
            'desc': f"Maize is a versatile cereal crop. {cond_str} Your soil pH is suitable. Ensure proper drainage to prevent waterlogging, which maize is sensitive to.",
            'yield': 'Expected Yield: 5-7 tons/hectare.',
            'link': 'https://kare.fa.org/crops/maize'
        },
        'chickpea': {
            'desc': f"Chickpea is a protein-rich pulse. {cond_str} It requires less water, making it perfect for your current moisture levels. Avoid excessive irrigation at flowering.",
            'yield': 'Expected Yield: 1.5-2 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Chickpea'
        },
        'kidneybeans': {
            'desc': f"Kidney beans require well-drained loamy soil. {cond_str} This crop fixes atmospheric nitrogen, improving your soil health for future rotations.",
            'yield': 'Expected Yield: 1.2-1.5 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Kidney_bean'
        },
        'pigeonpeas': {
            'desc': f"Pigeon peas are drought-tolerant. {cond_str} They have a deep root system that helps break hard soil pans. Excellent for intercropping.",
            'yield': 'Expected Yield: 1-1.5 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Pigeon_pea'
        },
        'mothbeans': {
            'desc': f"Moth beans are extremely drought-resistant. {cond_str} They provide great ground cover, preventing soil erosion in your field.",
            'yield': 'Expected Yield: 0.5-0.8 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Vigna_aconitifolia'
        },
        'mungbean': {
            'desc': f"Mungbean is a short-duration crop. {cond_str} It fits well in crop rotation. Ensure harvest is done before shattering of pods.",
            'yield': 'Expected Yield: 1-1.2 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Mung_bean'
        },
        'blackgram': {
            'desc': f"Blackgram improves soil fertility. {cond_str} It is sensitive to waterlogging, so ensure drainage is adequate given your rainfall.",
            'yield': 'Expected Yield: 0.8-1.0 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Vigna_mungo'
        },
        'lentil': {
            'desc': f"Lentils prefer cool climates. {cond_str} They are best sown after the rainy season. Requires minimal fertigation due to nitrogen fixation.",
            'yield': 'Expected Yield: 1-1.5 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Lentil'
        },
        'pomegranate': {
            'desc': f"Pomegranate is a high-value fruit crop. {cond_str} It requires regular irrigation but cannot tolerate standing water. Pruning is essential for quality fruit.",
            'yield': 'Expected Yield: 10-12 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Pomegranate'
        },
        'banana': {
            'desc': f"Banana is moisture-loving and requires high nutrients. {cond_str} Your high rainfall or irrigation capacity is key here. Protect from strong winds.",
            'yield': 'Expected Yield: 30-40 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Banana'
        },
        'mango': {
            'desc': f"Mango is the king of fruits. {cond_str} Deep, well-drained soil is ideal. Requires a dry spell during flowering for good fruit set.",
            'yield': 'Expected Yield: 8-10 tons/hectare (after full establishment).',
            'link': 'https://en.wikipedia.org/wiki/Mango'
        },
        'grapes': {
            'desc': f"Grapes require careful pruning and training. {cond_str} They are sensitive to high humidity which causes diseases, so manage canopy air circulation well.",
            'yield': 'Expected Yield: 20-25 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Grape'
        },
        'watermelon': {
            'desc': f"Watermelon thrives in warm, dry climates. {cond_str} Sandy loam soil is best for root development. Requires frequent irrigation during early growth.",
            'yield': 'Expected Yield: 25-30 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Watermelon'
        },
        'muskmelon': {
            'desc': f"Muskmelon requires plenty of heat. {cond_str} High humidity can reduce sweetness, so ensure harvest is during dry weather.",
            'yield': 'Expected Yield: 15-20 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Muskmelon'
        },
        'apple': {
            'desc': f"Apples require chilling hours to fruit. {cond_str} Suitable for cooler high-altitude regions. Ensure pollinators like bees are present.",
            'yield': 'Expected Yield: 10-15 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Apple'
        },
        'orange': {
            'desc': f"Oranges need well-drained soil. {cond_str} They are sensitive to waterlogging. Regular micronutrient sprays will enhance fruit quality.",
            'yield': 'Expected Yield: 15-20 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Orange_(fruit)'
        },
        'papaya': {
            'desc': f"Papaya is a fast-growing fruit crop. {cond_str} Highly sensitive to frost and waterlogging. Provides quick returns compared to other orchards.",
            'yield': 'Expected Yield: 40-50 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Papaya'
        },
        'coconut': {
            'desc': f"Coconut thrives in humid coastal climates. {cond_str} Requires consistent moisture. Mulching is highly recommended to retain soil humidity.",
            'yield': 'Expected Yield: 10,000-14,000 nuts/hectare/year.',
            'link': 'https://en.wikipedia.org/wiki/Coconut'
        },
        'cotton': {
            'desc': f"Cotton is a major fiber crop. {cond_str} Requires a long frost-free period. Pest management (bollworm) is critical for yield.",
            'yield': 'Expected Yield: 2-3 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Cotton'
        },
        'jute': {
            'desc': f"Jute requires a hot and humid climate. {cond_str} It is a rain-fed crop. Retting water availability is crucial for fiber extraction after harvest.",
            'yield': 'Expected Yield: 2.5-3 tons/hectare.',
            'link': 'https://en.wikipedia.org/wiki/Jute'
        },
        'coffee': {
            'desc': f"Coffee grows well in shade. {cond_str} Acidic soil conditions are preferred. Requires pruning to maintain bush shape and facilitate picking.",
            'yield': 'Expected Yield: 0.8-1.2 tons/hectare (clean coffee).',
            'link': 'https://en.wikipedia.org/wiki/Coffee'
        }
    }
    
    # Default fallback
    default = {
        'desc': f"This crop is suitable for your provided conditions: {cond_str}. Ensure standard agricultural practices for your region.",
        'yield': 'Yield varies based on management.',
        'link': 'https://en.wikipedia.org/wiki/Agriculture'
    }
    
    return details.get(crop, default)

def get_fertilizer_details(fert, data):
    analysis = f"Given your soil is {data.get('Soil Type', 'varied')} and you are growing {data.get('Crop Type', 'crops')},"
    
    details = {
        'Urea': {
            'desc': f"{analysis} your soil is highly deficient in Nitrogen. Urea provides 46% N, promoting vigorous leafy growth. Apply in split doses to reduce leaching losses.",
            'yield': 'significantly improves vegetative growth.',
            'link': 'https://en.wikipedia.org/wiki/Urea#Agriculture'
        },
        'DAP': {
            'desc': f"{analysis} Di-Ammonium Phosphate supplies both N and high P. Essential for root development and early plant establishment. Best applied basally at sowing.",
            'yield': 'Enhances root establishment and flowering.',
            'link': 'https://en.wikipedia.org/wiki/Diammonium_phosphate'
        },
        '14-35-14': {
            'desc': f"{analysis} this complex fertilizer provides balanced nutrition with high Phosphorus. Good for root crops and pulses initial growth stages.",
            'yield': 'Balanced growth support.',
            'link': 'https://en.wikipedia.org/wiki/Fertilizer'
        },
        '28-28': {
            'desc': f"{analysis} this complex fertilizer provides equal high amounts of N and P. Suitable for top dressing in crops requiring vegetative and root boost.",
            'yield': 'Boosts both foliage and root systems.',
            'link': 'https://en.wikipedia.org/wiki/Fertilizer'
        },
        '17-17-17': {
            'desc': f"{analysis} this is a balanced NPK fertilizer. It corrects general deficiencies in all three major nutrients, ensuring uniform crop health.",
            'yield': 'Supports overall plant health and metabolic functions.',
            'link': 'https://en.wikipedia.org/wiki/NPK_fertilizer'
        },
        '20-20': {
            'desc': f"{analysis} supplies Nitrogen and Phosphorus. Often called Ammonium Phosphate Sulfate. Good for sulfur-loving crops like oilseeds if it contains S.",
            'yield': 'Improves protein content and growth.',
            'link': 'https://en.wikipedia.org/wiki/Fertilizer'
        },
        '10-26-26': {
            'desc': f"{analysis} high in Phosphorus and Potassium. Ideal for flowering and fruiting stages, and for root crops like potatoes. Low Nitrogen prevents excessive vegetative growth.",
            'yield': 'Maximizes fruit/grain quality and weight.',
            'link': 'https://en.wikipedia.org/wiki/Fertilizer'
        }
    }
    
    default = {
        'desc': f"{analysis} this fertilizer is recommended to balance your nutrient profile.",
        'yield': 'Optimizes nutrient availability.',
        'link': 'https://en.wikipedia.org/wiki/Fertilizer'
    }
    
    return details.get(fert, default)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
