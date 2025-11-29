"""
MATERNAL RISK ASSESSMENT SYSTEM - Hybrid Architecture
PyQt5 + QWebEngineView for modern UI
"""

import sys
import os
import pickle
import json
import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, pyqtSlot, QObject, pyqtSignal

class Backend(QObject):
    """Python backend - handles all ML logic and data operations"""
    
    # Signals to send data to frontend
    results_ready = pyqtSignal(str)  # Send results as JSON string
    
    def __init__(self):
        super().__init__()
        self.load_models()
        self.risk_labels = {0: 'Low', 1: 'Moderate', 2: 'High'}
    
    def load_models(self):
        """Load ML models - same as your original code"""
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
            # Calculate BMI
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            
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
            
            # Helper function to convert numpy/pandas types to Python native types
            def safe_float(value):
                """Convert to float and handle NaN"""
                try:
                    val = float(value)
                    # Replace NaN with 0 or None
                    return 0.0 if (val != val) else val  # NaN != NaN is True
                except:
                    return 0.0
            
            # Prepare result as JSON with safe conversions
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
            
            print(f"✓ Assessment complete: {risk_level} ({confidence:.1f}%)")
            print(f"  Probabilities - Low: {result['probabilities']['low']:.1f}%, Moderate: {result['probabilities']['moderate']:.1f}%, High: {result['probabilities']['high']:.1f}%")
            
            return json.dumps(result)
            
        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            print(f"✗ Assessment error: {error_msg}")
            return json.dumps({'error': str(e)})
    
    @pyqtSlot(str, str, int, float, float, float, float, float, str, float, str, bool, result=str)
    def save_assessment(self, patient_id, health_worker, age, bmi, systolic, 
                    diastolic, blood_sugar, hemoglobin, risk_level, 
                    confidence, model_used, lab_available):
        """Save assessment to CSV - returns success message"""
        try:
            record = {
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Patient_ID': patient_id or 'N/A',
                'Age': age,
                'BMI': float(bmi),
                'SystolicBP': float(systolic),
                'DiastolicBP': float(diastolic),
                'Blood_Sugar': float(blood_sugar) if lab_available else 'N/A',
                'Hemoglobin': float(hemoglobin) if lab_available else 'N/A',
                'Risk_Level': risk_level,
                'Confidence': f"{confidence:.1f}%",
                'Model_Used': model_used,
                'Lab_Available': 'Yes' if lab_available else 'No',
                'Health_Worker': health_worker or 'N/A'
            }
            
            history_file = 'assessment_history.csv'
            if os.path.exists(history_file):
                df = pd.read_csv(history_file)
                df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
            else:
                df = pd.DataFrame([record])
            df.to_csv(history_file, index=False)
            
            print(f"✓ Assessment saved: Patient {patient_id}")
            return json.dumps({'success': True, 'message': 'Assessment saved successfully'})
            
        except Exception as e:
            print(f"✗ Save error: {e}")
            return json.dumps({'success': False, 'error': str(e)})
    
    @pyqtSlot(result=str)
    def load_history(self):
        """Load assessment history as JSON"""
        try:
            if not os.path.exists('assessment_history.csv'):
                return json.dumps([])
            
            df = pd.read_csv('assessment_history.csv')
            # Convert to list of dicts
            records = df.to_dict('records')
            return json.dumps(records)
            
        except Exception as e:
            print(f"Error loading history: {e}")
            return json.dumps([])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maternal Risk Assessment System")
        self.setGeometry(100, 50, 1400, 900)
        
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
        
        self.setCentralWidget(self.browser)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()