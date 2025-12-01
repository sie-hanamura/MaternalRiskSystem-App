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
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, pyqtSlot, QObject, pyqtSignal, Qt
from PyQt5.QtGui import QIcon

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
    
    def __init__(self):
        super().__init__()
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
    
    @pyqtSlot(str, str, int, float, float, float, float, float, str, float, str, bool, result=str)
    def save_assessment(self, patient_id, health_worker, age, bmi, systolic, 
                        diastolic, blood_sugar, hemoglobin, risk_level, 
                        confidence, model_used, lab_available):
        """Save assessment to CSV"""
        # Add debug print
        print(f"\n{'='*60}")
        print(f"save_assessment CALLED")
        print(f"patient_id: {patient_id!r} ({type(patient_id).__name__})")
        print(f"health_worker: {health_worker!r} ({type(health_worker).__name__})")
        print(f"age: {age!r} ({type(age).__name__})")
        print(f"bmi: {bmi!r} ({type(bmi).__name__})")
        print(f"lab_available: {lab_available!r} ({type(lab_available).__name__})")
        print(f"{'='*60}\n")
        
        try:
            record = {
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Patient_ID': patient_id if patient_id else 'N/A',
                'Age': int(age),
                'BMI': float(bmi),
                'SystolicBP': float(systolic),
                'DiastolicBP': float(diastolic),
                'Blood_Sugar': float(blood_sugar) if lab_available else None,
                'Hemoglobin': float(hemoglobin) if lab_available else None,
                'Risk_Level': risk_level,
                'Confidence': f"{confidence:.1f}%",
                'Model_Used': model_used,
                'Lab_Available': 'Yes' if lab_available else 'No',
                'Health_Worker': health_worker if health_worker else 'N/A'
            }
            
            history_file = 'assessment_history.csv'
            if os.path.exists(history_file):
                df = pd.read_csv(history_file)
                df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
            else:
                df = pd.DataFrame([record])
            
            df.to_csv(history_file, index=False, na_rep='N/A')
            
            print(f"✓ Assessment saved: Patient {patient_id}")
            return json.dumps({'success': True, 'message': 'Assessment saved successfully'})
            
        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            print(f"✗ Save error: {error_msg}")
            return json.dumps({'success': False, 'error': str(e)})
    
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" ")
        self.setGeometry(100, 50, 1400, 900)
        
        # Set window icon
        if os.path.exists('assets/icon.png'):
            self.setWindowIcon(QIcon('assets/icon.png'))
        
        # Apply modern healthcare title bar
        self.apply_modern_titlebar()
        
        # Create web view
        self.browser = QWebEngineView()
        
        # Set up Python ↔ JavaScript bridge
        self.backend = Backend()
        self.channel = QWebChannel()
        self.channel.registerObject('backend', self.backend)
        self.browser.page().setWebChannel(self.channel)
        
        # Load local HTML UI
        html_path = os.path.join(os.getcwd(), 'ui', 'index.html')
        self.browser.load(QUrl.fromLocalFile(html_path))
        self.browser.page().profile().clearHttpCache()  
        
        self.setCentralWidget(self.browser)
    
    def apply_modern_titlebar(self):
        """Apply modern healthcare-style title bar with light teal color"""
        try:
            if sys.platform == 'win32':
                try:
                    from ctypes import windll, c_int, byref, sizeof
                    from ctypes.wintypes import DWORD
                    
                    hwnd = int(self.winId())
                    
                    # Light Teal Title Bar - RGB: #E3F5F4 = BGR: 0x00F4F5E3
                    # This complements your #36ABA3 sidebar perfectly
                    color = DWORD(0x00F4F5E3)
                    
                    # Apply custom title bar color
                    windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, byref(color), sizeof(color))
                    
                    # Use light mode for dark text on light background
                    light_mode = c_int(0)
                    windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, byref(light_mode), sizeof(light_mode))
                    
                    print("✓ Modern healthcare title bar applied (Light Teal)")
                except Exception as e:
                    print(f"Note: Could not apply custom title bar: {e}")
        except Exception as e:
            print(f"Note: Modern styling not available: {e}")


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