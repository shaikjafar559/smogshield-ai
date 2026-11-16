/**
 * SmogShield AI - Frontend Application Controller
 * Handles real-time diurnal charts, dynamic routine generation,
 * IAQ hacks catalog, impact calculation, GenAI chat, and community pledges.
 */

// Application State
const state = {
  currentCity: "Delhi-NCR, India",
  currentAqi: 385,
  currentPm25: 285.0,
  cityData: null,
  diurnalChart: null,
  familyProfile: {
    family_name: "Our Family",
    household_size: 4,
    vulnerabilities: {
      infants_toddlers: 1,
      elderly: 1,
      respiratory_patients: 1,
      pregnant: 0,
      active_outdoor_athletes: 0,
      pets: 0
    },
    housing_type: "Apartment (mid-level)",
    window_sealing_quality: "Standard / Moderate Drafts",
    heating_source: "Electric / Heat Pump",
    cooking_style: "Standard with Range Hood",
    primary_commute: "Personal Car (ICE)",
    daily_commute_km: 20.0,
    has_air_purifier: false,
    purifier_count: 0
  },
  iaqHacks: [],
  communityPledges: [],
  geminiApiKey: localStorage.getItem("smogshield_gemini_key") || ""
};

// Initialize Application on DOM Ready
document.addEventListener("DOMContentLoaded", async () => {
  if (window.lucide) {
    lucide.createIcons();
  }

  setupNavigationTabs();
  setupEventListeners();
  await loadLocations();
  await refreshCityData(state.currentCity);
  await generateRoutine();
  await loadIAQHacks();
  await updateImpactCalculation();
  await loadCommunityData();
});

// Setup Navigation Tabs
function setupNavigationTabs() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => {
        t.classList.remove("active", "bg-sky-500/20", "text-sky-300", "border", "border-sky-500/30");
        t.classList.add("text-slate-400", "hover:text-slate-200", "hover:bg-slate-800");
      });
      tab.classList.add("active", "bg-sky-500/20", "text-sky-300", "border", "border-sky-500/30");
      tab.classList.remove("text-slate-400", "hover:text-slate-200", "hover:bg-slate-800");

      const targetId = tab.getAttribute("data-target");
      document.querySelectorAll(".tab-content").forEach(c => c.classList.add("hidden"));
      const targetContent = document.getElementById(targetId);
      if (targetContent) {
        targetContent.classList.remove("hidden");
      }
      if (window.lucide) lucide.createIcons();
    });
  });
}

// Setup Event Listeners
function setupEventListeners() {
  // City Selector
  const citySelect = document.getElementById("city-selector");
  citySelect.addEventListener("change", async (e) => {
    state.currentCity = e.target.value;
    await refreshCityData(state.currentCity);
    await generateRoutine();
  });

  // Custom AQI Slider Toggle
  const toggleCustomBtn = document.getElementById("toggle-custom-aqi-btn");
  const customPanel = document.getElementById("custom-aqi-panel");
  toggleCustomBtn.addEventListener("click", () => {
    customPanel.classList.toggle("hidden");
  });

  const aqiSlider = document.getElementById("custom-aqi-slider");
  const aqiLabel = document.getElementById("custom-aqi-val-label");
  aqiSlider.addEventListener("input", (e) => {
    aqiLabel.textContent = `${e.target.value} AQI`;
  });

  document.getElementById("apply-custom-aqi").addEventListener("click", async () => {
    const val = parseInt(aqiSlider.value);
    state.currentAqi = val;
    state.currentPm25 = val * 0.74;
    await refreshCityData(state.currentCity, val);
    await generateRoutine();
    await updateImpactCalculation();
    customPanel.classList.add("hidden");
  });

  // Generate Routine Button
  document.getElementById("btn-generate-routine").addEventListener("click", async () => {
    readProfileFromForm();
    await generateRoutine();
  });

  // IAQ Category Filters
  const catBtns = document.querySelectorAll(".iaq-filter-btn");
  catBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      catBtns.forEach(b => {
        b.classList.remove("active", "bg-sky-600", "text-white");
        b.classList.add("bg-slate-800", "text-slate-300");
      });
      btn.classList.add("active", "bg-sky-600", "text-white");
      btn.classList.remove("bg-slate-800", "text-slate-300");
      renderIAQHacks(btn.getAttribute("data-cat"));
    });
  });

  // Impact Calculator Sliders
  const sizeSlider = document.getElementById("calc-size");
  const kmSlider = document.getElementById("calc-km");
  const pmSlider = document.getElementById("calc-pm");
  const commuteSelect = document.getElementById("calc-commute-mode");

  const syncCalc = async () => {
    document.getElementById("calc-size-val").textContent = `${sizeSlider.value} people`;
    document.getElementById("calc-km-val").textContent = `${kmSlider.value} km`;
    document.getElementById("calc-pm-val").textContent = `${pmSlider.value} µg/m³`;
    await updateImpactCalculation();
  };

  sizeSlider.addEventListener("input", syncCalc);
  kmSlider.addEventListener("input", syncCalc);
  pmSlider.addEventListener("input", syncCalc);
  commuteSelect.addEventListener("change", syncCalc);

  // Chat Form Submission
  const chatForm = document.getElementById("chat-form");
  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = document.getElementById("chat-input");
    const msg = input.value.trim();
    if (!msg) return;
    input.value = "";
    await sendChatMessage(msg);
  });

  // Community Pledge Form Submission
  const pledgeForm = document.getElementById("pledge-form");
  pledgeForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    await submitPledge();
  });
}

