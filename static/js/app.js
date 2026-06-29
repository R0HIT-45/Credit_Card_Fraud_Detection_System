/**
 * FraudSense AI - Core Application Controller
 */

const vFeatures = [
  {id:"v1",label:"V1"}, {id:"v2",label:"V2"}, {id:"v3",label:"V3"}, {id:"v4",label:"V4"},
  {id:"v5",label:"V5"}, {id:"v6",label:"V6"}, {id:"v7",label:"V7"}, {id:"v8",label:"V8"},
  {id:"v9",label:"V9"}, {id:"v10",label:"V10"}, {id:"v11",label:"V11"}, {id:"v12",label:"V12"},
  {id:"v13",label:"V13"}, {id:"v14",label:"V14"}, {id:"v15",label:"V15"}, {id:"v16",label:"V16"},
  {id:"v17",label:"V17"}, {id:"v18",label:"V18"}, {id:"v19",label:"V19"}, {id:"v20",label:"V20"},
  {id:"v21",label:"V21"}, {id:"v22",label:"V22"}, {id:"v23",label:"V23"}, {id:"v24",label:"V24"},
  {id:"v25",label:"V25"}, {id:"v26",label:"V26"}, {id:"v27",label:"V27"}, {id:"v28",label:"V28"}
];

const presets = {
  upi: {
    amount: 250, time: 3600, duration: 15, payment: "UPI", merchant: "Grocery",
    device: "Mobile", country: "India", international: "No", otp: "Yes", pin: "Yes", vpn: "No", newDevice: "No",
    pca: {v1:0.5,v2:0.1,v3:0.8,v4:0.3,v5:0.2,v6:0.1,v7:0,v8:0.2,v9:0.1,v10:-0.1,v11:0.3,v12:0.5,v13:0,v14:0.1,v15:0,v16:0,v17:0.05,v18:0,v19:0,v20:0,v21:0,v22:0,v23:0,v24:0,v25:0,v26:0,v27:0,v28:0}
  },
  atm: {
    amount: 10000, time: 7200, duration: 45, payment: "ATM", merchant: "Fuel",
    device: "ATM", country: "India", international: "No", otp: "No", pin: "Yes", vpn: "No", newDevice: "No",
    pca: {v1:0.9,v2:0.2,v3:0.5,v4:0.4,v5:0.1,v6:0.2,v7:-0.1,v8:0.3,v9:0,v10:0.1,v11:0.4,v12:0.6,v13:0,v14:0.2,v15:0,v16:0,v17:0.1,v18:0,v19:0,v20:0,v21:0,v22:0,v23:0,v24:0,v25:0,v26:0,v27:0,v28:0}
  },
  shopping: {
    amount: 3500, time: 14400, duration: 120, payment: "Credit Card", merchant: "Electronics",
    device: "Desktop", country: "India", international: "No", otp: "Yes", pin: "Not Required", vpn: "No", newDevice: "No",
    pca: {v1:0.6,v2:0,v3:1,v4:0.5,v5:0.3,v6:0.2,v7:0.1,v8:0.2,v9:0.1,v10:-0.2,v11:0.2,v12:0.4,v13:0,v14:0.15,v15:0,v16:0,v17:0.05,v18:0,v19:0,v20:0,v21:0,v22:0,v23:0,v24:0,v25:0,v26:0,v27:0,v28:0}
  },
  international: {
    amount: 120000, time: 86400, duration: 300, payment: "Credit Card", merchant: "Travel",
    device: "Desktop", country: "Russia", international: "Yes", otp: "No", pin: "Not Required", vpn: "Yes", newDevice: "Yes",
    pca: {v1:-3,v2:2.5,v3:-4,v4:-1.5,v5:-1.8,v6:0.9,v7:-3,v8:1.1,v9:-4,v10:-0.2,v11:-2.5,v12:-3.5,v13:0,v14:-5,v15:0,v16:0,v17:-3,v18:0,v19:0,v20:0,v21:0,v22:0,v23:0,v24:0,v25:0,v26:0,v27:0,v28:0}
  }
};

document.addEventListener('DOMContentLoaded', () => {
  buildPcaSliders();
  setupFormEventListeners();
});

