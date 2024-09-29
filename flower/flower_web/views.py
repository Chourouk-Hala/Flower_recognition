import os
import io
import json
import numpy as np
from PIL import Image
from django.shortcuts import render
from django.http import HttpResponse
from tensorflow import keras
import tensorflow_hub as hub
import tensorflow as tf

# Load class names from JSON
with open(os.path.join(os.path.dirname(__file__), 'cat_to_name.json'), 'r') as f:
    cat_to_name = json.load(f)

# Function to load the Keras model
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), 'final_model_FOR_REAL.h5')
    custom_objects = {'KerasLayer': hub.KerasLayer}
    print(f"Loading model from: {model_path}")  
    return keras.models.load_model(model_path, custom_objects=custom_objects)

# Load the model when the file is imported
model = load_model()

# Define a predict function
def prediction(image: np.ndarray) -> int:
    image = Image.fromarray(image)
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)

    # Make the prediction using the model
    predictions = model.predict(image)
    _, image_idx = tf.math.top_k(predictions, 1)
    return int(image_idx.numpy()[0])  # Convert to Python int

# Define the index view
def index(request):
    return render(request, "flower_web/index.html", {"class_idx": None, "class_name": None})

# Define the prediction view
def make_prediction(request):
    if request.method == "POST":
        try:
            # Get the uploaded image
            image_file = request.FILES['image']  
            image_file = Image.open(image_file)

            # Convert image to numpy array and preprocess if necessary
            image_file = np.array(image_file)

            # Make the prediction using the predict function
            index = prediction(image_file)

            class_idx = cat_to_name.get(str(index + 1))  # Get class name safely
            class_name = request.POST.get('real_class')

            # Render the template with the predicted class value
            return render(request, "flower_web/index.html", {
                "class_idx": class_idx, 
                "class_name": class_name
            })

        except Exception as e:
            return render(request, "flower_web/index.html", {
                "error": str(e)
            })