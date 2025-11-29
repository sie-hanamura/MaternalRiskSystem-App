// Initialize Python backend connection
let backend = null;

new QWebChannel(qt.webChannelTransport, function(channel) {
    backend = channel.objects.backend;
    console.log("✓ Connected to Python backend");
    initializeApp();
});

// Initialize application
function initializeApp() {
    // Set current date
    document.getElementById('current-date').textContent = 
        new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    
    // Navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => switchView(btn.dataset.view));
    });
    
    // BMI calculation
    document.getElementById('weight').addEventListener('input', calculateBMI);
    document.getElementById('height').addEventListener('input', calculateBMI);
    
    // Lab toggle
    document.getElementById('lab-available').addEventListener('change', toggleLabInputs);
    
    // Calculate button
    document.getElementById('calculate-btn').addEventListener('click', calculateRisk);
    
    // Action buttons
    document.getElementById('save-btn').addEventListener('click', saveAssessment);
    document.getElementById('print-btn').addEventListener('click', printReport);
    document.getElementById('new-btn').addEventListener('click', newAssessment);
    document.getElementById('export-btn').addEventListener('click', exportHistory);
    
    // Initial BMI calculation
    calculateBMI();
}

// Switch between views
function switchView(viewName) {
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.view === viewName);
    });
    
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });
    document.getElementById(`${viewName}-view`).classList.add('active');
    
    if (viewName === 'history') {
        loadHistory();
    }
}

// Calculate BMI
function calculateBMI() {
    const weight = parseFloat(document.getElementById('weight').value);
    const height = parseFloat(document.getElementById('height').value) / 100;
    
    if (weight && height > 0) {
        const bmi = weight / (height * height);
        document.getElementById('bmi-value').textContent = bmi.toFixed(1);
        
        let status, className;
        if (bmi < 18.5) {
            status = '⚠️ Underweight';
            className = 'warning';
        } else if (bmi < 25) {
            status = '✅ Normal';
            className = 'normal';
        } else if (bmi < 30) {
            status = '⚠️ Overweight';
            className = 'warning';
        } else {
            status = '🚨 Obese';
            className = 'danger';
        }
        
        const statusEl = document.getElementById('bmi-status');
        statusEl.textContent = status;
        statusEl.className = `bmi-status ${className}`;
    }
}

// Toggle lab inputs
function toggleLabInputs() {
    const labAvailable = document.getElementById('lab-available').checked;
    const labInputs = document.getElementById('lab-inputs');
    labInputs.style.display = labAvailable ? 'grid' : 'none';
    
    document.getElementById('blood-sugar').disabled = !labAvailable;
    document.getElementById('hemoglobin').disabled = !labAvailable;
    
    // Update model indicator
    const indicator = document.getElementById('model-indicator');
    if (labAvailable) {
        indicator.innerHTML = '<span class="info-icon">ℹ️</span> Using: Full Model (5 features) - 90.6% accuracy';
    } else {
        indicator.innerHTML = '<span class="info-icon">ℹ️</span> Using: Basic Model (3 features) - ~85% accuracy';
    }
}

// Calculate risk
function calculateRisk() {
    const btn = document.getElementById('calculate-btn');
    btn.textContent = '🔄 Calculating...';
    btn.disabled = true;
    
    try {
        const age = parseFloat(document.getElementById('age').value);
        const weight = parseFloat(document.getElementById('weight').value);
        const height = parseFloat(document.getElementById('height').value);
        const systolic = parseFloat(document.getElementById('systolic').value);
        const diastolic = parseFloat(document.getElementById('diastolic').value);
        const bloodSugar = parseFloat(document.getElementById('blood-sugar').value);
        const hemoglobin = parseFloat(document.getElementById('hemoglobin').value);
        const labAvailable = document.getElementById('lab-available').checked;
        
        backend.assess_risk(age, weight, height, systolic, diastolic, 
                           bloodSugar, hemoglobin, labAvailable, function(resultJson) {
            const result = JSON.parse(resultJson);
            
            if (result.error) {
                alert('Error: ' + result.error);
                btn.textContent = 'Calculate Risk Assessment';
                btn.disabled = false;
                return;
            }
            
            window.currentAssessment = result;
            displayResults(result);
            btn.textContent = 'Calculate Risk Assessment';
            btn.disabled = false;
        });
        
    } catch (error) {
        alert('Error calculating risk: ' + error);
        btn.textContent = 'Calculate Risk Assessment';
        btn.disabled = false;
    }
}

// Display results
function displayResults(result) {
    document.getElementById('results-card').style.display = 'block';
    
    // Risk level with icon
    const icons = { 'Low': '✅', 'Moderate': '⚠️', 'High': '🚨' };
    const riskEl = document.getElementById('risk-level');
    riskEl.textContent = `${icons[result.risk_level]} ${result.risk_level.toUpperCase()} RISK`;
    riskEl.className = `risk-level ${result.risk_level.toLowerCase()}`;
    
    // Update gauge
    updateGauge(result.confidence, result.risk_level);
    
    // Update probability bars
    updateProbabilities(result.probabilities);
    
    // Update recommendations
    updateRecommendations(result);
    
    // Scroll to results
    document.querySelector('.right-column').scrollIntoView({ behavior: 'smooth' });
}

// Update gauge
function updateGauge(percentage, riskLevel) {
    document.getElementById('gauge-percentage').textContent = `${Math.round(percentage)}%`;
    
    const colors = {
        'Low': '#10b981',
        'Moderate': '#f59e0b',
        'High': '#ef4444'
    };
    
    const gaugeFill = document.getElementById('gauge-fill');
    const gaugePercentage = document.getElementById('gauge-percentage');
    const color = colors[riskLevel] || colors.Low;
    
    gaugeFill.style.stroke = color;
    gaugePercentage.style.color = color;
    
    const circumference = 251.2;
    const offset = circumference - (percentage / 100) * circumference;
    
    gaugeFill.style.strokeDasharray = `${circumference} ${circumference}`;
    gaugeFill.style.strokeDashoffset = circumference;
    
    setTimeout(() => {
        gaugeFill.style.strokeDashoffset = offset;
    }, 100);
}

