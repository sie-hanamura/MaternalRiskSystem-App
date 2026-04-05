"""
MATERNAL RISK ASSESSMENT SYSTEM - Hybrid Architecture
PyQt5 + QWebEngineView for modern UI
Enhanced with PDF Report Generation
"""

import sys
import os
import pickle
import json
import pandas as pd
from datetime import datetime, timedelta

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QFileDialog,
                             QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, pyqtSlot, QObject, pyqtSignal, Qt, QPoint, QSize, QEvent
from PyQt5.QtGui import QIcon, QPainterPath, QRegion

# PDF generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas


class PDFReportGenerator:
    """Generate professional medical assessment reports"""
    
    @staticmethod
    def generate_report(patient_data, assessment_result, filename=None):
        """
        Generate PDF report for maternal risk assessment
        
        Args:
            patient_data: dict with patient info (patient_id, age, weight, height, etc.)
            assessment_result: dict with ML prediction results
            filename: output filename (optional, will auto-generate if None)
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            patient_id = patient_data.get('patient_id', 'UNKNOWN').replace('/', '_')
            filename = f"reports/MRAS_Report_{patient_id}_{timestamp}.pdf"
        
        # Create reports directory if doesn't exist
        os.makedirs('reports', exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for PDF elements
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#36ABA3'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#6b7280'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#374151'),
            spaceAfter=6,
            alignment=TA_LEFT,
            fontName='Helvetica'
        )
        
        # =====================================================================
        # HEADER SECTION
        # =====================================================================
        
        # Logo and title (if logo exists)
        if os.path.exists('assets/logo.png'):
            try:
                logo = RLImage('assets/logo.png', width=1.2*inch, height=1.2*inch)
                logo.hAlign = 'CENTER'
                story.append(logo)
                story.append(Spacer(1, 0.15*inch))
            except:
                pass
        
        # Title
        story.append(Paragraph("MATERNAL RISK ASSESSMENT REPORT", title_style))
        story.append(Paragraph("Municipal Health Office Bay, Laguna", subtitle_style))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                              ParagraphStyle('timestamp', parent=body_style, alignment=TA_CENTER, fontSize=9)))
        
        story.append(Spacer(1, 0.3*inch))
        
        # =====================================================================
        # PATIENT INFORMATION
        # =====================================================================
        
        story.append(Paragraph("PATIENT INFORMATION", heading_style))
        
        patient_info_data = [
            ['Patient ID:', patient_data.get('patient_id', 'N/A')],
            ['Date of Assessment:', datetime.now().strftime('%B %d, %Y')],
            ['Age:', f"{patient_data.get('age', 'N/A')} years"],
            ['Health Worker:', patient_data.get('health_worker', 'N/A')]
        ]
        
        patient_table = Table(patient_info_data, colWidths=[2.2*inch, 4*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#374151')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb'))
        ]))
        
        story.append(patient_table)
        story.append(Spacer(1, 0.2*inch))
        
        # =====================================================================
        # CLINICAL MEASUREMENTS
        # =====================================================================
        
        story.append(Paragraph("CLINICAL MEASUREMENTS", heading_style))
        
        bmi = assessment_result.get('bmi', 0)
        bmi_status = PDFReportGenerator._get_bmi_status(bmi)
        
        measurements_data = [
            ['Measurement', 'Value', 'Status'],
            ['Weight', f"{patient_data.get('weight', 'N/A')} kg", ''],
            ['Height', f"{patient_data.get('height', 'N/A')} cm", ''],
            ['BMI', f"{bmi:.1f} kg/m²", bmi_status],
            ['Blood Pressure', f"{patient_data.get('systolic', 'N/A')}/{patient_data.get('diastolic', 'N/A')} mmHg", 
             PDFReportGenerator._get_bp_status(patient_data.get('systolic', 0), patient_data.get('diastolic', 0))]
        ]
        
        # Add lab results if available
        if assessment_result.get('lab_available', False):
            measurements_data.extend([
                ['Blood Sugar', f"{patient_data.get('blood_sugar', 'N/A')} mmol/L",
                 PDFReportGenerator._get_bs_status(patient_data.get('blood_sugar', 0))],
                ['Hemoglobin', f"{patient_data.get('hemoglobin', 'N/A')} g/dL",
                 PDFReportGenerator._get_hb_status(patient_data.get('hemoglobin', 0))]
            ])
        else:
            measurements_data.append(['Laboratory Tests', 'Not Available', 'Basic screening performed'])
        
        measurements_table = Table(measurements_data, colWidths=[2.2*inch, 2*inch, 2*inch])
        measurements_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#36ABA3')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        story.append(measurements_table)
        story.append(Spacer(1, 0.25*inch))
        
        # =====================================================================
        # RISK ASSESSMENT RESULTS
        # =====================================================================
        
        story.append(Paragraph("RISK ASSESSMENT RESULTS", heading_style))
        
        risk_level = assessment_result.get('risk_level', 'Unknown')
        confidence = assessment_result.get('confidence', 0)
        model_used = assessment_result.get('model_used', 'Unknown')
        
        # Risk level with color
        risk_colors = {
            'Low': colors.HexColor('#10b981'),
            'Moderate': colors.HexColor('#f59e0b'),
            'High': colors.HexColor('#ef4444')
        }
        risk_color = risk_colors.get(risk_level, colors.black)
        
        risk_icons = {'Low': '✓', 'Moderate': '⚠', 'High': '⚠'}
        risk_icon = risk_icons.get(risk_level, '•')
        
        # Create risk assessment box
        risk_data = [
            ['CLASSIFICATION:', f"{risk_icon} {risk_level.upper()} RISK"],
            ['Confidence Level:', f"{confidence:.1f}%"],
            ['Model Used:', model_used]
        ]
        
        risk_table = Table(risk_data, colWidths=[2*inch, 4.2*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#374151')),
            ('TEXTCOLOR', (1, 0), (1, 0), risk_color),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 0), (1, 0), 14),
            ('FONTSIZE', (0, 0), (0, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('BOX', (0, 0), (-1, -1), 2, risk_color)
        ]))
        
        story.append(risk_table)
        story.append(Spacer(1, 0.15*inch))
        
        # Probability breakdown
        probs = assessment_result.get('probabilities', {'low': 0, 'moderate': 0, 'high': 0})
        
        prob_data = [
            ['Risk Category', 'Probability'],
            ['Low Risk', f"{probs.get('low', 0):.1f}%"],
            ['Moderate Risk', f"{probs.get('moderate', 0):.1f}%"],
            ['High Risk', f"{probs.get('high', 0):.1f}%"]
        ]
        
        prob_table = Table(prob_data, colWidths=[3*inch, 3.2*inch])
        prob_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#374151')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb'))
        ]))
        
        story.append(prob_table)
        story.append(Spacer(1, 0.25*inch))
        
        # =====================================================================
        # CLINICAL RECOMMENDATIONS
        # =====================================================================
        
        story.append(Paragraph("CLINICAL RECOMMENDATIONS", heading_style))
        
        recommendations = PDFReportGenerator._get_recommendations(risk_level)
        
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", body_style))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Add important note based on risk level
        if risk_level == 'High':
            note_style = ParagraphStyle(
                'WarningNote',
                parent=body_style,
                textColor=colors.HexColor('#dc2626'),
                fontSize=11,
                fontName='Helvetica-Bold',
                borderWidth=2,
                borderColor=colors.HexColor('#ef4444'),
                borderPadding=10,
                backColor=colors.HexColor('#fee2e2')
            )
            story.append(Paragraph("⚠ URGENT: Immediate referral to hospital with OB-GYN services is required. Do not delay.", note_style))
        elif risk_level == 'Moderate':
            note_style = ParagraphStyle(
                'CautionNote',
                parent=body_style,
                textColor=colors.HexColor('#92400e'),
                fontSize=10,
                fontName='Helvetica-Bold',
                borderWidth=1,
                borderColor=colors.HexColor('#f59e0b'),
                borderPadding=8,
                backColor=colors.HexColor('#fef3c7')
            )
            story.append(Paragraph("⚠ Coordinate with RHU midwife or physician for management plan.", note_style))
        else:
            note_style = ParagraphStyle(
                'InfoNote',
                parent=body_style,
                textColor=colors.HexColor('#065f46'),
                fontSize=10,
                borderWidth=1,
                borderColor=colors.HexColor('#10b981'),
                borderPadding=8,
                backColor=colors.HexColor('#d1fae5')
            )
            story.append(Paragraph("✓ Patient can be managed at barangay health center level with routine care.", note_style))
        
        story.append(Spacer(1, 0.3*inch))
        
        # =====================================================================
        # SIGNATURE SECTION
        # =====================================================================
        
        story.append(Paragraph("HEALTH WORKER CERTIFICATION", heading_style))
        
        sig_data = [
            ['Health Worker Name:', '________________________________'],
            ['Signature:', '________________________________'],
            ['Date:', datetime.now().strftime('%B %d, %Y')]
        ]
        
        sig_table = Table(sig_data, colWidths=[2*inch, 4.2*inch])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8)
        ]))
        
        story.append(sig_table)
        story.append(Spacer(1, 0.3*inch))
        
        # =====================================================================
        # FOOTER
        # =====================================================================
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=body_style,
            fontSize=8,
            textColor=colors.HexColor('#9ca3af'),
            alignment=TA_CENTER
        )
        
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("_______________________________________________", footer_style))
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph("This report is generated by the Maternal Risk Assessment System (MRAS)", footer_style))
        story.append(Paragraph("Municipal Health Office Bay, Laguna | AI-Assisted Screening Tool", footer_style))
        story.append(Paragraph("⚠ This is a screening tool, not a diagnostic system. Always follow clinical judgment and protocols.", footer_style))
        
        # Build PDF
        doc.build(story)
        
        return filename
    
    @staticmethod
    def _get_bmi_status(bmi):
        """Get BMI status text"""
        if bmi < 18.5:
            return "⚠ Underweight"
        elif bmi < 25:
            return "✓ Normal"
        elif bmi < 30:
            return "⚠ Overweight"
        else:
            return "⚠ Obese"
    
    @staticmethod
    def _get_bp_status(systolic, diastolic):
        """Get blood pressure status"""
        if systolic >= 140 or diastolic >= 90:
            return "⚠ Hypertensive"
        elif systolic >= 120 or diastolic >= 80:
            return "⚠ Prehypertensive"
        else:
            return "✓ Normal"
    
    @staticmethod
    def _get_bs_status(blood_sugar):
        """Get blood sugar status"""
        if blood_sugar >= 7.0:
            return "⚠ High (Diabetic range)"
        elif blood_sugar >= 5.6:
            return "⚠ Borderline"
        else:
            return "✓ Normal"
    
    @staticmethod
    def _get_hb_status(hemoglobin):
        """Get hemoglobin status"""
        if hemoglobin < 9.5:
            return "⚠ Low (Anemic)"
        elif hemoglobin < 11.0:
            return "⚠ Mild Anemia"
        else:
            return "✓ Normal"
    
    @staticmethod
    def _get_recommendations(risk_level):
        """Get clinical recommendations based on risk level"""
        if risk_level == 'Low':
            return [
                "Continue regular prenatal checkups (monthly schedule)",
                "Maintain healthy diet with adequate nutrition",
                "Engage in moderate physical activity as tolerated",
                "Monitor for any changes in symptoms or condition",
                "Return immediately if warning signs appear (severe headache, vision changes, severe abdominal pain, vaginal bleeding, decreased fetal movement)",
                "Schedule next checkup in 4 weeks at barangay health station"
            ]
        elif risk_level == 'Moderate':
            return [
                "Refer to Rural Health Unit (RHU) for comprehensive evaluation by physician or midwife",
                "Increase prenatal visit frequency to bi-weekly or as advised by RHU",
                "Monitor blood pressure and blood sugar levels regularly",
                "Educate patient on warning signs requiring immediate attention",
                "May require additional diagnostic tests or specialist consultation",
                "Prepare birth plan with consideration for potential complications"
            ]
        else:  # High
            return [
                "IMMEDIATE referral to district/provincial hospital with Obstetrician-Gynecologist services",
                "Patient requires specialist care and intensive monitoring",
                "High-risk pregnancy may require advanced medical interventions",
                "Coordinate emergency transport if needed",
                "Weekly or more frequent prenatal visits required",
                "Hospital delivery strongly recommended",
                "Alert receiving facility of incoming high-risk maternal case"
            ]


class Backend(QObject):
    """Python backend - handles all ML logic and data operations"""

    results_ready = pyqtSignal(str)

    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.load_models()
        self.risk_labels = {0: 'Low', 1: 'Moderate', 2: 'High'}
        self.current_patient_data = {}
        self.current_assessment = {}
    
    def load_models(self):
        """Load ML models"""
        try:
            with open('model_BEST_for_deployment.pkl', 'rb') as f:
                self.model_full = pickle.load(f)
            with open('scaler.pkl', 'rb') as f:
                self.scaler_full = pickle.load(f)
            with open('model_config.json', 'r') as f:
                self.config_full = json.load(f)
            with open('model_BASIC_for_deployment.pkl', 'rb') as f:
                self.model_basic = pickle.load(f)
            with open('scaler_BASIC.pkl', 'rb') as f:
                self.scaler_basic = pickle.load(f)
            with open('model_config_BASIC.json', 'r') as f:
                self.config_basic = json.load(f)
            print("✓ Models loaded successfully")
        except Exception as e:
            print(f"Error loading models: {e}")
            sys.exit(1)
    
    @pyqtSlot(float, float, float, float, float, float, float, bool, result=str)
    def assess_risk(self, age, weight, height, systolic, diastolic, 
                blood_sugar, hemoglobin, lab_available):
        """Assess maternal risk - called from JavaScript"""
        try:
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            
            # Store patient data for PDF generation
            self.current_patient_data = {
                'age': age,
                'weight': weight,
                'height': height,
                'systolic': systolic,
                'diastolic': diastolic,
                'blood_sugar': blood_sugar,
                'hemoglobin': hemoglobin
            }
            
            if lab_available:
                input_data = pd.DataFrame({
                    'BMI': [bmi],
                    'SystolicBP': [systolic],
                    'Blood Sugar Level': [blood_sugar],
                    'Hemoglobin Level': [hemoglobin],
                    'DiastolicBP': [diastolic]
                })
                input_scaled = self.scaler_full.transform(input_data)
                prediction_num = self.model_full.predict(input_scaled)[0]
                prediction_proba = self.model_full.predict_proba(input_scaled)[0]
                model_used = "Full Model (5 features)"
            else:
                input_data = pd.DataFrame({
                    'BMI': [bmi],
                    'SystolicBP': [systolic],
                    'DiastolicBP': [diastolic]
                })
                input_scaled = self.scaler_basic.transform(input_data)
                prediction_num = self.model_basic.predict(input_scaled)[0]
                prediction_proba = self.model_basic.predict_proba(input_scaled)[0]
                model_used = "Basic Model (3 features)"
            
            risk_level = self.risk_labels[prediction_num]
            confidence = float(prediction_proba[prediction_num] * 100)
            
            def safe_float(value):
                try:
                    val = float(value)
                    return 0.0 if (val != val) else val
                except:
                    return 0.0
            
            result = {
                'risk_level': str(risk_level),
                'confidence': safe_float(confidence),
                'probabilities': {
                    'low': safe_float(prediction_proba[0] * 100),
                    'moderate': safe_float(prediction_proba[1] * 100),
                    'high': safe_float(prediction_proba[2] * 100)
                },
                'bmi': safe_float(bmi),
                'model_used': str(model_used),
                'lab_available': bool(lab_available)
            }
            
            # Store current assessment for PDF generation
            self.current_assessment = result
            
            print(f"✓ Assessment complete: {risk_level} ({confidence:.1f}%)")
            print(f"  Probabilities - Low: {result['probabilities']['low']:.1f}%, Moderate: {result['probabilities']['moderate']:.1f}%, High: {result['probabilities']['high']:.1f}%")
            
            return json.dumps(result)
            
        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            print(f"✗ Assessment error: {error_msg}")
            return json.dumps({'error': str(e)})
    
    @pyqtSlot(str, str, result=str)
    def generate_pdf_report(self, patient_id, health_worker):
        """Generate PDF report for current assessment"""
        try:
            if not self.current_assessment:
                return json.dumps({'success': False, 'error': 'No assessment data available'})
            
            # Combine patient data with IDs
            patient_data = {
                **self.current_patient_data,
                'patient_id': patient_id or 'N/A',
                'health_worker': health_worker or 'N/A'
            }
            
            # Generate PDF
            filename = PDFReportGenerator.generate_report(
                patient_data, 
                self.current_assessment
            )
            
            print(f"✓ PDF report generated: {filename}")
            return json.dumps({
                'success': True, 
                'filename': filename,
                'message': f'Report saved: {filename}'
            })
            
        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            print(f"✗ PDF generation error: {error_msg}")
            return json.dumps({'success': False, 'error': str(e)})
    
    @pyqtSlot(result=str)
    def generate_patient_id(self):
        """Generate unique Patient ID in format P-YYYY-NNNN"""
        try:
            current_year = datetime.now().year
            history_file = 'assessment_history.csv'

            # Default starting number
            next_number = 1

            if os.path.exists(history_file):
                df = pd.read_csv(history_file)

                if not df.empty and 'Patient_ID' in df.columns:
                    # Filter Patient IDs for current year (format: P-YYYY-NNNN)
                    year_prefix = f"P-{current_year}-"
                    current_year_ids = df[df['Patient_ID'].astype(str).str.startswith(year_prefix)]

                    if not current_year_ids.empty:
                        # Extract numbers from IDs like P-2025-0123 -> 123
                        numbers = []
                        for pid in current_year_ids['Patient_ID']:
                            try:
                                # Split by '-' and get the last part, convert to int
                                num = int(str(pid).split('-')[-1])
                                numbers.append(num)
                            except (ValueError, IndexError):
                                continue

                        if numbers:
                            next_number = max(numbers) + 1

            # Format: P-YYYY-NNNN (e.g., P-2025-0001)
            patient_id = f"P-{current_year}-{next_number:04d}"

            print(f"✓ Generated Patient ID: {patient_id}")
            return json.dumps({
                'success': True,
                'patient_id': patient_id
            })

        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            print(f"✗ Error generating Patient ID: {error_msg}")
            return json.dumps({
                'success': False,
                'error': str(e),
                'patient_id': f"P-{datetime.now().year}-0001"  # Fallback
            })

    @pyqtSlot(str, result=str)
    def save_assessment(self, json_data):
        """Save assessment to CSV with proper type handling

        Args:
            json_data (str): JSON string containing all assessment data with fields:
                - patient_id (str): Patient identifier
                - health_worker (str): Health worker name
                - age (int): Patient age
                - bmi (float): Body Mass Index
                - systolic (float): Systolic blood pressure
                - diastolic (float): Diastolic blood pressure
                - blood_sugar (float): Blood sugar level
                - hemoglobin (float): Hemoglobin level
                - risk_level (str): Risk assessment result
                - confidence (float): Confidence percentage
                - model_used (str): Model identifier
                - lab_available (bool/str): Laboratory availability

        Returns:
            str: JSON response with success/error status
        """
        try:
            # Parse JSON string to extract data
            print(f"\n{'='*60}")
            print(f"✓ save_assessment METHOD CALLED SUCCESSFULLY")
            print(f"Received JSON: {json_data!r}")
            print(f"{'='*60}\n")

            data = json.loads(json_data)

            # Extract fields from JSON
            patient_id = data.get('patient_id', 'N/A')
            health_worker = data.get('health_worker', 'N/A')
            age = data.get('age', 25)
            bmi = data.get('bmi', 0.0)
            systolic = data.get('systolic', 120)
            diastolic = data.get('diastolic', 80)
            blood_sugar = data.get('blood_sugar', 0.0)
            hemoglobin = data.get('hemoglobin', 0.0)
            risk_level = data.get('risk_level', 'Unknown')
            confidence = data.get('confidence', 0.0)
            model_used = data.get('model_used', 'Unknown')
            lab_available = data.get('lab_available', False)

            # Debug print - verify data extraction
            print(f"Extracted data:")
            print(f"  patient_id: {patient_id!r} ({type(patient_id).__name__})")
            print(f"  health_worker: {health_worker!r} ({type(health_worker).__name__})")
            print(f"  age: {age!r} ({type(age).__name__})")
            print(f"  bmi: {bmi!r} ({type(bmi).__name__})")
            print(f"  systolic: {systolic!r} ({type(systolic).__name__})")
            print(f"  diastolic: {diastolic!r} ({type(diastolic).__name__})")
            print(f"  blood_sugar: {blood_sugar!r} ({type(blood_sugar).__name__})")
            print(f"  hemoglobin: {hemoglobin!r} ({type(hemoglobin).__name__})")
            print(f"  risk_level: {risk_level!r} ({type(risk_level).__name__})")
            print(f"  confidence: {confidence!r} ({type(confidence).__name__})")
            print(f"  model_used: {model_used!r} ({type(model_used).__name__})")
            print(f"  lab_available: {lab_available!r} ({type(lab_available).__name__})")

            # Convert lab_available to boolean (handles bool, string "1"/"0", or "true"/"false")
            if isinstance(lab_available, str):
                lab_bool = lab_available in ("1", "true", "True", "yes", "Yes")
            else:
                lab_bool = bool(lab_available)

            record = {
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Patient_ID': str(patient_id).strip() if patient_id and str(patient_id).strip() not in ['', 'N/A'] else 'N/A',
                'Age': int(age),
                'BMI': float(bmi),
                'SystolicBP': float(systolic),
                'DiastolicBP': float(diastolic),
                'Blood_Sugar': float(blood_sugar) if lab_bool else None,
                'Hemoglobin': float(hemoglobin) if lab_bool else None,
                'Risk_Level': str(risk_level),
                'Confidence': f"{float(confidence):.1f}%",
                'Model_Used': str(model_used),
                'Lab_Available': 'Yes' if lab_bool else 'No',
                'Health_Worker': str(health_worker).strip() if health_worker and str(health_worker).strip() not in ['', 'N/A'] else 'N/A'
            }

            history_file = 'assessment_history.csv'
            if os.path.exists(history_file):
                df = pd.read_csv(history_file)
                df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
            else:
                df = pd.DataFrame([record])

            df.to_csv(history_file, index=False, na_rep='N/A')

            print(f"✓ Assessment saved: Patient {patient_id}")
            return json.dumps({
                'success': True,
                'message': 'Assessment saved successfully',
                'patient_id': record['Patient_ID']
            })

        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            print(f"✗ Save error: {error_msg}")
            return json.dumps({
                'success': False,
                'error': str(e),
                'details': error_msg
            })
    
    @pyqtSlot(result=str)
    def load_history(self):
        """Load assessment history as JSON"""
        try:
            if not os.path.exists('assessment_history.csv'):
                return json.dumps([])

            # Read CSV and handle mixed types properly
            df = pd.read_csv('assessment_history.csv', keep_default_na=True)

            # Replace NaN/None with 'N/A' for display purposes
            df = df.fillna('N/A')

            # Convert to dict and return as JSON
            records = df.to_dict('records')
            return json.dumps(records)

        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            print(f"Error loading history: {error_msg}")
            return json.dumps([])

    @pyqtSlot(result=str)
    def get_dashboard_stats(self):
        """Calculate statistics from assessment history for dashboard"""
        try:
            if not os.path.exists('assessment_history.csv'):
                return json.dumps({
                    'total_assessments': 0,
                    'high_risk_count': 0,
                    'high_risk_percentage': 0,
                    'avg_confidence': 0,
                    'recent_activity': 0,
                    'risk_distribution': {'Low': 0, 'Moderate': 0, 'High': 0},
                    'weekly_assessments': [],
                    'risk_factors': []
                })

            df = pd.read_csv('assessment_history.csv')

            # Basic stats
            total = len(df)
            high_risk = len(df[df['Risk_Level'] == 'High'])

            # Average confidence (remove % sign and convert to float)
            df['Confidence_Value'] = df['Confidence'].str.replace('%', '').astype(float)
            avg_conf = df['Confidence_Value'].mean()

            # Recent activity (last 7 days)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            seven_days_ago = datetime.now() - timedelta(days=7)
            recent = len(df[df['Timestamp'] >= seven_days_ago])

            # Risk distribution
            risk_dist = df['Risk_Level'].value_counts().to_dict()

            # Weekly assessments (last 12 weeks)
            df['Week'] = df['Timestamp'].dt.to_period('W')
            weekly = df.groupby('Week').size().tail(12).to_dict()
            weekly_data = [{'week': str(k), 'count': int(v)} for k, v in weekly.items()]

            # Most common risk factors (in High risk cases only)
            high_df = df[df['Risk_Level'] == 'High']
            risk_factors = []

            if not high_df.empty:
                # BMI >= 30
                high_bmi = len(high_df[high_df['BMI'] >= 30])
                if high_bmi > 0:
                    risk_factors.append({
                        'factor': 'High BMI (≥30 kg/m²)',
                        'count': high_bmi,
                        'percentage': round(high_bmi / len(high_df) * 100, 1)
                    })

                # High BP (≥140 or ≥90)
                high_bp = len(high_df[(high_df['SystolicBP'] >= 140) | (high_df['DiastolicBP'] >= 90)])
                if high_bp > 0:
                    risk_factors.append({
                        'factor': 'Hypertension (BP ≥140/90)',
                        'count': high_bp,
                        'percentage': round(high_bp / len(high_df) * 100, 1)
                    })

                # High Blood Sugar (≥7.0) - only if available
                if 'Blood_Sugar' in high_df.columns:
                    high_bs = len(high_df[high_df['Blood_Sugar'] >= 7.0])
                    if high_bs > 0:
                        risk_factors.append({
                            'factor': 'High Blood Sugar (≥7.0 mmol/L)',
                            'count': high_bs,
                            'percentage': round(high_bs / len(high_df) * 100, 1)
                        })

                # Low Hemoglobin (<9.5) - only if available
                if 'Hemoglobin' in high_df.columns:
                    low_hb = len(high_df[high_df['Hemoglobin'] < 9.5])
                    if low_hb > 0:
                        risk_factors.append({
                            'factor': 'Severe Anemia (Hb <9.5 g/dL)',
                            'count': low_hb,
                            'percentage': round(low_hb / len(high_df) * 100, 1)
                        })

            # Sort by count descending
            risk_factors.sort(key=lambda x: x['count'], reverse=True)

            return json.dumps({
                'total_assessments': int(total),
                'high_risk_count': int(high_risk),
                'high_risk_percentage': round(high_risk / total * 100, 1) if total > 0 else 0,
                'avg_confidence': round(avg_conf, 1),
                'recent_activity': int(recent),
                'risk_distribution': {k: int(v) for k, v in risk_dist.items()},
                'weekly_assessments': weekly_data,
                'risk_factors': risk_factors[:5]  # Top 5
            })

        except Exception as e:
            import traceback
            print(f"Dashboard stats error: {traceback.format_exc()}")
            return json.dumps({'error': str(e)})

    @pyqtSlot()
    def minimize_window(self):
        """Minimize window - called from JavaScript"""
        if self.main_window:
            self.main_window.showMinimized()

    @pyqtSlot()
    def maximize_window(self):
        """Toggle maximize/restore - called from JavaScript"""
        if self.main_window:
            self.main_window.toggle_maximize()

    @pyqtSlot()
    def close_window(self):
        """Close window - called from JavaScript"""
        if self.main_window:
            self.main_window.close()

    @pyqtSlot(int, int)
    def start_window_drag(self, x, y):
        """Start window drag - called from JavaScript"""
        if self.main_window:
            self.main_window.drag_start_pos = QPoint(x, y)

    @pyqtSlot(int, int)
    def move_window(self, global_x, global_y):
        """Move window during drag - called from JavaScript"""
        if self.main_window and self.main_window.drag_start_pos and not self.main_window.is_maximized:
            self.main_window.move(global_x - self.main_window.drag_start_pos.x(),
                                 global_y - self.main_window.drag_start_pos.y())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Frameless window setup
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Window properties
        self.setGeometry(100, 50, 1400, 900)
        if os.path.exists('assets/icon.png'):
            self.setWindowIcon(QIcon('assets/icon.png'))

        # Track drag position and maximized state
        self.drag_pos = QPoint()
        self.drag_start_pos = None
        self.is_maximized = False
        self.normal_geometry = None  # Store geometry before maximizing

        # Create central container widget with rounded corners
        self.central_container = QWidget()
        self.central_container.setObjectName("centralContainer")
        self.central_container.setStyleSheet("""
            #centralContainer {
                background: white;
                border-radius: 16px;
            }
        """)

        # Main layout
        container_layout = QVBoxLayout(self.central_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Create invisible title bar for window dragging functionality
        self.title_bar = self.create_title_bar()
        self.title_bar.setFixedHeight(0)
        self.title_bar.setVisible(False)
        container_layout.addWidget(self.title_bar)

        # Create web view
        self.browser = QWebEngineView()
        self.browser.setStyleSheet("""
            QWebEngineView {
                background: transparent;
                border-radius: 16px;
            }
        """)

        # Set up Python ↔ JavaScript bridge
        self.backend = Backend(main_window=self)
        self.channel = QWebChannel()
        self.channel.registerObject('backend', self.backend)
        self.browser.page().setWebChannel(self.channel)

        # Load local HTML UI
        html_path = os.path.join(os.getcwd(), 'ui', 'index.html')
        self.browser.load(QUrl.fromLocalFile(html_path))
        self.browser.page().profile().clearHttpCache()

        container_layout.addWidget(self.browser)

        # Set central widget
        self.setCentralWidget(self.central_container)

        # Apply initial rounded corners
        self.update_window_shape()

        print("✓ Modern frameless window initialized")

    def update_window_shape(self):
        """Apply rounded corners mask when window is not maximized"""
        if not self.is_maximized:
            # Apply rounded corners to the entire window
            path = QPainterPath()
            path.addRoundedRect(0, 0, self.width(), self.height(), 16, 16)
            region = QRegion(path.toFillPolygon().toPolygon())
            self.setMask(region)
        else:
            # Remove mask when maximized (square corners)
            self.clearMask()

    def update_maximize_icon(self):
        """Update maximize/restore button icon based on window state"""
        if self.is_maximized:
            # Show restore icon
            if os.path.exists('assets/restore-icon.png'):
                self.max_btn.setIcon(QIcon('assets/restore-icon.png'))
                self.max_btn.setIconSize(QSize(16, 16))
            else:
                self.max_btn.setText("❐")
        else:
            # Show maximize icon
            if os.path.exists('assets/maximize-icon.png'):
                self.max_btn.setIcon(QIcon('assets/maximize-icon.png'))
                self.max_btn.setIconSize(QSize(16, 16))
            else:
                self.max_btn.setText("□")

    def changeEvent(self, event):
        """Handle window state changes (maximize/restore) - SINGLE SOURCE OF TRUTH"""
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMaximized:
                # Window was maximized
                self.is_maximized = True
                self.clearMask()
                # Remove rounded corners when maximized
                self.central_container.setStyleSheet("""
                    #centralContainer {
                        background: white;
                        border-radius: 0px;
                    }
                """)
                # Update button icon
                self.update_maximize_icon()
            elif self.windowState() == Qt.WindowNoState:
                # Window was restored to normal
                self.is_maximized = False
                self.update_window_shape()
                # Restore rounded corners
                self.central_container.setStyleSheet("""
                    #centralContainer {
                        background: white;
                        border-radius: 16px;
                    }
                """)
                # Update button icon
                self.update_maximize_icon()
        super().changeEvent(event)

    def create_title_bar(self):
        """Create custom title bar with window controls"""
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("""
            QWidget {
                background: white;
                border-top-left-radius: 16px;
                border-top-right-radius: 16px;
            }
        """)

        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(16, 0, 4, 0)
        layout.setSpacing(0)

        # Add stretch to push buttons to the right
        layout.addStretch()

        # Window control buttons
        btn_style = """
            QPushButton {
                width: 40px;
                height: 32px;
                border: none;
                border-radius: 6px;
                background: transparent;
            }
            QPushButton:hover {
                background: #f3f4f6;
            }
        """

        close_btn_style = """
            QPushButton {
                width: 40px;
                height: 32px;
                border: none;
                border-radius: 6px;
                background: transparent;
            }
            QPushButton:hover {
                background: #ef4444;
            }
        """

        # Minimize button
        self.min_btn = QPushButton()
        if os.path.exists('assets/minimize-icon.png'):
            self.min_btn.setIcon(QIcon('assets/minimize-icon.png'))
            self.min_btn.setIconSize(QSize(16, 16))
        else:
            self.min_btn.setText("−")
        self.min_btn.setStyleSheet(btn_style)
        self.min_btn.clicked.connect(self.showMinimized)

        # Maximize/Restore button
        self.max_btn = QPushButton()
        self.max_btn.setStyleSheet(btn_style)
        self.max_btn.clicked.connect(self.toggle_maximize)
        # Icon will be set by update_maximize_icon()
        self.update_maximize_icon()

        # Close button
        self.close_btn = QPushButton()
        if os.path.exists('assets/close-icon.png'):
            self.close_btn.setIcon(QIcon('assets/close-icon.png'))
            self.close_btn.setIconSize(QSize(16, 16))
        else:
            self.close_btn.setText("✕")
        self.close_btn.setStyleSheet(close_btn_style)
        self.close_btn.clicked.connect(self.close)

        # Add buttons with spacing
        layout.addWidget(self.min_btn)
        layout.addSpacing(4)
        layout.addWidget(self.max_btn)
        layout.addSpacing(4)
        layout.addWidget(self.close_btn)

        # Make title bar draggable
        title_bar.mousePressEvent = self.title_bar_mouse_press
        title_bar.mouseMoveEvent = self.title_bar_mouse_move
        title_bar.mouseDoubleClickEvent = self.title_bar_double_click

        return title_bar

    def title_bar_mouse_press(self, event):
        """Handle mouse press on title bar for dragging"""
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def title_bar_mouse_move(self, event):
        """Handle mouse move on title bar for dragging"""
        if event.buttons() == Qt.LeftButton and not self.is_maximized:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def title_bar_double_click(self, event):
        """Handle double-click on title bar to maximize/restore"""
        if event.button() == Qt.LeftButton:
            self.toggle_maximize()
            event.accept()

    def toggle_maximize(self):
        """Toggle between maximized and normal window state"""
        # Check Qt's actual window state
        if self.windowState() & Qt.WindowMaximized:
            # Currently maximized - restore to normal
            self.showNormal()
            # changeEvent will handle state update and icon change
        else:
            # Currently normal - maximize
            self.showMaximized()
            # changeEvent will handle state update and icon change

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Maternal Risk Assessment System")
    app.setOrganizationName("Municipal Health Office Bay, Laguna")
    
    # Set app icon
    if os.path.exists('assets/icon.png'):
        app.setWindowIcon(QIcon('assets/icon.png'))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()