// Load Locations Dropdown
async function loadLocations() {
  try {
    const res = await fetch("/api/locations");
    const locations = await res.json();
    const selector = document.getElementById("city-selector");
    selector.innerHTML = "";
    locations.forEach(loc => {
      const opt = document.createElement("option");
      opt.value = loc.name;
      opt.textContent = `${loc.name} (AQI ${loc.base_aqi})`;
      if (loc.name === state.currentCity) opt.selected = true;
      selector.appendChild(opt);
    });
  } catch (err) {
    console.error("Failed to load locations:", err);
  }
}

// Refresh City Data & Update Atmospheric Inversion Banner + Diurnal Chart
async function refreshCityData(cityName, customAqi = null) {
  try {
    const url = `/api/location/${encodeURIComponent(cityName)}${customAqi ? `?custom_aqi=${customAqi}` : ""}`;
    const res = await fetch(url);
    const data = await res.json();
    state.cityData = data;
    state.currentAqi = data.base_aqi;
    state.currentPm25 = data.base_pm25;

    // Update Top Status Display
    const aqiDisplay = document.getElementById("aqi-display");
    aqiDisplay.textContent = `AQI ${data.base_aqi} • ${data.smog_alert_level.split(" ")[0]}`;

    const aqiBadge = document.getElementById("aqi-badge-container");
    if (data.base_aqi >= 300) {
      aqiBadge.className = "flex items-center gap-2 px-3 py-1.5 rounded-lg bg-rose-500/20 border border-rose-500/40 text-rose-300 font-bold text-sm animate-pulse";
    } else if (data.base_aqi >= 200) {
      aqiBadge.className = "flex items-center gap-2 px-3 py-1.5 rounded-lg bg-orange-500/20 border border-orange-500/40 text-orange-300 font-bold text-sm";
    } else {
      aqiBadge.className = "flex items-center gap-2 px-3 py-1.5 rounded-lg bg-amber-500/20 border border-amber-500/40 text-amber-300 font-bold text-sm";
    }

    document.getElementById("inversion-desc").textContent = `Thermal Inversion Alert: ${data.inversion_level}`;
    document.getElementById("best-vent-window").textContent = data.best_ventilation_window;
    document.getElementById("wind-speed-val").textContent = `${data.wind_speed_kmh} km/h (${data.wind_speed_kmh < 5 ? "Calm / Stagnant" : "Breeze"})`;

    // Sync sliders
    document.getElementById("calc-pm").value = Math.round(data.base_pm25);
    document.getElementById("calc-pm-val").textContent = `${Math.round(data.base_pm25)} µg/m³`;

    renderDiurnalChart(data);
  } catch (err) {
    console.error("Failed to refresh city data:", err);
  }
}