// Update probabilities
function updateProbabilities(probs) {
    document.getElementById('prob-low').textContent = `${probs.low.toFixed(1)}%`;
    document.getElementById('prob-moderate').textContent = `${probs.moderate.toFixed(1)}%`;
    document.getElementById('prob-high').textContent = `${probs.high.toFixed(1)}%`;
    
    document.getElementById('prob-bar-low').style.width = `${probs.low}%`;
    document.getElementById('prob-bar-moderate').style.width = `${probs.moderate}%`;
    document.getElementById('prob-bar-high').style.width = `${probs.high}%`;
}

// Update recommendations (FROM YOUR ORIGINAL CODE)
function updateRecommendations(result) {
    const recDiv = document.getElementById('recommendations');
    const probs = result.probabilities;
    
    if (result.risk_level === 'Low') {
        recDiv.innerHTML = `
            <h4 style="color: #10b981;">✅ Low Risk - Routine Care</h4>
            <ul>
                <li><b>Continue regular prenatal checkups</b> (monthly)</li>
                <li>Maintain healthy diet and moderate exercise</li>
                <li>Monitor for any changes in symptoms</li>
                <li>Return immediately if any warning signs appear</li>
                <li>Next checkup: Schedule in 4 weeks</li>
            </ul>
            <p style="font-style: italic; color: #10b981;">✓ Patient can be managed at barangay health center level.</p>
        `;
    } else if (result.risk_level === 'Moderate') {
        recDiv.innerHTML = `
            <h4 style="color: #f59e0b;">⚠️ Moderate Risk - Enhanced Monitoring</h4>
            <ul>
                <li><b>Refer to Rural Health Unit (RHU)</b> for evaluation</li>
                <li>Increase prenatal visits (bi-weekly or as advised)</li>
                <li>Monitor blood pressure and blood sugar regularly</li>
                <li>Educate on warning signs to watch for</li>
                <li>May need additional tests or specialist consultation</li>
            </ul>
            <p style="font-style: italic; color: #f59e0b;">⚠️ Coordinate with RHU midwife or physician for management plan.</p>
        `;
    } else {
        recDiv.innerHTML = `
            <h4 style="color: #ef4444;">🚨 High Risk - URGENT REFERRAL NEEDED</h4>
            <ul>
                <li><b style="color: #dc2626;">IMMEDIATE referral to hospital/OB-GYN</b></li>
                <li>Patient needs specialist care and close monitoring</li>
                <li>High-risk pregnancy requiring advanced interventions</li>
                <li>Weekly or more frequent prenatal visits required</li>
                <li>Prepare for potential complications</li>
            </ul>
            <p><b style="color: #dc2626;">⚠️ DO NOT DELAY: Refer to nearest hospital with OB-GYN services immediately.</b></p>
        `;
    }
}

// Save assessment
function saveAssessment() {
    if (!window.currentAssessment) {
        alert('No assessment to save');
        return;
    }
    
    const patientId = document.getElementById('patient-id').value || 'N/A';
    const healthWorker = document.getElementById('health-worker').value || 'N/A';
    const age = parseInt(document.getElementById('age').value);
    const result = window.currentAssessment;
    
    backend.save_assessment(
        patientId, healthWorker, age, result.bmi,
        parseFloat(document.getElementById('systolic').value),
        parseFloat(document.getElementById('diastolic').value),
        parseFloat(document.getElementById('blood-sugar').value),
        parseFloat(document.getElementById('hemoglobin').value),
        result.risk_level, result.confidence, result.model_used,
        result.lab_available,
        function(response) {
            const res = JSON.parse(response);
            if (res.success) {
                alert('✓ Assessment saved successfully!');
            } else {
                alert('Error: ' + res.error);
            }
        }
    );
}

// Print report
function printReport() {
    window.print();
}

// New assessment
function newAssessment() {
    document.getElementById('patient-id').value = '';
    document.getElementById('health-worker').value = '';
    document.getElementById('age').value = '25';
    document.getElementById('weight').value = '60';
    document.getElementById('height').value = '160';
    document.getElementById('systolic').value = '120';
    document.getElementById('diastolic').value = '80';
    document.getElementById('blood-sugar').value = '5.5';
    document.getElementById('hemoglobin').value = '12.0';
    document.getElementById('lab-available').checked = true;
    
    document.getElementById('results-card').style.display = 'none';
    calculateBMI();
    window.scrollTo(0, 0);
}

// Load history
function loadHistory() {
    backend.load_history(function(historyJson) {
        const records = JSON.parse(historyJson);
        const tbody = document.getElementById('history-tbody');
        
        tbody.innerHTML = records.map(record => {
            const riskClass = record.Risk_Level.toLowerCase();
            return `
                <tr>
                    <td>${record.Timestamp}</td>
                    <td>${record.Patient_ID}</td>
                    <td>${record.Age}</td>
                    <td>${parseFloat(record.BMI).toFixed(1)}</td>
                    <td><span class="risk-badge ${riskClass}">${record.Risk_Level}</span></td>
                    <td>${record.Confidence}</td>
                    <td>${record.Model_Used}</td>
                    <td>${record.Health_Worker}</td>
                </tr>
            `;
        }).join('');
    });
}

// Export history
function exportHistory() {
    alert('Export feature: Use the Python application menu to export CSV files.');
}