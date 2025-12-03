// ============================================
// LANGUAGE TRANSLATION SYSTEM
// ============================================

// Current language (default: English)
let currentLanguage = localStorage.getItem('language') || 'en';

// Comprehensive translation dictionary
const translations = {
    en: {
        // Header
        'app-title': 'MATERNAL RISK ASSESSMENT SYSTEM',
        'app-subtitle': 'Municipal Health Office Bay, Laguna | AI-Assisted Screening Tool',

        // Settings
        'settings-language': 'Language',
        'lang-english': 'English',
        'lang-filipino': 'Filipino',

        // Navigation
        'nav-new-assessment': 'New Assessment',
        'nav-dashboard': 'Dashboard',
        'nav-history': 'History',
        'nav-about': 'About',

        // Patient Information
        'patient-info-title': 'Patient Information',
        'label-patient-id': 'Patient ID',
        'label-health-worker': 'Health Worker',
        'placeholder-patient-id': 'e.g., P-2024-001',
        'placeholder-health-worker': 'Your name',

        // Clinical Measurements
        'clinical-measurements-title': 'Clinical Measurements',
        'label-age': 'Age (years)',
        'hint-age': 'Normal: 18-35',
        'label-weight': 'Weight (kg)',
        'label-height': 'Height (cm)',
        'label-systolic': 'Systolic BP (mmHg)',
        'hint-systolic': 'Normal: 90-120',
        'label-diastolic': 'Diastolic BP (mmHg)',
        'hint-diastolic': 'Normal: 60-80',

        // BMI Status
        'bmi-normal': 'Normal',
        'bmi-underweight': 'Underweight',
        'bmi-overweight': 'Overweight',
        'bmi-obese': 'Obese',

        // Laboratory
        'lab-results-title': 'Laboratory Test Results',
        'lab-available-text': 'Laboratory results available',
        'label-blood-sugar': 'Blood Sugar (mmol/L)',
        'hint-blood-sugar': 'Normal: 4.0-7.0',
        'label-hemoglobin': 'Hemoglobin (g/dL)',
        'hint-hemoglobin': 'Normal: 11.0-14.0',

        // Model Indicator
        'model-full': 'Using: Full Model (5 features) - 90.6% accuracy',
        'model-basic': 'Using: Basic Model (3 features) - ~85% accuracy',

        // Buttons
        'btn-calculate': 'Calculate Risk Assessment',
        'btn-calculating': '🔄 Calculating...',
        'btn-save': '💾 Save Assessment',
        'btn-print': '🖨️ Print Report',
        'btn-new': '📝 New Assessment',
        'btn-export': '📥 Export to CSV',

        // Results
        'results-title': 'Assessment Results',
        'confidence-level': 'Confidence Level',
        'probability-breakdown': 'Probability Breakdown',
        'prob-low-risk': '✅ Low Risk',
        'prob-moderate-risk': '⚠️ Moderate Risk',
        'prob-high-risk': '🚨 High Risk',
        'recommended-actions': 'Recommended Actions',

        // Risk Levels (for display)
        'risk-low': 'LOW RISK',
        'risk-moderate': 'MODERATE RISK',
        'risk-high': 'HIGH RISK',

        // History
        'history-title': '📊 Assessment History',
        'table-datetime': 'Date/Time',
        'table-patient-id': 'Patient ID',
        'table-age': 'Age',
        'table-risk-level': 'Risk Level',
        'table-confidence': 'Confidence',
        'table-model-used': 'Model Used',
        'table-health-worker': 'Health Worker',

        // Recommendations (Low Risk)
        'rec-low-title': '✅ Low Risk - Routine Care',
        'rec-low-1': '<b>Continue regular prenatal checkups</b> (monthly)',
        'rec-low-2': 'Maintain healthy diet and moderate exercise',
        'rec-low-3': 'Monitor for any changes in symptoms',
        'rec-low-4': 'Return immediately if any warning signs appear',
        'rec-low-5': 'Next checkup: Schedule in 4 weeks',
        'rec-low-note': '✓ Patient can be managed at barangay health center level.',

        // Recommendations (Moderate Risk)
        'rec-moderate-title': '⚠️ Moderate Risk - Enhanced Monitoring',
        'rec-moderate-1': '<b>Refer to Rural Health Unit (RHU)</b> for evaluation',
        'rec-moderate-2': 'Increase prenatal visits (bi-weekly or as advised)',
        'rec-moderate-3': 'Monitor blood pressure and blood sugar regularly',
        'rec-moderate-4': 'Educate on warning signs to watch for',
        'rec-moderate-5': 'May need additional tests or specialist consultation',
        'rec-moderate-note': '⚠️ Coordinate with RHU midwife or physician for management plan.',

        // Recommendations (High Risk)
        'rec-high-title': '🚨 High Risk - URGENT REFERRAL NEEDED',
        'rec-high-1': '<b style="color: #dc2626;">IMMEDIATE referral to hospital/OB-GYN</b>',
        'rec-high-2': 'Patient needs specialist care and close monitoring',
        'rec-high-3': 'High-risk pregnancy requiring advanced interventions',
        'rec-high-4': 'Weekly or more frequent prenatal visits required',
        'rec-high-5': 'Prepare for potential complications',
        'rec-high-note': '⚠️ DO NOT DELAY: Refer to nearest hospital with OB-GYN services immediately.',

        // Dashboard
        'dashboard-total-assessments': 'Total assessments conducted',
        'dashboard-high-risk': 'Patients requiring immediate referral',
        'dashboard-avg-confidence': 'Average prediction confidence',
        'dashboard-recent-activity': 'Assessments this week',
        'dashboard-risk-distribution': 'Risk Level Distribution',
        'dashboard-assessments-over-time': 'Assessments Over Time',
        'dashboard-risk-factors': 'Most Common Risk Factors',
        'dashboard-risk-factor': 'Risk Factor',
        'dashboard-count': 'Count',
        'dashboard-percentage': 'Percentage',
        'dashboard-no-data': 'No data available'
    },

    fil: {
        // Header
        'app-title': 'SISTEMA NG PAGSUSURI SA PANGANIB SA INA',
        'app-subtitle': 'Tanggapan ng Kalusugan ng Bayan ng Bay, Laguna | Kagamitang Pandagdag ng AI',

        // Settings
        'settings-language': 'Wika',
        'lang-english': 'Ingles',
        'lang-filipino': 'Filipino',

        // Navigation
        'nav-new-assessment': 'Bagong Pagsusuri',
        'nav-dashboard': 'Dashboard',
        'nav-history': 'Kasaysayan',
        'nav-about': 'Tungkol',

        // Patient Information
        'patient-info-title': 'Impormasyon ng Pasyente',
        'label-patient-id': 'Patient ID',
        'label-health-worker': 'Manggagawa ng Kalusugan',
        'placeholder-patient-id': 'hal., P-2024-001',
        'placeholder-health-worker': 'Iyong pangalan',

        // Clinical Measurements
        'clinical-measurements-title': 'Mga Sukat sa Klinika',
        'label-age': 'Edad (taon)',
        'hint-age': 'Normal: 18-35',
        'label-weight': 'Timbang (kg)',
        'label-height': 'Taas (cm)',
        'label-systolic': 'Systolic BP (mmHg)',
        'hint-systolic': 'Normal: 90-120',
        'label-diastolic': 'Diastolic BP (mmHg)',
        'hint-diastolic': 'Normal: 60-80',

        // BMI Status
        'bmi-normal': 'Normal',
        'bmi-underweight': 'Kulang sa Timbang',
        'bmi-overweight': 'Labis sa Timbang',
        'bmi-obese': 'Sobra sa Timbang',

        // Laboratory
        'lab-results-title': 'Resulta ng Laboratoryo',
        'lab-available-text': 'May resulta ng laboratoryo',
        'label-blood-sugar': 'Asukal sa Dugo (mmol/L)',
        'hint-blood-sugar': 'Normal: 4.0-7.0',
        'label-hemoglobin': 'Hemoglobina (g/dL)',
        'hint-hemoglobin': 'Normal: 11.0-14.0',

        // Model Indicator
        'model-full': 'Ginagamit: Kumpletong Modelo (5 features) - 90.6% kawastuhan',
        'model-basic': 'Ginagamit: Pangunahing Modelo (3 features) - ~85% kawastuhan',

        // Buttons
        'btn-calculate': 'Kalkulahin ang Pagsusuri sa Panganib',
        'btn-calculating': '🔄 Kinakalkula...',
        'btn-save': '💾 I-save ang Pagsusuri',
        'btn-print': '🖨️ I-print ang Ulat',
        'btn-new': '📝 Bagong Pagsusuri',
        'btn-export': '📥 I-export sa CSV',

        // Results
        'results-title': 'Resulta ng Pagsusuri',
        'confidence-level': 'Antas ng Katiyakan',
        'probability-breakdown': 'Detalye ng Posibilidad',
        'prob-low-risk': '✅ Mababang Panganib',
        'prob-moderate-risk': '⚠️ Katamtamang Panganib',
        'prob-high-risk': '🚨 Mataas na Panganib',
        'recommended-actions': 'Mga Inirerekomendang Aksyon',

        // Risk Levels (for display)
        'risk-low': 'MABABANG PANGANIB',
        'risk-moderate': 'KATAMTAMANG PANGANIB',
        'risk-high': 'MATAAS NA PANGANIB',

        // History
        'history-title': '📊 Kasaysayan ng Pagsusuri',
        'table-datetime': 'Petsa/Oras',
        'table-patient-id': 'Patient ID',
        'table-age': 'Edad',
        'table-risk-level': 'Antas ng Panganib',
        'table-confidence': 'Katiyakan',
        'table-model-used': 'Modelo na Ginamit',
        'table-health-worker': 'Manggagawa ng Kalusugan',

        // Recommendations (Low Risk)
        'rec-low-title': '✅ Mababang Panganib - Karaniwang Pag-aalaga',
        'rec-low-1': '<b>Magpatuloy sa regular na prenatal checkup</b> (buwanan)',
        'rec-low-2': 'Panatilihin ang malusog na pagkain at katamtamang ehersisyo',
        'rec-low-3': 'Bantayan ang anumang pagbabago sa mga sintomas',
        'rec-low-4': 'Bumalik kaagad kung may lumilitaw na babala',
        'rec-low-5': 'Susunod na checkup: Mag-iskedyul sa loob ng 4 na linggo',
        'rec-low-note': '✓ Maaaring pangasiwaan ang pasyente sa antas ng barangay health center.',

        // Recommendations (Moderate Risk)
        'rec-moderate-title': '⚠️ Katamtamang Panganib - Dagdag na Pagsubaybay',
        'rec-moderate-1': '<b>Dalhin sa Rural Health Unit (RHU)</b> para sa evaluasyon',
        'rec-moderate-2': 'Dagdagan ang prenatal visits (tuwing dalawang linggo o ayon sa payo)',
        'rec-moderate-3': 'Regular na bantayan ang presyon ng dugo at asukal sa dugo',
        'rec-moderate-4': 'Turuan tungkol sa mga senyales ng panganib na dapat bantayan',
        'rec-moderate-5': 'Maaaring kailanganin ng dagdag na pagsusuri o konsultasyon sa espesyalista',
        'rec-moderate-note': '⚠️ Makipagtulungan sa midwife o doktor ng RHU para sa plano ng pangangalaga.',

        // Recommendations (High Risk)
        'rec-high-title': '🚨 Mataas na Panganib - KAILANGAN NG AGARANG REFERRAL',
        'rec-high-1': '<b style="color: #dc2626;">AGARANG dalhin sa ospital/OB-GYN</b>',
        'rec-high-2': 'Kailangan ng pasyente ng pag-aalaga ng espesyalista at malapit na pagsubaybay',
        'rec-high-3': 'Pagbubuntis na may mataas na panganib na nangangailangan ng advanced na interbensyon',
        'rec-high-4': 'Kailangan ng lingguhang o mas madalas na prenatal visits',
        'rec-high-5': 'Maghanda para sa mga posibleng komplikasyon',
        'rec-high-note': '⚠️ HUWAG MAGPABAYA: Dalhin kaagad sa pinakamalapit na ospital na may serbisyo ng OB-GYN.',

        // Dashboard
        'dashboard-total-assessments': 'Kabuuang pagsusuring isinagawa',
        'dashboard-high-risk': 'Pasyenteng nangangailangan ng agarang referral',
        'dashboard-avg-confidence': 'Average na katiyakan ng prediction',
        'dashboard-recent-activity': 'Pagsusuri ngayong linggo',
        'dashboard-risk-distribution': 'Distribusyon ng Antas ng Panganib',
        'dashboard-assessments-over-time': 'Pagsusuri sa Paglipas ng Panahon',
        'dashboard-risk-factors': 'Pinaka-Karaniwang Risk Factors',
        'dashboard-risk-factor': 'Risk Factor',
        'dashboard-count': 'Bilang',
        'dashboard-percentage': 'Porsyento',
        'dashboard-no-data': 'Walang available na data'
    }
};

