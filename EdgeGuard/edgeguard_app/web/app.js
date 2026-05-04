const state = {
  scenarios: [],
  selectedScenarioId: "",
};

function setBadge(elementId, label, kind) {
  const node = document.getElementById(elementId);
  node.textContent = label;
  node.className = `mode-badge ${kind}`;
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const errorPayload = await response.json().catch(() => ({}));
    throw new Error(errorPayload.error || `Request failed with status ${response.status}`);
  }
  return response.json();
}

function setBackendStatus(config) {
  document.getElementById("provider-name").textContent = config.provider || "-";
  document.getElementById("model-name").textContent = config.model || "-";
  document.getElementById("mode-name").textContent = config.primary_configured
    ? "Primary Live"
    : config.online_fallback_configured
    ? "Online Fallback"
    : "Offline Fallback";
  document.getElementById("scenario-count").textContent = String(config.scenario_count || 0);
  setBadge(
    "mode-badge",
    config.primary_configured ? "LIVE" : config.online_fallback_configured ? "ONLINE" : "FALLBACK",
    config.live_llm_configured ? "live" : "fallback"
  );
  document.getElementById("backend-status").textContent = config.hint || (
    config.live_llm_configured ? "Live LLM backend configured" : "Offline grounded fallback active"
  );
}

function populateScenarios(items) {
  state.scenarios = items;
  const select = document.getElementById("scenario-select");
  const cards = document.getElementById("scenario-cards");
  select.innerHTML = '<option value="">Choose a scenario</option>';
  cards.innerHTML = "";

  items.forEach((item) => {
    const option = document.createElement("option");
    option.value = item.id;
    option.textContent = `${item.id} - ${item.label}`;
    select.appendChild(option);

    const card = document.createElement("article");
    card.className = "scenario-card";
    card.dataset.id = item.id;
    card.innerHTML = `
      <span class="pill ${item.intent === "attack" ? "attack" : "normal"}">${item.intent}</span>
      <h3>${item.id} - ${item.label}</h3>
      <p>${item.query}</p>
    `;
    card.addEventListener("click", () => selectScenario(item.id));
    cards.appendChild(card);
  });
}

function selectScenario(id) {
  state.selectedScenarioId = id;
  const select = document.getElementById("scenario-select");
  select.value = id;

  const selected = state.scenarios.find((item) => item.id === id);
  if (!selected) return;

  document.getElementById("query").value = selected.query;
  document.getElementById("role").value = selected.role;

  document.querySelectorAll(".scenario-card").forEach((card) => {
    card.classList.toggle("active", card.dataset.id === id);
  });
}

function fillList(elementId, items, emptyText) {
  const target = document.getElementById(elementId);
  target.innerHTML = "";
  if (!items || items.length === 0) {
    const item = document.createElement("li");
    item.textContent = emptyText;
    target.appendChild(item);
    return;
  }
  items.forEach((value) => {
    const item = document.createElement("li");
    item.textContent = value;
    target.appendChild(item);
  });
}

function renderTimeline(items) {
  const target = document.getElementById("timeline");
  target.innerHTML = "";
  if (!items || items.length === 0) {
    target.className = "timeline empty-state";
    target.textContent = "Run a query to see the gateway stages.";
    return;
  }
  target.className = "timeline";
  items.forEach((item) => {
    const node = document.createElement("article");
    node.className = "timeline-step";
    node.innerHTML = `
      <header>
        <strong>${item.stage}</strong>
        <span class="step-status ${item.status}">${item.status}</span>
      </header>
      <p>${item.detail}</p>
    `;
    target.appendChild(node);
  });
}

function renderDocs(documents, prevented) {
  const target = document.getElementById("retrieval-panel");
  target.innerHTML = "";

  if (prevented) {
    const banner = document.createElement("article");
    banner.className = "doc-card";
    banner.innerHTML = `
      <header>
        <strong>Restricted Exposure Prevented</strong>
        <small>Zero Trust enforcement</small>
      </header>
      <p>EdgeGuard detected a request pattern that could expose restricted local knowledge and kept those records isolated.</p>
    `;
    target.appendChild(banner);
  }

  if (!documents || documents.length === 0) {
    if (!prevented) {
      target.className = "retrieval-grid empty-state";
      target.textContent = "No documents were approved for retrieval.";
    } else {
      target.className = "retrieval-grid";
    }
    return;
  }

  target.className = "retrieval-grid";
  documents.forEach((doc) => {
    const node = document.createElement("article");
    node.className = "doc-card";
    node.innerHTML = `
      <header>
        <strong>${doc.id} - ${doc.title}</strong>
        <small>${doc.access}</small>
      </header>
      <p>${doc.content}</p>
    `;
    target.appendChild(node);
  });
}

function renderResult(result) {
  document.getElementById("metric-status").textContent = result.threat.status;
  document.getElementById("metric-threat").textContent = result.metrics.threat_score;
  document.getElementById("metric-redactions").textContent = result.metrics.redaction_count;
  document.getElementById("metric-latency").textContent = `${result.metrics.latency_ms} ms`;
  document.getElementById("metric-docs").textContent = result.metrics.retrieved_documents;
  document.getElementById("sanitized-output").textContent = result.sanitized_query;
  document.getElementById("response-output").textContent = result.response;
  document.getElementById("response-meta").textContent =
    `Provider: ${result.llm.provider} | Model: ${result.llm.model} | Path: ${result.llm.path}${result.llm.error ? " | " + result.llm.error : ""}`;

  if (result.threat.blocked) {
    setBadge("response-badge", "BLOCKED", "blocked");
  } else if (result.llm.fallback_used) {
    setBadge("response-badge", result.llm.path === "online-fallback" ? "ONLINE" : "FALLBACK", result.llm.path === "online-fallback" ? "live" : "fallback");
  } else {
    setBadge("response-badge", "LIVE", "live");
  }

  fillList("redaction-list", result.redactions, "No sensitive fields required masking.");
  fillList("threat-list", result.threat.reasons, "No threat indicators detected.");
  renderTimeline(result.timeline);
  renderDocs(result.retrieval.documents, result.retrieval.restricted_exposure_prevented);
}

async function submitQuery() {
  const query = document.getElementById("query").value.trim();
  const role = document.getElementById("role").value;
  if (!query) {
    alert("Enter a query first.");
    return;
  }

  const submit = document.getElementById("submit");
  submit.disabled = true;
  submit.textContent = "Processing...";

  try {
    const result = await fetchJson("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, role }),
    });
    renderResult(result);
  } catch (error) {
    alert(error.message);
  } finally {
    submit.disabled = false;
    submit.textContent = "Process Through EdgeGuard";
  }
}

async function initialize() {
  try {
    const [config, scenarioPayload] = await Promise.all([
      fetchJson("/api/config"),
      fetchJson("/api/scenarios"),
    ]);
    setBackendStatus(config);
    populateScenarios(scenarioPayload.items || []);
  } catch (error) {
    document.getElementById("backend-status").textContent = error.message;
  }
}

document.getElementById("submit").addEventListener("click", submitQuery);
document.getElementById("run-demo").addEventListener("click", () => {
  if (!state.selectedScenarioId && state.scenarios.length > 0) {
    selectScenario(state.scenarios[0].id);
  }
  submitQuery();
});
document.getElementById("scenario-select").addEventListener("change", (event) => {
  if (!event.target.value) return;
  selectScenario(event.target.value);
});

initialize();
