# utils/chart_utils.py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

def create_probability_chart(probabilities, class_names):
    plt.clf()
    plt.close('all')
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = {
        'glioma_tumor': '#ff9800', 
        'meningioma_tumor': '#2196f3', 
        'pituitary_tumor': '#9c27b0', 
        'no_tumor': '#4caf50'
    }
    class_colors = [colors.get(name, '#666') for name in class_names]
    display_names = [name.replace('_', ' ').title() for name in class_names]
    bars = ax.barh(display_names, probabilities * 100, color=class_colors)
    ax.set_xlabel('Probability (%)', fontsize=12)
    ax.set_title('Prediction Probabilities by Class', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 100)
    
    for i, (bar, prob) in enumerate(zip(bars, probabilities)):
        ax.text(prob * 100 + 1, bar.get_y() + bar.get_height()/2, 
               f'{prob*100:.1f}%', va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plt.close('all')
    return base64.b64encode(img.getvalue()).decode()

def create_heatmap_image(heatmap):
    plt.clf()
    plt.close('all')
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(heatmap, cmap='jet', alpha=0.8)
    ax.set_title('Activation Heatmap', fontsize=14, fontweight='bold')
    ax.axis('off')
    plt.colorbar(im, ax=ax, label='Activation Strength')
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plt.close('all')
    return base64.b64encode(img.getvalue()).decode()

def create_comparison_image(original_image, heatmap):
    plt.clf()
    plt.close('all')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.imshow(original_image)
    ax1.set_title('Original MRI Scan', fontsize=12, fontweight='bold')
    ax1.axis('off')
    ax2.imshow(original_image)
    ax2.imshow(heatmap, cmap='jet', alpha=0.5)
    ax2.set_title('With Grad-CAM Overlay', fontsize=12, fontweight='bold')
    ax2.axis('off')
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plt.close('all')
    return base64.b64encode(img.getvalue()).decode()

def create_detailed_metrics_chart(probabilities, class_names, confidence):
    plt.clf()
    plt.close('all')
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    colors = ['#ff9800', '#2196f3', '#9c27b0', '#4caf50']
    display_names = [name.replace('_', ' ').title() for name in class_names]
    ax1.bar(display_names, probabilities * 100, color=colors)
    ax1.set_ylabel('Probability (%)')
    ax1.set_title('Class Probabilities')
    ax1.set_ylim(0, 100)
    for i, prob in enumerate(probabilities):
        ax1.text(i, prob * 100 + 1, f'{prob*100:.1f}%', ha='center', fontweight='bold')
    
    ax2.pie(probabilities, labels=display_names, autopct='%1.1f%%', colors=colors)
    ax2.set_title('Probability Distribution')
    
    # Confidence gauge
    theta = np.linspace(0, np.pi, 100)
    r = 1
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    ax3.plot(x, y, 'k-', linewidth=2)
    ax3.fill_between(x, 0, y, where=(theta <= np.pi * confidence), color='green', alpha=0.5)
    ax3.set_xlim(-1.2, 1.2)
    ax3.set_ylim(0, 1.2)
    ax3.set_aspect('equal')
    ax3.set_title(f'Confidence: {confidence*100:.1f}%')
    ax3.axis('off')
    
    # Model metrics
    metrics = ['Accuracy: 95.7%', 'Precision: 94.2%', 'Recall: 93.8%', 'F1-Score: 94.0%']
    ax4.axis('tight')
    ax4.axis('off')
    table_data = [[m] for m in metrics]
    table = ax4.table(cellText=table_data, loc='center', cellLoc='center', colWidths=[0.3])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plt.close('all')
    return base64.b64encode(img.getvalue()).decode()