function buildPcaSliders() {
  const container = document.getElementById('pca-grid-container');
  if (!container) return;

  container.innerHTML = vFeatures.map(f => {
    return `
      <div class="pca-item">
        <div class="pca-label-row">
          <label for="${f.id}">${f.label}</label>
          <span id="${f.id}-val">0.0</span>
        </div>
        <input 
          type="range" 
          id="${f.id}" 
          class="pca-slider" 
          min="-10" 
          max="10" 
          step="0.1" 
          value="0" 
          oninput="document.getElementById('${f.id}-val').textContent = Number(this.value ?? 0).toFixed(1)"
        />
      </div>
    `;
  }).join('');
}

function setupFormEventListeners() {
  document.querySelectorAll('.preset-card[data-preset]').forEach(card => {
    card.addEventListener('click', () => {
      loadPreset(card.getAttribute('data-preset'));
    });
  });

  const analyzeBtn = document.getElementById('analyze-btn');
  if (analyzeBtn) analyzeBtn.addEventListener('click', analyzeTransaction);

  const retryBtn = document.getElementById('error-retry-btn');
  if (retryBtn) {
    retryBtn.addEventListener('click', () => {
      document.getElementById('error-alert-card').style.display = 'none';
      analyzeTransaction();
    });
  }
}

function loadPreset(key) {
  const p = presets[key];
  if (!p) return;

  setValue('amount', p.amount);
  setValue('time', p.time);
  setValue('duration', p.duration);
  setValue('payment-method', p.payment);
  setValue('merchant', p.merchant);
  setValue('device', p.device);
  setValue('country', p.country);
  setValue('international', p.international);
  setValue('otp', p.otp);
  setValue('pin', p.pin);
  setValue('vpn', p.vpn);
  setValue('new-device', p.newDevice);

  vFeatures.forEach(f => {
    const val = Number(p.pca[f.id] ?? 0);
    setValue(f.id, val);
    const label = document.getElementById(f.id + '-val');
    if (label) label.textContent = val.toFixed(1);
  });

  hideResults();
}

function setValue(id, val) {
  const el = document.getElementById(id);
  if (el) el.value = val;
}

function hideResults() {
  const results = document.getElementById('result-panel');
  if (results) results.style.display = 'none';
  const errorCard = document.getElementById('error-alert-card');
  if (errorCard) errorCard.style.display = 'none';
}

async function analyzeTransaction() {
  hideResults();
  
  const analyzeBtn = document.getElementById('analyze-btn');
  const amountVal = parseFloat(document.getElementById('amount')?.value);
  const timeVal = parseInt(document.getElementById('time')?.value) || 0;

  if (isNaN(amountVal) || amountVal < 0) {
    showErrorMessage('Please enter a valid, non-negative transaction amount.');
    return;
  }

  const payload = { amount: amountVal, time: timeVal };
  vFeatures.forEach(f => {
    payload[f.id] = parseFloat(document.getElementById(f.id)?.value) || 0;
  });

  if (analyzeBtn) analyzeBtn.disabled = true;

  const loader = document.getElementById('loading-overlay');
  if (loader) loader.style.display = 'block';

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) throw new Error(`HTTP Error Status: ${response.status}`);
    const data = await response.json();
    if (!data.success) throw new Error(data.error || 'Prediction calculation failed on server.');
    
    if (loader) loader.style.display = 'none';
    renderScoringOutcome(data);
  } catch (err) {
    if (loader) loader.style.display = 'none';
    showErrorMessage(err.message || 'Unable to connect to the scoring server.');
  } finally {
    if (analyzeBtn) analyzeBtn.disabled = false;
  }
}

function showErrorMessage(msg) {
  const errorCard = document.getElementById('error-alert-card');
  const errorText = document.getElementById('error-message-text');
  if (errorCard && errorText) {
    errorText.textContent = msg;
    errorCard.style.display = 'block';
  }
}

