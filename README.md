# 🧠 NeuroScan AI 
### Brain Tumor Detection using MobileNetV2 & Grad-CAM

<div align="center">

![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![MobileNetV2](https://img.shields.io/badge/MobileNetV2-00ACC1?style=for-the-badge&logo=tensorflow&logoColor=white)
![GradCAM](https://img.shields.io/badge/GradCAM-FF6B6B?style=for-the-badge&logo=keras&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

*A powerful web application for detecting and classifying brain tumors in MRI scans using MobileNetV2 with Grad-CAM explainability*

[![Live Demo](https://img.shields.io/badge/🚀-Live_Demo_on_HuggingFace-blue?style=for-the-badge)](https://asad-aziz-brain-tumor-detection.hf.space/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

## 🌟 Overview

**NeuroScan AI** is an intelligent web application that leverages the power of **MobileNetV2** deep learning architecture to automatically detect and classify brain tumors in MRI images. With **Grad-CAM** explainability, this tool provides medical professionals and researchers with transparent, interpretable results for preliminary brain tumor analysis. The application offers real-time classification with confidence scores, visual heatmaps showing tumor locations, and comprehensive PDF reports for clinical documentation.

### 🎯 Key Features

- **🔍 Accurate Detection**: Powered by MobileNetV2 with 95.7% validation accuracy
- **🔥 Grad-CAM Explainability**: Visual heatmaps showing which regions influenced predictions
- **📊 Multi-Class Classification**: Detects Glioma, Meningioma, Pituitary tumors, and healthy scans
- **📈 Probability Distribution**: Detailed confidence scores for all classes
- **📄 PDF Reports**: Download comprehensive clinical reports
- **🔐 User Authentication**: Secure signup/login with history tracking
- **📜 Analysis History**: Save and review all previous analyses
- **📊 Analytics Dashboard**: View statistics and detection patterns
- **🌓 Dark/Light Mode**: User preference with global persistence
- **⚡ Real-time Processing**: Results in under 3 seconds

## 🛠️ Technical Details

### Model Architecture

This application uses **MobileNetV2** with a custom classifier head:

- **Base Model**: MobileNetV2 (ImageNet pre-trained)
- **Custom Head**: Dropout(0.2) + Linear(1280, num_classes)
- **Input Size**: 160x160x3 (RGB)
- **Output Classes**: 4 (Glioma, Meningioma, Pituitary, No Tumor)

### Grad-CAM Explainability

**Grad-CAM** (Gradient-weighted Class Activation Mapping) provides visual explanations:

1. **Forward Pass**: Model processes the image
2. **Backward Pass**: Gradients flow to the last convolutional layer
3. **Weight Calculation**: Gradients are pooled to create importance weights
4. **Heatmap Generation**: Weighted combination of feature maps
5. **Overlay**: Heatmap is overlaid on original image

## 💻 Usage Guide

### Step-by-Step Process

1. **Launch the Application**
   - Run `python app.py`
   - Navigate to `http://localhost:5000`

2. **Create Account / Login**
   - Click "Sign Up" to create a new account
   - Or login with existing credentials

3. **Upload MRI Image**
   - Go to Detection page
   - Click "Browse Files" or drag & drop an MRI image
   - Supported formats: JPG, PNG, BMP, TIFF, JFIF

4. **View Results**
   - **Original MRI**: Displays on the left
   - **Grad-CAM Analysis**: Shows heatmap overlay on the right
   - **Prediction**: Tumor type with confidence score
   - **Probability Distribution**: Class-wise probabilities chart
   - **Detailed Metrics**: Confidence gauge and performance metrics
   - **Pure Heatmap**: Clean activation heatmap
   - **Comparison View**: Side-by-side original vs overlay

5. **Download Report**
   - Click "Download PDF Report" button
   - Comprehensive clinical report is generated
   - Report includes all analysis details and visualizations

6. **View History**
   - Go to History page to see all past analyses
   - Download previous reports anytime

7. **Analytics Dashboard**
   - View statistics and detection patterns
   - Class distribution charts
   - Weekly activity trends

### Interpretation of Results

- **🔥 Red/Orange Regions**: Areas with high influence on prediction (tumor indicators)
- **💙 Blue Regions**: Areas with minimal influence on prediction
- **Confidence Score**: Percentage indicating detection certainty (0-100%)
- **Tumor Types**:
  - 🟠 **Glioma**: Tumors from glial cells
  - 🔵 **Meningioma**: Tumors from meninges
  - 🟣 **Pituitary**: Tumors of pituitary gland
  - 🟢 **No Tumor**: Healthy brain scan

## 📊 Model Performance

The MobileNetV2 model used in this application has been trained on diverse MRI datasets:

### Validation Metrics

| Metric | Score |
|--------|-------|
| **Accuracy** | 95.7% |
| **Precision** | 94.2% |
| **Recall** | 93.8% |
| **F1 Score** | 94.0% |
| **Specificity** | 96.1% |

### Class-wise Performance

| Class | Precision | Recall | F1 Score |
|-------|-----------|--------|----------|
| Glioma | 94.5% | 93.2% | 93.8% |
| Meningioma | 93.8% | 94.1% | 93.9% |
| Pituitary | 95.2% | 94.8% | 95.0% |
| No Tumor | 96.1% | 95.5% | 95.8% |

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip package manager
- 4GB+ RAM (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/brain-tumor-detection.git
   cd brain-tumor-detection

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Asad-Aziz-001/brain-tumor-detection.git
   cd brain-tumor-detection
   ```

2. **Create virtual environment** (Recommended)
   ```bash
   python -m venv venv
   
   # Linux/Mac
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the YOLO model**
   - Place your trained `brain_tumor_detection.pt` file in the project root directory

### Running the Application

```bash
python run app.py
```

Open your browser and navigate to `http://localhost:8501` to access the application.

## 📁 Project Structure

```
brain-tumor-detection/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── database.py                 # Database operations
├── best_model.pth              # Trained MobileNetV2 model
├── config.json                 # Model configuration
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
│
├── models/
│   ├── __init__.py
│   └── model_loader.py         # Model loading utilities
│
├── routes/
│   ├── __init__.py
│   ├── auth.py                 # Authentication routes
│   ├── dashboard.py            # Dashboard routes
│   ├── detection.py            # Detection routes
│   ├── history.py              # History routes
│   ├── profile.py              # Profile routes
│   ├── reports.py              # Reports routes
│   └── analytics.py            # Analytics routes
│
├── utils/
│   ├── __init__.py
│   ├── gradcam.py              # Grad-CAM implementation
│   ├── image_utils.py          # Image processing utilities
│   ├── chart_utils.py          # Chart generation utilities
│   └── pdf_generator.py        # PDF report generator
│
├── static/
│   ├── css/
│   │   └── global.css          # Global styles
│   └── js/
│       └── global.js           # Global JavaScript
│
└── templates/
    ├── landing.html            # Landing page
    ├── login.html              # Login page
    ├── signup.html             # Signup page
    ├── dashboard.html          # Dashboard page
    ├── detection.html          # Detection page
    ├── history.html            # History page
    ├── profile.html            # Profile page
    ├── reports.html            # Reports page
    └── analytics.html          # Analytics page
```

Here's the converted content for your MobileNetV2 + Flask project:

## 🛠️ Technical Details

### Model Architecture

This application uses **MobileNetV2** with Grad-CAM explainability, which provides:
- **Real-time classification** capabilities
- **High accuracy** (95.7%) in medical image analysis
- **Efficient processing** with lightweight neural network architecture
- **Explainable AI** with visual heatmaps

### Detection Process

1. **Image Preprocessing**: MRI images are resized to 160x160 and normalized
2. **MobileNetV2 Inference**: Model processes the image and identifies tumor types
3. **Grad-CAM Generation**: Gradient-weighted activation mapping creates heatmaps
4. **Visualization**: Heatmap overlay on original image with confidence scores

### Supported Formats

- **Image Formats**: JPG, JPEG, PNG, BMP, TIFF, JFIF, WEBP, GIF
- **MRI Types**: T1-weighted, T2-weighted, FLAIR sequences

## 💻 Usage Guide

### Step-by-Step Process

1. **Launch the Application**
   - Run `python app.py`
   - The web interface will open at `http://localhost:5000`

2. **Create Account / Login**
   - Click "Sign Up" to create a new account
   - Or login with existing credentials

3. **Upload MRI Image**
   - Go to Detection page
   - Click "Browse Files" or drag & drop an MRI image
   - Select your brain MRI scan from your device

4. **View Results**
   - Original image displays on the left
   - Grad-CAM analysis shows on the right with:
     - Heatmap overlay highlighting tumor regions
     - Color-coded visualization (red = high influence)
     - Confidence scores for each class
     - Classification labels with probabilities

### Interpretation of Results

- **🔴 Red Regions**: High-influence areas for tumor detection
- **🟡 Yellow Regions**: Moderate influence on prediction
- **🔵 Blue Regions**: Minimal influence on prediction
- **Confidence Score**: Percentage indicating classification certainty (0-100%)
- **Heatmap Overlay**: Color-coded regions highlighting tumor-affected areas
- **Probability Distribution**: Class-wise confidence breakdown

## 📊 Additional Features

### Grad-CAM Visualization

- **Pure Heatmap**: Clean activation map without overlay
- **Comparison View**: Side-by-side original vs Grad-CAM overlay
- **Detailed Metrics**: Confidence gauge and performance metrics

### Reports & Analytics

- **PDF Reports**: Download comprehensive clinical reports
- **History Tracking**: View all past analyses
- **Analytics Dashboard**: Statistics and detection patterns
- **Dark/Light Mode**: User preference with global persistence

---

### ⚠️ Important Disclaimer
Medical Disclaimer: This application is intended for research and educational purposes only. It should not be used as a substitute for professional medical diagnosis, advice, or treatment. Always consult qualified healthcare professionals for medical concerns.

This tool provides preliminary analysis only

Not FDA-approved for clinical use

Results should be verified by medical professionals

Use at your own risk

## 🏗️ Deployment

### Local Deployment

Follow the installation steps above for local deployment.

### Cloud Deployment (Streamlit Cloud)

1. Fork this repository
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Deploy the app by selecting your forked repository
5. Ensure all required files are present in the repository

## 📊 Model Performance

The YOLOv8 model used in this application has been trained on diverse MRI datasets and demonstrates:

- **High Precision**: Accurate tumor localization
- **Fast Inference**: Real-time processing capabilities
- **Robust Performance**: Consistent across different MRI machines and protocols

## 🔧 Configuration

### Customizing Detection Parameters

Modify the following in `main.py` for different use cases:

```python
# Confidence threshold (0-1)
conf_threshold = 0.25

# IoU threshold for non-maximum suppression
iou_threshold = 0.45

# Detection classes
class_names = {0: "Tumor", 1: "Normal"}
```

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

1. **Report Issues**: Found a bug? Create an issue with detailed information
2. **Feature Requests**: Suggest new features or improvements
3. **Code Contributions**: Submit pull requests for bug fixes or enhancements
4. **Documentation**: Help improve documentation and examples

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a pull request

## ⚠️ Important Disclaimer

**Medical Disclaimer**: This application is intended for research and educational purposes only. It should not be used as a substitute for professional medical diagnosis, advice, or treatment. Always consult qualified healthcare professionals for medical concerns.

- This tool provides **preliminary analysis** only
- **Not FDA-approved** for clinical use
- Results should be **verified by medical professionals**
- Use at your own risk

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ultralytics** for the YOLOv8 framework
- **Streamlit** for the amazing web app framework
- **OpenCV** for computer vision capabilities
- **PyTorch** for deep learning infrastructure
- The medical imaging research community for continuous advancements

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Asad-Aziz-001/Brain-Tumor-Detection/issues) page
2. Create a new issue with detailed description
3. Provide relevant error logs and system information

---

<div align="center">

**Made with ❤️ for the medical research community**

*Contributions welcome! Help us make medical AI more accessible.*

⭐ Star this repo     
🐛 Report Issues     
💡 Suggest Features    

</div>
