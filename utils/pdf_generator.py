# utils/pdf_generator.py
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import os
from utils.image_utils import save_image_temp

def generate_pdf_report(result, original_arr, overlay_arr, heatmap_arr, comparison_arr, probability_chart, detailed_metrics, upload_folder, report_folder):
    """Generate comprehensive PDF report"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    pdf_path = os.path.join(report_folder, f'neuroscan_report_{timestamp}.pdf')
    
    # Save images temporarily
    orig_img_path = save_image_temp(original_arr, 'original', upload_folder)
    overlay_img_path = save_image_temp(overlay_arr, 'overlay', upload_folder)
    heatmap_img_path = save_image_temp(heatmap_arr, 'heatmap', upload_folder)
    comparison_img_path = save_image_temp(comparison_arr, 'comparison', upload_folder)
    
    # Decode base64 images
    import base64
    prob_chart_data = base64.b64decode(probability_chart)
    prob_chart_path = os.path.join(upload_folder, f'prob_chart_{timestamp}.png')
    with open(prob_chart_path, 'wb') as f:
        f.write(prob_chart_data)
    
    metrics_chart_data = base64.b64decode(detailed_metrics)
    metrics_chart_path = os.path.join(upload_folder, f'metrics_chart_{timestamp}.png')
    with open(metrics_chart_path, 'wb') as f:
        f.write(metrics_chart_data)
    
    # Create PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, 
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
                                 fontSize=24, textColor=colors.HexColor('#667eea'),
                                 alignment=TA_CENTER, spaceAfter=30)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'],
                                   fontSize=16, textColor=colors.HexColor('#764ba2'),
                                   spaceAfter=12, spaceBefore=12)
    normal_style = styles['Normal']
    
    story = []
    
    # Title
    story.append(Paragraph("NeuroScan AI - Clinical Report", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    story.append(Spacer(1, 20))
    
    # Diagnosis Result
    story.append(Paragraph("Diagnosis Result", heading_style))
    pred_class = result['prediction']
    confidence = result['confidence'] * 100
    display_name = pred_class.replace('_', ' ').upper()
    
    diagnosis_text = f"<b>Finding:</b> {display_name}<br/><b>Confidence:</b> {confidence:.1f}%"
    if pred_class == 'no_tumor':
        diagnosis_text += "<br/><b>Status:</b> No tumor detected. The brain scan appears normal."
    else:
        diagnosis_text += "<br/><b>Status:</b> Tumor detected. Please consult a medical professional."
    
    story.append(Paragraph(diagnosis_text, normal_style))
    story.append(Spacer(1, 20))
    
    # Images Section
    story.append(Paragraph("Medical Imaging Analysis", heading_style))
    
    img_data = [
        [ReportImage(orig_img_path, width=2.5*inch, height=2.5*inch),
         ReportImage(overlay_img_path, width=2.5*inch, height=2.5*inch)]
    ]
    img_table = Table(img_data, colWidths=[2.5*inch, 2.5*inch])
    img_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(img_table)
    
    caption_data = [['Original MRI Scan', 'Grad-CAM Analysis']]
    caption_table = Table(caption_data, colWidths=[2.5*inch, 2.5*inch])
    caption_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ]))
    story.append(caption_table)
    story.append(Spacer(1, 15))
    
    # Probability Charts
    story.append(Paragraph("Statistical Analysis", heading_style))
    story.append(ReportImage(prob_chart_path, width=5*inch, height=3*inch))
    story.append(Spacer(1, 10))
    
    # Class Probabilities Table
    story.append(Paragraph("Class-wise Probabilities", heading_style))
    prob_data = [['Class', 'Probability', 'Confidence Level']]
    class_names = list(result['all_probabilities'].keys())
    for class_name in class_names:
        prob = result['all_probabilities'][class_name] * 100
        level = 'High' if prob > 70 else 'Medium' if prob > 30 else 'Low'
        display_name = class_name.replace('_', ' ').title()
        prob_data.append([display_name, f'{prob:.1f}%', level])
    
    prob_table = Table(prob_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(prob_table)
    story.append(Spacer(1, 20))
    
    # Disclaimer
    story.append(Paragraph("Disclaimer", heading_style))
    disclaimer_text = """
    This report is generated by an AI-based system for research and educational purposes only. 
    The analysis should not be considered as a substitute for professional medical advice.
    """
    story.append(Paragraph(disclaimer_text, normal_style))
    
    doc.build(story)
    
    # Cleanup
    for path in [orig_img_path, overlay_img_path, heatmap_img_path, comparison_img_path, prob_chart_path, metrics_chart_path]:
        if os.path.exists(path):
            os.remove(path)
    
    return pdf_path