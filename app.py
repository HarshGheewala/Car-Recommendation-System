import pandas as pd
import streamlit as st
import pickle


#for design and feature based
car_dict1 = pickle.load(open("Features.pkl","rb"))
Improved = pickle.load(open("ImprovedDesign.pkl","rb"))

#for Pure Design
design = pickle.load(open("design_similarity.pkl","rb"))

#for Pure Features
feature = pickle.load(open("Feature_similarity.pkl","rb"))

#for performance based
car_dict2 = pickle.load(open("Performance.pkl","rb"))
distance_matrix = pickle.load(open("distancematrix.pkl","rb"))

CarsBasedOnDesign = pd.DataFrame(car_dict1)
CarsBasedOnPerformance = pd.DataFrame(car_dict2)

CarsBasedOnDesign["Price Range"] = CarsBasedOnDesign["Price Range"].apply(lambda x : x.replace("Rs.","").strip())
CarsBasedOnPerformance["Price Range"] = CarsBasedOnPerformance["Price Range"].apply(lambda x : x.replace("Rs.","").strip())


def recommendCarsBasedOnDesignAndFeature(car):
    car_index = CarsBasedOnDesign[CarsBasedOnDesign["Car Model"] == car].index[0]
    distances = Improved[car_index]
    carsList = sorted(list(enumerate(distances)),reverse=True, key = lambda x:x[1])[1:6] 
    
    recommended_Cars = []
    image = []
    price = []
    for i in carsList:
        recommended_Cars.append(CarsBasedOnDesign["Car Model"].iloc[i[0]])
        image.append(CarsBasedOnDesign["Image"].iloc[i[0]])
        price.append(CarsBasedOnDesign["Price Range"].iloc[i[0]])
    return recommended_Cars,image,price


def recommendCarsBasedOnPerformance(car):
    car_index = CarsBasedOnPerformance[CarsBasedOnPerformance["Car Model"] == car].index[0]
    distances = distance_matrix[car_index]
    carsList = sorted(list(enumerate(distances)),reverse=False, key = lambda x:x[1])[1:6] 
    
    recommended_Cars = []
    image = []
    price = []
    for i in carsList:
        recommended_Cars.append(CarsBasedOnPerformance["Car Model"].iloc[i[0]])
        image.append(CarsBasedOnPerformance["Image"].iloc[i[0]])
        price.append(CarsBasedOnPerformance["Price Range"].iloc[i[0]])
    return recommended_Cars,image,price


def recommendCarsBasedOnDesign(car):
    car_index = CarsBasedOnDesign[CarsBasedOnDesign["Car Model"] == car].index[0]
    distances = design[car_index]
    carsList = sorted(list(enumerate(distances)),reverse=True, key = lambda x:x[1])[1:6] 
    
    recommended_Cars = []
    image = []
    price = []
    for i in carsList:
        recommended_Cars.append(CarsBasedOnDesign["Car Model"].iloc[i[0]])
        image.append(CarsBasedOnDesign["Image"].iloc[i[0]])
        price.append(CarsBasedOnDesign["Price Range"].iloc[i[0]])
    return recommended_Cars,image,price


def recommendCarsBasedOnFeatures(car):
    car_index = CarsBasedOnDesign[CarsBasedOnDesign["Car Model"] == car].index[0]
    distances = feature[car_index]
    carsList = sorted(list(enumerate(distances)),reverse=True, key = lambda x:x[1])[1:6] 
    
    recommended_Cars = []
    image = []
    price = []
    for i in carsList:
        recommended_Cars.append(CarsBasedOnDesign["Car Model"].iloc[i[0]])
        image.append(CarsBasedOnDesign["Image"].iloc[i[0]])
        price.append(CarsBasedOnDesign["Price Range"].iloc[i[0]])
    return recommended_Cars,image,price


st.title("Car Recommendation System")

selected_car = st.selectbox("Please Select the car",
                       CarsBasedOnDesign["Car Model"].values)

selected_choice = st.selectbox("Please select your Priority",
                       ["Design and Features","Design","Features","Performance"])

if st.button("Recommend"):
    if (selected_choice == "Design"):
        names,images,prices = recommendCarsBasedOnDesign(selected_car)
    elif (selected_choice == "Design and Features"):
        names,images,prices = recommendCarsBasedOnDesignAndFeature(selected_car)
    elif (selected_choice == "Features"):
        names,images,prices = recommendCarsBasedOnFeatures(selected_car)
    else:
        names,images,prices = recommendCarsBasedOnPerformance(selected_car)

    
    cols = st.columns(5)

    st.markdown("""
        <style>
        .car-container {
            text-align: center;
            height: 250px;
        }
        .car-image {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        .car-name {
            height: 50px
        }
        .car-price {
            white-space: nowrap;
            margin-bottom: -30px;
        }
        </style>
    """, unsafe_allow_html=True)

    for col, name, image, price in zip(cols, names, images, prices):
        col.markdown(f'''
            <div class="car-container">
                <img src="{image}" class="car-image"/>
                <p class="car-name">{name}</p>
                <p class="car-price">\u20B9 {price}</p>
            </div>
            ''', unsafe_allow_html=True)
