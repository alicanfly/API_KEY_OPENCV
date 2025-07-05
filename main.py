import cv2
import numpy as np
import streamlit as st
from tensorflow.kera.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)
from PIL import Image

def load_model():
    model = MobileNetV2(weights='imagenet')
    return model

def preprecess_image(image):
    img = np.array(image)   
    img = cv2.resize(img, (224, 224))
    img = preprocess_input(img)
    img = np.expand_dims(image, axis=0)
    
    return img


def classify_image(model, image):
    try:
        preprocessed_image = preprecess_image(image)
        predictions = model.predict(preprocessed_image)
        decoded_predictions = decode_predictions(predictions, top=3)[0]
    
        return decoded_predictions
    
    except Exception as e:
        st.error(f"Error during image classification: {str(e)}")
        return None


def main():
    st.set_page_config(page_title="AI Image Classifier", page_icon="📄", layout="centered")
    st.title("AI Image Classifier")
    st.write("Upload an image and let AI tell you what is in it.")

    @st.cache_resource
    def load_cached_model():
        return load_model()    
    
    model = load_cached_model()

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = st.image(
            uploaded_file,
            caption='Uploaded Image.',
            use_column_width=True
        )
        btn = st.button("Classify Image")

        if btn:
            with st.spinner("Analyze Image..."):
                immage = Image.open(uploaded_file)
                predictions = classify_image(model, image)

                if predictions:
                    st.write("Predictions:")
                    for _, label, score in predictions:
                        st.write(f"**{label}**: {score:.2%}")

if __name__ == "__main__":
    main()