// Render Diurnal Chart using Chart.js
function renderDiurnalChart(data) {
  const ctx = document.getElementById("diurnalChart").getContext("2d");
  const points = data.diurnal_multipliers || [
    { hour: "00:00", factor: 1.2 },
    { hour: "06:00", factor: 1.4 },
    { hour: "12:00", factor: 0.8 },
    { hour: "14:00", factor: 0.65 },
    { hour: "18:00", factor: 1.25 },
    { hour: "22:00", factor: 1.3 }
  ];

  const labels = points.map(p => p.hour);
  const pmValues = points.map(p => Math.round(data.base_pm25 * p.factor));

  if (state.diurnalChart) {
    state.diurnalChart.destroy();
  }

  state.diurnalChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Surface PM2.5 (µg/m³)",
          data: pmValues,
          borderColor: "#38bdf8",
          backgroundColor: "rgba(56, 189, 248, 0.15)",
          fill: true,
          tension: 0.4,
          pointBackgroundColor: points.map(p => {
            if (p.hour === "14:00" || p.hour === "13:00") return "#10b981"; // Safe vent window
            if (p.hour === "06:00" || p.hour === "08:00" || p.hour === "20:00") return "#f43f5e"; // Hazard peak
            return "#38bdf8";
          }),
          pointRadius: 5,
          pointHoverRadius: 7
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: "#0f172a",
          borderColor: "#334155",
          borderWidth: 1,
          titleFont: { size: 12 },
          bodyFont: { size: 12 },
          callbacks: {
            label: function(context) {
              const pt = points[context.dataIndex];
              return ` PM2.5: ${context.parsed.y} µg/m³ (${pt.inversion || "Trapping Phase"})`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: { color: "#94a3b8", font: { size: 10 } }
        },
        y: {
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: { color: "#94a3b8", font: { size: 10 } }
        }
      }
    }
  });
}

// Read Profile from Form
function readProfileFromForm() {
  state.familyProfile = {
    family_name: document.getElementById("prof-name").value || "Our Family",
    household_size: parseInt(document.getElementById("prof-size").value) || 4,
    vulnerabilities: {
      infants_toddlers: document.getElementById("vuln-infant").checked ? 1 : 0,
      elderly: document.getElementById("vuln-elderly").checked ? 1 : 0,
      respiratory_patients: document.getElementById("vuln-asthma").checked ? 1 : 0,
      pregnant: document.getElementById("vuln-pregnant").checked ? 1 : 0,
      active_outdoor_athletes: 0,
      pets: 0
    },
    housing_type: document.getElementById("prof-housing").value,
    window_sealing_quality: document.getElementById("prof-window").value,
    heating_source: document.getElementById("prof-heating").value,
    cooking_style: "Standard with Range Hood",
    primary_commute: document.getElementById("prof-commute").value,
    daily_commute_km: parseFloat(document.getElementById("prof-km").value) || 20.0,
    has_air_purifier: false,
    purifier_count: 0
  };
}

