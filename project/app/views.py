import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from .forms import RentalPriceForm
import re
def extract_floor_info(floor_str):
    try:
        match = re.match(r'(?P<floor_number>-?\d+)(?:st|nd|rd|th)?(?: floor| of (?P<total_floors>\d+))?', floor_str, re.IGNORECASE)
        
        if match:
            floor_number = int(match.group('floor_number'))
            total_floors = match.group('total_floors')
            total_floors = int(total_floors) if total_floors else None
            return floor_number, total_floors
        
        
        if 'Ground' in floor_str:
            return 0, None  
        elif 'Upper Basement' in floor_str:
            return -1, None  
        elif 'Lower Basement' in floor_str:
            return -2, None  
        else:
            return None, None  
    except (ValueError, TypeError):
        return None, None

def load_and_preprocess_data():
    # Load the dataset from the static folder
    file_path = os.path.join(settings.BASE_DIR, 'static/app/data/House_Rent_Dataset.csv')
    data = pd.read_csv(file_path)

    # Preprocessing
    data['Posted On'] = pd.to_datetime(data['Posted On'], format='%Y-%m-%d')
    data['Year']=data['Posted On'].dt.year
    
    data = data.drop('Posted On', axis=1)  

    data['Current Floor'], data['Total Floors'] = zip(*data['Floor'].apply(extract_floor_info))

    data = data.drop('Floor', axis=1)

    return data

def predict_rent(request):
    if request.method == 'POST':
        form=RentalPriceForm(request.POST)

        data = load_and_preprocess_data()

        features = ['Year','BHK', 'Size','Area Locality', 'City', 'Furnishing Status',
            'Bathroom','Current Floor']
        target = 'Rent'
        data=data.drop("Total Floors",axis=1)
        data=data.drop("Tenant Preferred",axis=1)
        data=data.drop("Point of Contact",axis=1)
        data=data.drop("Area Type",axis=1)

        X = data[features]
        y = data[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        numerical_cols = ['BHK', 'Size', 'Current Floor','Bathroom','Year']
        categorical_cols = [ 'Area Locality', 'City', 'Furnishing Status']

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', SimpleImputer(strategy='mean'), numerical_cols),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
            ]
        )

        from sklearn.ensemble import RandomForestRegressor
        model_pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', RandomForestRegressor())
        ])
        model_pipeline.fit(X_train, y_train)

        if form.is_valid():
            BHK = form.cleaned_data['bhk']
            Size = form.cleaned_data['size']
            Area_Locality = form.cleaned_data['area_locality']
            City = form.cleaned_data['city']
            Furnishing_Status = form.cleaned_data['furnished_status']
            Current_Floor = int(form.cleaned_data['current_floor'])
            Bathrooms=int(form.cleaned_data["bathrooms"])
            year=int(form.cleaned_data['year'])

            user_input = pd.DataFrame({
                'Year':[year],
                'BHK': [BHK],
                'Size': [Size],
                'Area Locality': [Area_Locality],
                'City': [City],
                'Furnishing Status': [Furnishing_Status],
                'Current Floor': [Current_Floor],
                "Bathroom":[Bathrooms]
            })

            predicted_rent = model_pipeline.predict(user_input)[0]
            return render(request, 'app/index.html', {"form": form,"predicted_rent":predicted_rent,'values':{"year":year,"bhk":BHK,"size":Size,"area_locality":Area_Locality,"city":City,"furnished_status":Furnishing_Status,"current_floor":Current_Floor,"bathrooms":Bathrooms}})


        
    else:
        form=RentalPriceForm(request.GET)

    return render(request, 'app/index.html',{"form":form})