// Function to update all text based on current language
function updateLanguage() {
    const lang = currentLanguage;

    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[lang][key]) {
            element.innerHTML = translations[lang][key];
        }
    });

    // Update all placeholders with data-i18n-placeholder attribute
    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        if (translations[lang][key]) {
            element.placeholder = translations[lang][key];
        }
    });

    // Update checkmarks in dropdown
    updateLanguageCheckmarks();

    // Update current date display with correct locale
    const dateEl = document.getElementById('current-date');
    if (dateEl) {
        const locale = lang === 'en' ? 'en-US' : 'fil-PH';
        dateEl.textContent = new Date().toLocaleDateString(locale, {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    // Save language preference
    localStorage.setItem('language', lang);
}

// Function to update language checkmarks
function updateLanguageCheckmarks() {
    const checkEn = document.getElementById('check-en');
    const checkFil = document.getElementById('check-fil');

    if (currentLanguage === 'en') {
        checkEn.classList.add('visible');
        checkFil.classList.remove('visible');
    } else {
        checkEn.classList.remove('visible');
        checkFil.classList.add('visible');
    }
}

// Function to switch language
function switchLanguage(lang) {
    if (lang === currentLanguage) return;

    currentLanguage = lang;
    updateLanguage();

    // Re-update model indicator based on current state
    const labAvailable = document.getElementById('lab-available').checked;
    const indicator = document.getElementById('model-indicator');
    const iconImg = '<img src="../assets/info-circle.png" alt="" class="info-icon" style="width: 16px; height: 16px; margin-right: 12px;">';

    if (labAvailable) {
        indicator.innerHTML = iconImg + '<span data-i18n="model-full">' + translations[currentLanguage]['model-full'] + '</span>';
    } else {
        indicator.innerHTML = iconImg + '<span data-i18n="model-basic">' + translations[currentLanguage]['model-basic'] + '</span>';
    }

    // Re-update BMI status if visible
    const bmiStatus = document.getElementById('bmi-status');
    if (bmiStatus && bmiStatus.textContent) {
        calculateBMI(); // Recalculate to update status text
    }

    // Close dropdown after selection
    closeSettingsDropdown();
}

// Function to toggle settings dropdown
function toggleSettingsDropdown() {
    const dropdown = document.getElementById('settings-dropdown');
    dropdown.classList.toggle('active');
}

// Function to close settings dropdown
function closeSettingsDropdown() {
    const dropdown = document.getElementById('settings-dropdown');
    dropdown.classList.remove('active');
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const settingsContainer = document.querySelector('.settings-container');
    const dropdown = document.getElementById('settings-dropdown');

    if (settingsContainer && dropdown && !settingsContainer.contains(event.target)) {
        closeSettingsDropdown();
    }
});

// Initialize Python backend connection
let backend = null;

new QWebChannel(qt.webChannelTransport, function(channel) {
    backend = channel.objects.backend;
    console.log("✓ Connected to Python backend");
    initializeApp();
});

// Initialize application
function initializeApp() {
    // Initialize language on app load
    updateLanguage();

    // Custom title bar window controls
    document.getElementById('titlebar-minimize').addEventListener('click', () => {
        if (backend) {
            backend.minimize_window();
        }
    });

    document.getElementById('titlebar-maximize').addEventListener('click', () => {
        if (backend) {
            backend.maximize_window();
        }
    });

    document.getElementById('titlebar-close').addEventListener('click', () => {
        if (backend) {
            backend.close_window();
        }
    });

    // Title bar dragging
    const dragRegion = document.querySelector('.titlebar-drag-region');
    let isDragging = false;

    dragRegion.addEventListener('mousedown', (e) => {
        isDragging = true;
        if (backend) {
            backend.start_window_drag(e.clientX, e.clientY);
        }
    });

    document.addEventListener('mousemove', (e) => {
        if (isDragging && backend) {
            backend.move_window(e.screenX, e.screenY);
        }
    });

    document.addEventListener('mouseup', () => {
        isDragging = false;
    });

    // Settings dropdown button
    document.getElementById('settings-btn').addEventListener('click', function(e) {
        e.stopPropagation();
        toggleSettingsDropdown();
    });

    // Language selection buttons
    document.getElementById('lang-en').addEventListener('click', () => switchLanguage('en'));
    document.getElementById('lang-fil').addEventListener('click', () => switchLanguage('fil'));

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
    } else if (viewName === 'dashboard') {
        loadDashboard();
    } else if (viewName === 'about') {
        // Initialize feature importance chart when About view loads
        setTimeout(() => {
            initFeatureImportanceChart();
        }, 100);
    }
}