// Generate Routine via API
async function generateRoutine() {
  const headlineEl = document.getElementById("routine-headline");
  headlineEl.textContent = "Synthesizing atmospheric boundary layer & lifestyle data...";

  try {
    const res = await fetch(`/api/routine/generate?city=${encodeURIComponent(state.currentCity)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(state.familyProfile)
    });
    const plan = await res.json();
    renderRoutinePlan(plan);
  } catch (err) {
    console.error("Error generating routine:", err);
    headlineEl.textContent = "Unable to load routine. Please check connection.";
  }
}

// Render Routine Plan to DOM
function renderRoutinePlan(plan) {
  document.getElementById("routine-headline").textContent = plan.summary_headline;
  document.getElementById("stat-routine-pm-prevented").textContent = `${plan.total_estimated_intake_prevented_ug.toLocaleString()} µg`;
  document.getElementById("stat-routine-co2-prevented").textContent = `${plan.total_co2_prevented_kg} kg`;

  // Render Critical Warnings
  const warnBox = document.getElementById("critical-warnings-box");
  const warnList = document.getElementById("critical-warnings-list");
  if (plan.critical_family_warnings && plan.critical_family_warnings.length > 0) {
    warnBox.classList.remove("hidden");
    warnList.innerHTML = plan.critical_family_warnings.map(w => `<li>${w}</li>`).join("");
  } else {
    warnBox.classList.add("hidden");
  }

  // Render Phased Steps
  const stepsContainer = document.getElementById("routine-steps-list");
  stepsContainer.innerHTML = "";

  plan.routine_steps.forEach((step, idx) => {
    let riskBadge = `<span class="px-2 py-0.5 rounded text-[11px] font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/30">Extreme Risk</span>`;
    if (step.outdoor_smog_risk.toLowerCase().includes("moderate")) {
      riskBadge = `<span class="px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Ventilation Window</span>`;
    } else if (step.outdoor_smog_risk.toLowerCase().includes("high")) {
      riskBadge = `<span class="px-2 py-0.5 rounded text-[11px] font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30">High Risk</span>`;
    }

    const card = document.createElement("div");
    card.className = "glass-panel p-5 rounded-xl border border-slate-800 space-y-4 hover:border-sky-500/30 transition";
    card.innerHTML = `
      <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
        <div class="flex items-center gap-3">
          <span class="px-2.5 py-1 rounded-lg bg-sky-950 text-sky-400 font-mono text-xs font-bold border border-sky-800">${step.time_window}</span>
          <span class="text-xs font-semibold text-slate-300">${step.phase}</span>
        </div>
        ${riskBadge}
      </div>

      <div>
        <h4 class="text-base font-bold text-white flex items-center gap-2">
          <i data-lucide="check-circle-2" class="w-4 h-4 text-sky-400 shrink-0"></i>
          ${step.action_title}
        </h4>
        <p class="text-xs text-slate-300 mt-1.5 leading-relaxed">${step.recommended_action}</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
        <div class="bg-slate-900/80 p-3 rounded-lg border border-teal-500/20 text-xs">
          <span class="font-bold text-teal-400 block mb-1 flex items-center gap-1.5">
            <i data-lucide="leaf" class="w-3.5 h-3.5"></i> Sustainable Alternative
          </span>
          <p class="text-slate-300">${step.sustainable_alternative}</p>
        </div>

        <div class="bg-slate-900/80 p-3 rounded-lg border border-sky-500/20 text-xs">
          <span class="font-bold text-sky-400 block mb-1 flex items-center gap-1.5">
            <i data-lucide="shield" class="w-3.5 h-3.5"></i> Indoor IAQ Protocol
          </span>
          <p class="text-slate-300">${step.iaq_protocol}</p>
        </div>
      </div>

      <!-- Impact & Science Explanation Bar -->
      <div class="p-3 rounded-lg bg-slate-950/70 border border-slate-800 text-xs text-slate-400 space-y-1">
        <div class="text-slate-200">
          <strong class="text-amber-300">Why this matters:</strong> ${step.direct_impact_explanation}
        </div>
        <div class="flex flex-wrap gap-4 pt-1 text-[11px]">
          <span class="text-teal-300"><strong>Emission Saved:</strong> ${step.emission_savings}</span>
          <span class="text-sky-300"><strong>Health Benefit:</strong> ${step.health_benefit}</span>
        </div>
      </div>
    `;
    stepsContainer.appendChild(card);
  });

  // Render Sustainable Swaps Grid
  const swapsGrid = document.getElementById("sustainable-swaps-grid");
  swapsGrid.innerHTML = plan.key_sustainable_swaps.map(swap => `
    <div class="bg-slate-900/80 p-3.5 rounded-xl border border-slate-800 space-y-2">
      <span class="text-[10px] font-bold uppercase tracking-wider text-rose-400">Smog Habit</span>
      <h5 class="text-xs font-semibold text-slate-200">${swap.habit}</h5>
      <div class="pt-1 border-t border-slate-800">
        <span class="text-[10px] font-bold uppercase tracking-wider text-teal-400">Sustainable Swap</span>
        <p class="text-xs text-teal-200 font-medium">${swap.sustainable_swap}</p>
      </div>
      <p class="text-[10px] text-slate-400 italic">${swap.impact}</p>
    </div>
  `).join("");

  if (window.lucide) lucide.createIcons();
}

// Load IAQ Hacks Catalog
async function loadIAQHacks() {
  try {
    const res = await fetch("/api/iaq-hacks");
    state.iaqHacks = await res.json();
    renderIAQHacks("All");
  } catch (err) {
    console.error("Error loading IAQ hacks:", err);
  }
}