function renderScoringOutcome(data) {
  const resultsCard = document.getElementById('result-panel');
  if (!resultsCard) return;

  const isFraud = String(data.final_verdict || '').toUpperCase() === 'FRAUD';
  const confidence = Number(data.confidence ?? 0);
  const riskLevel = String(data.risk_level || 'LOW').toUpperCase();

  const verdictText = document.getElementById('verdict-text');
  if (verdictText) {
    verdictText.textContent = isFraud ? 'FRAUD' : 'LEGITIMATE';
    verdictText.className = 'verdict-text ' + (isFraud ? 'fraud' : 'legitimate');
  }

  const riskBadge = document.getElementById('risk-display');
  if (riskBadge) {
    riskBadge.textContent = riskLevel;
    riskBadge.className = 'kpi-val ' + riskLevel.toLowerCase();
  }

  const confPctText = document.getElementById('conf-pct');
  if (confPctText) confPctText.textContent = confidence.toFixed(1) + '%';
  
  const fraudProb = document.getElementById('fraud-prob');
  if (fraudProb) fraudProb.textContent = confidence.toFixed(1) + '%';
  if (fraudProb) fraudProb.className = 'kpi-val ' + (isFraud ? 'high' : 'low');

  renderModelCompCards(data.models);
  renderDecisionExplanation(isFraud, riskLevel);

  resultsCard.style.display = 'block';
  resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function renderModelCompCards(models) {
  const container = document.getElementById('models-grid');
  if (!container) return;

  const rf = models?.random_forest;
  const xgb = models?.xgboost;

  if (!rf && !xgb) {
    container.innerHTML = '<div>Model metrics unavailable.</div>';
    return;
  }

  container.innerHTML = `
    <div class="model-card">
      <div class="model-name">
        <span>Random Forest</span>
      </div>
      <div class="model-stat">
        <span>Probability</span>
        <span>${Number(rf?.fraud_probability ?? 0).toFixed(1)}%</span>
      </div>
      <div class="model-stat">
        <span>Prediction</span>
        <span>${rf?.prediction === 1 ? 'Fraud' : 'Legitimate'}</span>
      </div>
    </div>
    <div class="model-card">
      <div class="model-name">
        <span>XGBoost</span>
      </div>
      <div class="model-stat">
        <span>Probability</span>
        <span>${Number(xgb?.fraud_probability ?? 0).toFixed(1)}%</span>
      </div>
      <div class="model-stat">
        <span>Prediction</span>
        <span>${xgb?.prediction === 1 ? 'Fraud' : 'Legitimate'}</span>
      </div>
    </div>
  `;
}

function renderDecisionExplanation(isFraud, risk) {
  const container = document.getElementById('explain-list');
  if (!container) return;

  // Retrieve values from the UI context fields to explain the decision
  const amount = document.getElementById('amount')?.value || 0;
  const international = document.getElementById('international')?.value === 'Yes';
  const newDevice = document.getElementById('new-device')?.value === 'Yes';
  const otpFailed = document.getElementById('otp')?.value === 'No';
  const vpn = document.getElementById('vpn')?.value === 'Yes';
  const merchant = document.getElementById('merchant')?.value;
  const country = document.getElementById('country')?.value;

  let points = [];
  
  if (isFraud) {
    points.push({ text: `Transaction amount (₹${amount}) is unusually high for this profile.`, bad: true });
    
    if (international) {
      points.push({ text: `International transaction detected from ${country || 'unknown region'}.`, bad: true });
    }
    
    if (newDevice || vpn) {
      points.push({ text: `Suspicious network activity: ${vpn ? 'VPN/Proxy detected.' : ''} ${newDevice ? 'Unrecognized device signature.' : ''}`, bad: true });
    }
    
    if (otpFailed) {
      points.push({ text: 'Failed OTP or authentication verification.', bad: true });
    }
    
    points.push({ text: `PCA components indicate behavior deviates significantly from historical patterns.`, bad: true });
  } else {
    points.push({ text: `Transaction amount (₹${amount}) matches expected user patterns.`, bad: false });
    
    if (!international && country) {
      points.push({ text: `Domestic transaction originating from ${country}.`, bad: false });
    }
    
    if (!newDevice && !vpn) {
      points.push({ text: `Trusted device and network signature recognized.`, bad: false });
    }
    
    if (!otpFailed) {
      points.push({ text: `Strong authentication (OTP/PIN) successfully verified.`, bad: false });
    }
    
    points.push({ text: `PCA behavior metrics are within safe historical thresholds.`, bad: false });
  }

  container.innerHTML = points.map(pt => 
    `<li class="${pt.bad ? 'indicator-bad' : 'indicator-good'}">${pt.text}</li>`
  ).join('');
}