// Calculate BMI
function calculateBMI() {
    const weight = parseFloat(document.getElementById('weight').value);
    const height = parseFloat(document.getElementById('height').value) / 100;

    if (weight && height > 0) {
        const bmi = weight / (height * height);
        document.getElementById('bmi-value').textContent = bmi.toFixed(1);

        let statusKey, className;
        if (bmi < 18.5) {
            statusKey = 'bmi-underweight';
            className = 'warning';
        } else if (bmi < 25) {
            statusKey = 'bmi-normal';
            className = 'normal';
        } else if (bmi < 30) {
            statusKey = 'bmi-overweight';
            className = 'warning';
        } else {
            statusKey = 'bmi-obese';
            className = 'danger';
        }

        const statusEl = document.getElementById('bmi-status');
        const icon = className === 'normal' ? '✅' : (className === 'danger' ? '🚨' : '⚠️');
        statusEl.textContent = icon + ' ' + translations[currentLanguage][statusKey];
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

    // Update model indicator with translation and class
    const indicator = document.getElementById('model-indicator');
    const iconImg = '<img src="../assets/info-circle.png" alt="" class="info-icon" style="width: 16px; height: 16px; margin-right: 12px;">';

    if (labAvailable) {
        indicator.className = 'model-indicator full';
        indicator.innerHTML = iconImg + '<span data-i18n="model-full">' + translations[currentLanguage]['model-full'] + '</span>';
    } else {
        indicator.className = 'model-indicator basic';
        indicator.innerHTML = iconImg + '<span data-i18n="model-basic">' + translations[currentLanguage]['model-basic'] + '</span>';
    }
}

// Calculate risk
function calculateRisk() {
    const btn = document.getElementById('calculate-btn');
    btn.textContent = translations[currentLanguage]['btn-calculating'];
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
                btn.textContent = translations[currentLanguage]['btn-calculate'];
                btn.disabled = false;
                return;
            }

            window.currentAssessment = result;
            displayResults(result);
            btn.textContent = translations[currentLanguage]['btn-calculate'];
            btn.disabled = false;
        });
        
    } catch (error) {
        alert('Error calculating risk: ' + error);
        btn.textContent = translations[currentLanguage]['btn-calculate'];
        btn.disabled = false;
    }
}