// Render IAQ Hacks
function renderIAQHacks(category = "All") {
  const container = document.getElementById("iaq-cards-grid");
  container.innerHTML = "";

  const filtered = category === "All" 
    ? state.iaqHacks 
    : state.iaqHacks.filter(h => h.category.toLowerCase() === category.toLowerCase());

  filtered.forEach(hack => {
    const card = document.createElement("div");
    card.className = "glass-card p-5 rounded-xl border border-slate-800 flex flex-col justify-between space-y-4";
    card.innerHTML = `
      <div class="space-y-2">
        <div class="flex items-center justify-between text-xs">
          <span class="px-2 py-0.5 rounded-full bg-sky-950 text-sky-400 border border-sky-800 font-medium">${hack.category}</span>
          <span class="text-slate-400 font-mono">${hack.difficulty}</span>
        </div>
        <h4 class="text-base font-bold text-white">${hack.title}</h4>
        <p class="text-xs text-slate-300 leading-relaxed">${hack.scientific_rationale}</p>
      </div>

      <div class="space-y-3 pt-2 border-t border-slate-800">
        <div class="flex items-center justify-between text-xs">
          <span class="text-slate-400">Est. Cost: <strong class="text-emerald-400">$${hack.est_cost_usd}</strong></span>
          <span class="text-slate-400">CADR: <strong class="text-sky-300">${hack.cadr_rating ? hack.cadr_rating.split(" ")[0] : "Passive"}</strong></span>
        </div>

        <div class="p-2.5 rounded-lg bg-slate-900/90 text-xs text-slate-300 space-y-1">
          <span class="font-bold text-teal-400 block text-[11px]">Key Instruction:</span>
          <p class="text-slate-300 text-[11px] line-clamp-2">${hack.instructions[0]}</p>
        </div>

        <button onclick="viewHackDetail('${hack.id}')" class="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold transition flex items-center justify-center gap-1.5">
          <i data-lucide="info" class="w-3.5 h-3.5"></i>
          <span>View Materials & Steps</span>
        </button>
      </div>
    `;
    container.appendChild(card);
  });

  if (window.lucide) lucide.createIcons();
}

// View Specific Hack Detail Modal or Alert
function viewHackDetail(hackId) {
  if (hackId === "corsi-rosenthal-box") {
    openCRBoxModal();
    return;
  }
  const hack = state.iaqHacks.find(h => h.id === hackId);
  if (!hack) return;

  const content = `
    ${hack.title}\n\n
    Estimated Cost: $${hack.est_cost_usd}\n
    CADR / Clearance: ${hack.cadr_rating || "Passive"}\n\n
    MATERIALS NEEDED:\n${hack.materials_needed.map(m => `• ${m}`).join("\n")}\n\n
    INSTRUCTIONS:\n${hack.instructions.join("\n\n")}\n\n
    SCIENCE:\n${hack.scientific_rationale}
  `;
  alert(content);
}

// Update Direct Impact Calculator
async function updateImpactCalculation() {
  const householdSize = parseInt(document.getElementById("calc-size").value) || 4;
  const km = parseFloat(document.getElementById("calc-km").value) || 25.0;
  const pm = parseFloat(document.getElementById("calc-pm").value) || 285.0;
  const commute = document.getElementById("calc-commute-mode").value;

  try {
    const res = await fetch("/api/impact/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        household_size: householdSize,
        has_vulnerable_members: true,
        current_outdoor_pm25: pm,
        commute_mode: commute,
        daily_commute_km: km,
        implemented_actions: ["C-R Box", "Sealing", "Anti-Idling"]
      })
    });
    const impact = await res.json();

    document.getElementById("metric-pm-prevented").textContent = `${impact.pm25_prevented_ug.toLocaleString()} µg`;
    document.getElementById("metric-cigs-prevented").textContent = `${impact.cigarette_equivalent_prevented} cigs / day`;
    document.getElementById("metric-risk-drop").textContent = `${impact.acute_respiratory_risk_drop_pct}%`;
    document.getElementById("metric-risk-bar").style.width = `${impact.acute_respiratory_risk_drop_pct}%`;

    document.getElementById("metric-co2-saved").textContent = `${impact.daily_co2_saved_kg} kg`;
    document.getElementById("metric-tailpipe-saved").textContent = `${impact.daily_pm_tailpipe_saved_grams} g / day`;
    document.getElementById("metric-neighborhood-multiplier").textContent = `${impact.neighborhood_scale_pm25_kg_year} kg`;
    document.getElementById("calc-narrative").textContent = impact.explanation_narrative;
  } catch (err) {
    console.error("Error updating impact:", err);
  }
}

