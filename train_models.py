import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# Create models directory
if not os.path.exists('models'):
    os.makedirs('models')

def train_crop_model():
    print("Training Crop Model...")
    df = pd.read_csv('crop_recommendation.csv')
    
    X = df.drop('label', axis=1)
    y = df['label']
    
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Crop Model Accuracy: {acc * 100:.2f}%")
    
    with open('models/crop_model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    with open('models/crop_label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)
        
    print("Crop Model Saved.")

def train_fertilizer_model():
    print("\nTraining Fertilizer Model...")
    df = pd.read_csv('fertilizer_recommendation.csv')
    
    # Encoders for categorical inputs
    le_soil = LabelEncoder()
    df['Soil Type'] = le_soil.fit_transform(df['Soil Type'])
    
    le_crop = LabelEncoder()
    df['Crop Type'] = le_crop.fit_transform(df['Crop Type'])
    
    le_fert = LabelEncoder()
    df['Fertilizer Name'] = le_fert.fit_transform(df['Fertilizer Name'])
    
    X = df.drop('Fertilizer Name', axis=1)
    y = df['Fertilizer Name']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Fertilizer Model Accuracy: {acc * 100:.2f}%")
    
    with open('models/fertilizer_model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    with open('models/input_encoders.pkl', 'wb') as f:
        pickle.dump({'soil': le_soil, 'crop': le_crop}, f)
        
    with open('models/fertilizer_label_encoder.pkl', 'wb') as f:
        pickle.dump(le_fert, f)
        
    print("Fertilizer Model Saved.")

if __name__ == "__main__":
    train_crop_model()
    train_fertilizer_model()