// Display results
function displayResults(result) {
    document.getElementById('results-card').style.display = 'block';

    // Risk level with icon and translation
    const icons = { 'Low': '✅', 'Moderate': '⚠️', 'High': '🚨' };
    const riskKeys = { 'Low': 'risk-low', 'Moderate': 'risk-moderate', 'High': 'risk-high' };
    const riskEl = document.getElementById('risk-level');
    riskEl.textContent = `${icons[result.risk_level]} ${translations[currentLanguage][riskKeys[result.risk_level]]}`;
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

// Update recommendations
function updateRecommendations(result) {
    const recDiv = document.getElementById('recommendations');
    const lang = currentLanguage;

    if (result.risk_level === 'Low') {
        recDiv.innerHTML = `
            <h4 style="color: #10b981;">${translations[lang]['rec-low-title']}</h4>
            <ul>
                <li>${translations[lang]['rec-low-1']}</li>
                <li>${translations[lang]['rec-low-2']}</li>
                <li>${translations[lang]['rec-low-3']}</li>
                <li>${translations[lang]['rec-low-4']}</li>
                <li>${translations[lang]['rec-low-5']}</li>
            </ul>
            <p style="font-style: italic; color: #10b981;">${translations[lang]['rec-low-note']}</p>
        `;
    } else if (result.risk_level === 'Moderate') {
        recDiv.innerHTML = `
            <h4 style="color: #f59e0b;">${translations[lang]['rec-moderate-title']}</h4>
            <ul>
                <li>${translations[lang]['rec-moderate-1']}</li>
                <li>${translations[lang]['rec-moderate-2']}</li>
                <li>${translations[lang]['rec-moderate-3']}</li>
                <li>${translations[lang]['rec-moderate-4']}</li>
                <li>${translations[lang]['rec-moderate-5']}</li>
            </ul>
            <p style="font-style: italic; color: #f59e0b;">${translations[lang]['rec-moderate-note']}</p>
        `;
    } else {
        recDiv.innerHTML = `
            <h4 style="color: #ef4444;">${translations[lang]['rec-high-title']}</h4>
            <ul>
                <li>${translations[lang]['rec-high-1']}</li>
                <li>${translations[lang]['rec-high-2']}</li>
                <li>${translations[lang]['rec-high-3']}</li>
                <li>${translations[lang]['rec-high-4']}</li>
                <li>${translations[lang]['rec-high-5']}</li>
            </ul>
            <p><b style="color: #dc2626;">${translations[lang]['rec-high-note']}</b></p>
        `;
    }
}

// Save assessment
function saveAssessment() {
    if (!window.currentAssessment) {
        alert('No assessment to save. Please calculate risk first.');
        return;
    }

    const result = window.currentAssessment;

    // Get Patient ID from input field
    let patientIdInput = document.getElementById('patient-id').value.trim();

    // If Patient ID is empty, generate one automatically
    if (!patientIdInput || patientIdInput === '' || patientIdInput === 'N/A') {
        console.log('Patient ID is empty, generating auto ID...');

        // Call backend to generate Patient ID
        backend.generate_patient_id(function(response) {
            try {
                const idResult = JSON.parse(response);
                if (idResult.success && idResult.patient_id) {
                    // Update the input field with generated ID
                    document.getElementById('patient-id').value = idResult.patient_id;
                    console.log('✓ Generated Patient ID:', idResult.patient_id);

                    // Now proceed with saving using the generated ID
                    proceedWithSave(idResult.patient_id, result);
                } else {
                    // Fallback to default if generation fails
                    const fallbackId = idResult.patient_id || 'P-2025-0001';
                    document.getElementById('patient-id').value = fallbackId;
                    console.warn('⚠ Using fallback Patient ID:', fallbackId);
                    proceedWithSave(fallbackId, result);
                }
            } catch (e) {
                console.error('Error parsing generate_patient_id response:', e);
                alert('Error generating Patient ID. Please enter manually.');
            }
        });
    } else {
        // Patient ID provided, save directly
        proceedWithSave(patientIdInput, result);
    }
}

// Helper function to proceed with saving assessment
function proceedWithSave(patientId, result) {
    const healthWorker = document.getElementById('health-worker').value.trim() || 'N/A';
    const age = parseInt(document.getElementById('age').value) || 25;
    const bmi = parseFloat(result.bmi) || 0.0;
    const systolic = parseFloat(document.getElementById('systolic').value) || 120;
    const diastolic = parseFloat(document.getElementById('diastolic').value) || 80;
    const bloodSugar = parseFloat(document.getElementById('blood-sugar').value) || 0.0;
    const hemoglobin = parseFloat(document.getElementById('hemoglobin').value) || 0.0;
    const riskLevel = String(result.risk_level);
    const confidence = parseFloat(result.confidence) || 0.0;
    const modelUsed = String(result.model_used);
    const labAvailable = Boolean(result.lab_available);

    // Create data object with all assessment information
    const assessmentData = {
        patient_id: String(patientId),
        health_worker: String(healthWorker),
        age: parseInt(age),
        bmi: parseFloat(bmi),
        systolic: parseFloat(systolic),
        diastolic: parseFloat(diastolic),
        blood_sugar: parseFloat(bloodSugar),
        hemoglobin: parseFloat(hemoglobin),
        risk_level: String(riskLevel),
        confidence: parseFloat(confidence),
        model_used: String(modelUsed),
        lab_available: labAvailable
    };

    // Debug log
    console.log("Saving assessment with data:", assessmentData);

    // Convert to JSON string and send as single parameter
    const jsonData = JSON.stringify(assessmentData);
    console.log("JSON string to send:", jsonData);

    backend.save_assessment(jsonData, function(response) {
        console.log("=== Save Response Received ===");
        console.log("Raw response:", response);
        console.log("Response type:", typeof response);
        console.log("Response length:", response ? response.length : 0);

        try {
            // Check for empty response
            if (!response || (typeof response === 'string' && response.trim() === '')) {
                console.error('✗ Empty response from backend - slot may not have executed');
                throw new Error('Empty response from backend. The save_assessment method may not have been called. Check Python console for slot signature errors.');
            }

            // Try to parse JSON
            const res = JSON.parse(response);
            console.log("Parsed response:", res);

            if (res.success) {
                console.log('✓ Assessment saved successfully! Patient ID:', res.patient_id);
            } else {
                console.error('✗ Error saving assessment:', res.error || 'Unknown error');
                if (res.details) {
                    console.error('Error details:', res.details);
                }
            }
        } catch (e) {
            console.error('✗ CRITICAL ERROR: Failed to save assessment');
            console.error('✗ Parse error:', e.message);
            console.error('✗ This usually means the Python method signature does not match');
            console.error('✗ Check the Python console for "@pyqtSlot" errors');
            console.error('✗ Response was:', response || '(empty)');
        }
    });
}

// ============================================
// ⬇️ THIS IS THE ONLY CHANGE YOU NEED ⬇️
// ============================================

// Print report - Generate PDF
function printReport() {
    if (!window.currentAssessment) {
        alert('No assessment to print');
        return;
    }
    
    const btn = document.getElementById('print-btn');
    const originalText = btn.textContent;
    btn.textContent = '📄 Generating PDF...';
    btn.disabled = true;
    
    const patientId = document.getElementById('patient-id').value || 'N/A';
    const healthWorker = document.getElementById('health-worker').value || 'N/A';
    
    backend.generate_pdf_report(patientId, healthWorker, function(response) {
        const result = JSON.parse(response);
        
        if (result.success) {
            alert(`✓ PDF Report Generated!\n\nSaved to: ${result.filename}\n\nYou can find it in the 'reports' folder.`);
        } else {
            alert('Error generating PDF: ' + result.error);
        }
        
        btn.textContent = originalText;
        btn.disabled = false;
    });
}

// ============================================
// ⬆️ END OF CHANGE ⬆️
// ============================================

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

// Global variables for charts
let riskPieChart = null;
let weeklyLineChart = null;

// Load dashboard
function loadDashboard() {
    if (!backend) {
        console.error('Backend not initialized');
        return;
    }

    backend.get_dashboard_stats(function(statsJson) {
        try {
            const stats = JSON.parse(statsJson);

            if (stats.error) {
                console.error('Error loading dashboard stats:', stats.error);
                return;
            }

            // Update summary cards
            document.getElementById('total-assessments').textContent = stats.total_assessments;
            document.getElementById('high-risk-count').textContent =
                `${stats.high_risk_count} (${stats.high_risk_percentage}%)`;
            document.getElementById('avg-confidence').textContent = `${stats.avg_confidence}%`;
            document.getElementById('recent-activity').textContent = stats.recent_activity;

            // Update risk distribution pie chart
            updateRiskPieChart(stats.risk_distribution);

            // Update weekly assessments line chart
            updateWeeklyLineChart(stats.weekly_assessments);

            // Update risk factors table
            updateRiskFactorsTable(stats.risk_factors);

        } catch (e) {
            console.error('Error parsing dashboard stats:', e);
        }
    });
}

// Update risk distribution pie chart
function updateRiskPieChart(riskDist) {
    const ctx = document.getElementById('risk-pie-chart');
    if (!ctx) return;

    // Destroy previous chart if exists
    if (riskPieChart) {
        riskPieChart.destroy();
    }

    const dataValues = [
        riskDist.Low || 0,
        riskDist.Moderate || 0,
        riskDist.High || 0
    ];
    const total = dataValues.reduce((a, b) => a + b, 0);

    // Update center label
    document.getElementById('doughnut-total').textContent = total;

    const data = {
        labels: ['Low Risk', 'Moderate Risk', 'High Risk'],
        datasets: [{
            data: dataValues,
            backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
            borderWidth: 2,
            borderColor: '#fff'
        }]
    };

    riskPieChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        padding: 15,
                        font: {
                            size: 11,
                            family: "'Segoe UI', sans-serif"
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Update weekly assessments line chart
function updateWeeklyLineChart(weeklyData) {
    const ctx = document.getElementById('weekly-line-chart');
    if (!ctx) return;

    // Destroy previous chart if exists
    if (weeklyLineChart) {
        weeklyLineChart.destroy();
    }

    const labels = weeklyData.map(item => {
        // Format week label (e.g., "2025-W01" -> "Week 1")
        const weekStr = item.week.toString();
        const weekNum = weekStr.split('-W')[1] || weekStr.split('/')[1] || '?';
        return `Week ${weekNum}`;
    });

    const counts = weeklyData.map(item => item.count);

    // Create gradient
    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(54, 171, 163, 0.3)');
    gradient.addColorStop(1, 'rgba(54, 171, 163, 0.0)');

    const data = {
        labels: labels,
        datasets: [{
            label: 'Assessments',
            data: counts,
            borderColor: '#36ABA3',
            backgroundColor: gradient,
            borderWidth: 3,
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointBackgroundColor: '#36ABA3',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointHoverRadius: 6
        }]
    };

    weeklyLineChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 13,
                        family: "'Segoe UI', sans-serif"
                    },
                    bodyFont: {
                        size: 14,
                        family: "'Segoe UI', sans-serif"
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        color: '#f3f4f6',
                        drawBorder: false
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Update risk factors table
function updateRiskFactorsTable(riskFactors) {
    const tbody = document.getElementById('risk-factors-tbody');
    if (!tbody) return;

    if (!riskFactors || riskFactors.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="3" style="text-align: center; color: #9ca3af; padding: 24px;">
                    <span data-i18n="dashboard-no-data">${translations[currentLanguage]['dashboard-no-data']}</span>
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = riskFactors.map(factor => `
        <tr>
            <td>${factor.factor}</td>
            <td style="font-weight: 600; color: #36ABA3;">${factor.count}</td>
            <td class="percentage-cell">
                <div class="percentage-bar" style="width: ${factor.percentage}%;"></div>
                <span class="percentage-text">${factor.percentage}%</span>
            </td>
        </tr>
    `).join('');
}

// Export history
function exportHistory() {
    alert('Export feature: Use the Python application menu to export CSV files.');
}

// Feature Importance Chart
let featureImportanceChart = null;

function initFeatureImportanceChart() {
    const ctx = document.getElementById('feature-importance-chart');
    if (!ctx) return;

    // Destroy previous chart if exists
    if (featureImportanceChart) {
        featureImportanceChart.destroy();
    }

    const data = {
        labels: [
            'BMI (Body Mass Index)',
            'Systolic Blood Pressure',
            'Blood Sugar Level',
            'Hemoglobin Level',
            'Diastolic Blood Pressure'
        ],
        datasets: [{
            label: 'Relative Importance',
            data: [100, 85, 70, 60, 50],
            backgroundColor: [
                'rgba(54, 171, 163, 0.9)',
                'rgba(54, 171, 163, 0.75)',
                'rgba(54, 171, 163, 0.6)',
                'rgba(54, 171, 163, 0.45)',
                'rgba(54, 171, 163, 0.3)'
            ],
            borderColor: '#36ABA3',
            borderWidth: 1
        }]
    };

    featureImportanceChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 13,
                        family: "'Segoe UI', sans-serif"
                    },
                    bodyFont: {
                        size: 14,
                        family: "'Segoe UI', sans-serif"
                    },
                    callbacks: {
                        label: function(context) {
                            return 'Importance: ' + context.parsed.x + '%';
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        },
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        color: '#f3f4f6'
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: 12
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}