// Chat Assistant Handler
async function sendChatMessage(userText) {
  const chatMessages = document.getElementById("chat-messages");

  // Append User Bubble
  const userDiv = document.createElement("div");
  userDiv.className = "flex items-start justify-end gap-3";
  userDiv.innerHTML = `
    <div class="chat-msg-user p-3.5 rounded-xl text-xs sm:text-sm max-w-lg leading-relaxed">
      ${escapeHtml(userText)}
    </div>
    <div class="w-8 h-8 rounded-lg bg-sky-700 flex items-center justify-center shrink-0 text-white font-bold text-xs">
      You
    </div>
  `;
  chatMessages.appendChild(userDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  // Append Loading Bubble
  const loadingDiv = document.createElement("div");
  loadingDiv.id = "chat-loading-indicator";
  loadingDiv.className = "flex items-start gap-3";
  loadingDiv.innerHTML = `
    <div class="w-8 h-8 rounded-lg bg-sky-600 flex items-center justify-center shrink-0">
      <i data-lucide="shield" class="w-4 h-4 text-white"></i>
    </div>
    <div class="chat-msg-ai p-3.5 rounded-xl text-xs sm:text-sm text-slate-400">
      <span class="inline-flex items-center gap-1">
        Analyzing atmospheric physics and indoor dynamics
        <span class="animate-bounce">.</span><span class="animate-bounce delay-100">.</span><span class="animate-bounce delay-200">.</span>
      </span>
    </div>
  `;
  chatMessages.appendChild(loadingDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  if (window.lucide) lucide.createIcons();

  try {
    const persona = document.getElementById("chat-persona-select").value;
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: userText,
        location: state.currentCity,
        current_aqi: state.currentAqi,
        persona: persona,
        api_key: state.geminiApiKey || null
      })
    });
    const chatResp = await res.json();

    loadingDiv.remove();

    // Render Assistant Bubble
    const aiDiv = document.createElement("div");
    aiDiv.className = "flex items-start gap-3";
    const renderedMarkdown = window.marked ? marked.parse(chatResp.reply) : `<p>${chatResp.reply}</p>`;

    let citationsHtml = "";
    if (chatResp.citations && chatResp.citations.length > 0) {
      citationsHtml = `
        <div class="pt-2 mt-2 border-t border-slate-800 text-[11px] text-slate-400 space-y-0.5">
          <strong class="text-sky-400">Citations & Models:</strong>
          <ul class="list-disc list-inside">
            ${chatResp.citations.map(c => `<li>${c}</li>`).join("")}
          </ul>
        </div>
      `;
    }

    aiDiv.innerHTML = `
      <div class="w-8 h-8 rounded-lg bg-sky-600 flex items-center justify-center shrink-0">
        <i data-lucide="shield-check" class="w-4 h-4 text-white"></i>
      </div>
      <div class="chat-msg-ai p-4 rounded-xl text-xs sm:text-sm text-slate-200 max-w-2xl leading-relaxed space-y-2">
        <div class="prose prose-invert prose-sm max-w-none">
          ${renderedMarkdown}
        </div>
        ${citationsHtml}
      </div>
    `;
    chatMessages.appendChild(aiDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    if (window.lucide) lucide.createIcons();
  } catch (err) {
    console.error("Chat error:", err);
    loadingDiv.remove();
    const errorDiv = document.createElement("div");
    errorDiv.className = "p-3 bg-rose-950/40 border border-rose-500/30 rounded-lg text-rose-300 text-xs";
    errorDiv.textContent = "Error communicating with AI engine. Please retry.";
    chatMessages.appendChild(errorDiv);
  }
}

function sendQuickPrompt(text) {
  document.getElementById("chat-input").value = text;
  sendChatMessage(text);
}

// Community Data & Pledges
async function loadCommunityData() {
  try {
    // Load Campaigns
    const campRes = await fetch("/api/community/initiatives");
    const campaigns = await campRes.json();
    const campGrid = document.getElementById("community-campaigns-grid");
    campGrid.innerHTML = campaigns.map(c => `
      <div class="glass-card p-5 rounded-xl border border-slate-800 space-y-3">
        <div class="flex items-center justify-between text-xs">
          <span class="px-2 py-0.5 rounded-full bg-teal-950 text-teal-400 border border-teal-800 font-medium">${c.category}</span>
          <span class="text-teal-300 font-bold flex items-center gap-1">
            <i data-lucide="check" class="w-3.5 h-3.5"></i> ${c.pledges_count} Pledged
          </span>
        </div>
        <h4 class="text-base font-bold text-white">${c.title}</h4>
        <p class="text-xs text-slate-300 leading-relaxed">${c.description}</p>
        <div class="p-2.5 rounded-lg bg-slate-900/90 text-xs text-teal-300 border border-teal-500/20">
          <strong>Community Impact:</strong> ${c.impact_metric}
        </div>
      </div>
    `).join("");

    // Load Pledges Feed
    const pledRes = await fetch("/api/community/pledges");
    const pledges = await pledRes.json();
    state.communityPledges = pledges;
    renderPledgesList();
  } catch (err) {
    console.error("Error loading community data:", err);
  }
}

function renderPledgesList() {
  const container = document.getElementById("pledges-stream-list");
  container.innerHTML = state.communityPledges.map(p => `
    <div class="p-3.5 bg-slate-900/80 rounded-xl border border-slate-800 space-y-1.5 text-xs">
      <div class="flex items-center justify-between">
        <span class="font-bold text-white flex items-center gap-1.5">
          <i data-lucide="user-check" class="w-4 h-4 text-teal-400"></i>
          ${p.family_name} • <span class="text-slate-400 font-normal">${p.neighborhood}</span>
        </span>
        <span class="text-[10px] text-slate-500 font-mono">${p.timestamp || "Recently"}</span>
      </div>
      <p class="text-slate-300 italic">"${p.community_message}"</p>
      <div class="flex flex-wrap gap-1.5 pt-1">
        ${p.actions_pledged.map(a => `<span class="px-2 py-0.5 rounded bg-teal-950/80 text-teal-300 text-[10px] border border-teal-800">${a}</span>`).join("")}
      </div>
    </div>
  `).join("");
  if (window.lucide) lucide.createIcons();
}

async function submitPledge() {
  const family = document.getElementById("pledge-family").value.trim();
  const colony = document.getElementById("pledge-colony").value.trim();
  const msg = document.getElementById("pledge-msg").value.trim() || "Pledged to protect our community's clean air!";

  const acts = [];
  if (document.getElementById("pledge-act-1").checked) acts.push("Zero-Idling at School Gates");
  if (document.getElementById("pledge-act-2").checked) acts.push("Trip-Chaining Errands");
  if (document.getElementById("pledge-act-3").checked) acts.push("C-R Box DIY Air Cleaner");
  if (document.getElementById("pledge-act-4").checked) acts.push("Zero Wood/Waste Burning");

  if (!acts.length) acts.push("Low-Emission Winter Routine");

  try {
    const res = await fetch("/api/community/pledge", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        neighborhood: colony,
        family_name: family,
        actions_pledged: acts,
        community_message: msg
      })
    });
    const newPledge = await res.json();
    state.communityPledges.unshift(newPledge);
    renderPledgesList();
    closePledgeModal();
    alert("Thank you! Your family's pledge has been added to the neighborhood action board.");
  } catch (err) {
    console.error("Error submitting pledge:", err);
  }
}

// Modal Helpers
function openCRBoxModal() {
  document.getElementById("cr-modal").classList.remove("hidden");
  if (window.lucide) lucide.createIcons();
}

function closeCRBoxModal() {
  document.getElementById("cr-modal").classList.add("hidden");
}

function openPledgeModal() {
  document.getElementById("pledge-modal").classList.remove("hidden");
  if (window.lucide) lucide.createIcons();
}

function closePledgeModal() {
  document.getElementById("pledge-modal").classList.add("hidden");
}

function toggleApiKeyInput() {
  const panel = document.getElementById("gemini-key-panel");
  panel.classList.toggle("hidden");
  const input = document.getElementById("gemini-api-key");
  if (state.geminiApiKey) input.value = state.geminiApiKey;
}

function saveApiKey() {
  const key = document.getElementById("gemini-api-key").value.trim();
  state.geminiApiKey = key;
  localStorage.setItem("smogshield_gemini_key", key);
  document.getElementById("gemini-key-panel").classList.add("hidden");
  alert(key ? "Gemini API Key saved for live inference." : "Using built-in atmospheric reasoning engine.");
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
