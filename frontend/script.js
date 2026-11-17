/* =====================================================
   CYBERCORE FRONTEND
   English + Hindi
   ===================================================== */


/* ================= LANGUAGE DATA ================= */

const translations = {

    en: {

        workspace: "WORKSPACE",

        dashboard: "Dashboard",
        cases: "Cases",
        evidence: "Evidence",
        device: "Device Correlation",
        email: "Email Analysis",
        graph: "Unified Graph",
        timeline: "Timeline",
        findings: "Findings",
        dossier: "Entity Dossier",
        system: "System Status",

        offlineMode: "Offline Mode",
        localProcessing: "Local processing enabled",

        about: "About",

        heroTitle: "Unified Cyber Fraud Intelligence",

        heroText:
            "Analyze, correlate and visualize fragmented cyber-fraud evidence in one secure workspace.",

        uploadArtifact: "Upload Artifact",

        startAnalysis: "Start Analysis",

        totalCases: "Total Cases",
        highRisk: "High Risk",
        avgRisk: "Avg. Risk Score",
        suspiciousEntities: "Suspicious Entities",
        connectedArtifacts: "Connected Artifacts",

        thisMonth: "this month",

        artifactIngestion: "Artifact Ingestion",

        uploadDescription:
            "Upload suspicious digital evidence",

        dropFiles: "Drop files here",

        supportedFiles:
            "or click to browse • CSV, JSON, TXT, EML, PDF",

        browseFiles: "Browse Files",

        forensicPipeline: "Forensic Pipeline",

        pipelineDescription:
            "Evidence processing workflow",

        connectionGraph: "Connection Graph",

        graphDescription:
            "Entity relationships and transaction flow",

        viewFullGraph: "View Full Graph",

        riskOverview: "Risk Overview",

        riskDescription:
            "Highest priority entities",

        recentCases: "Recent Investigations",

        recentDescription:
            "Latest activity across your workspace",

        viewAll: "View All",

        aboutCyberCore: "About CyberCore",

        whatIsCyberCore: "What is CyberCore?",

        howItWorks: "How it Works",

        forensicIntegrity: "Forensic Integrity"

    },


    hi: {

        workspace: "वर्कस्पेस",

        dashboard: "डैशबोर्ड",
        cases: "केसेस",
        evidence: "एविडेंस",
        device: "डिवाइस कॉरिलेशन",
        email: "ईमेल एनालिसिस",
        graph: "यूनिफाइड ग्राफ",
        timeline: "टाइमलाइन",
        findings: "फाइंडिंग्स",
        dossier: "एंटिटी डॉसियर",
        system: "सिस्टम स्टेटस",

        offlineMode: "ऑफलाइन मोड",
        localProcessing: "लोकल प्रोसेसिंग सक्षम",

        about: "अबाउट",

        heroTitle: "यूनिफाइड साइबर फ्रॉड इंटेलिजेंस",

        heroText:
            "एक सुरक्षित वर्कस्पेस में साइबर फ्रॉड से जुड़े डिजिटल एविडेंस का विश्लेषण, कॉरिलेशन और विज़ुअलाइज़ेशन करें।",

        uploadArtifact: "आर्टिफैक्ट अपलोड करें",

        startAnalysis: "एनालिसिस शुरू करें",

        totalCases: "कुल केसेस",
        highRisk: "हाई रिस्क",
        avgRisk: "औसत रिस्क स्कोर",
        suspiciousEntities: "संदिग्ध एंटिटीज़",
        connectedArtifacts: "कनेक्टेड आर्टिफैक्ट्स",

        thisMonth: "इस महीने",

        artifactIngestion: "आर्टिफैक्ट इनजेशन",

        uploadDescription:
            "संदिग्ध डिजिटल एविडेंस अपलोड करें",

        dropFiles: "फाइल यहाँ ड्रॉप करें",

        supportedFiles:
            "या ब्राउज़ करने के लिए क्लिक करें • CSV, JSON, TXT, EML, PDF",

        browseFiles: "फाइल ब्राउज़ करें",

        forensicPipeline: "फॉरेंसिक पाइपलाइन",

        pipelineDescription:
            "एविडेंस प्रोसेसिंग वर्कफ़्लो",

        connectionGraph: "कनेक्शन ग्राफ",

        graphDescription:
            "एंटिटी रिलेशनशिप और ट्रांजैक्शन फ्लो",

        viewFullGraph: "पूरा ग्राफ देखें",

        riskOverview: "रिस्क ओवरव्यू",

        riskDescription:
            "सबसे महत्वपूर्ण संदिग्ध एंटिटीज़",

        recentCases: "हाल की जांच",

        recentDescription:
            "आपके वर्कस्पेस की हाल की गतिविधियां",

        viewAll: "सभी देखें",

        aboutCyberCore: "CyberCore के बारे में",

        whatIsCyberCore: "CyberCore क्या है?",

        howItWorks: "यह कैसे काम करता है?",

        forensicIntegrity: "फॉरेंसिक इंटीग्रिटी"

    }

};


/* ================= CURRENT LANGUAGE ================= */

let currentLang = "en";

/* ================= BACKEND API =================
   Local default: http://127.0.0.1:8000
   Render builds frontend/api-config.js with the deployed API URL.
*/
const API_BASE = window.__API_BASE__ || "http://127.0.0.1:8000";
let currentCaseId = null;
let lastAnalysis = null;



/* ================= LANGUAGE FUNCTION ================= */

function applyLanguage(lang) {

    currentLang = lang;

    document.documentElement.lang = lang;

    const elements = document.querySelectorAll("[data-i18n]");

    elements.forEach(element => {

        const key = element.getAttribute("data-i18n");

        if (translations[lang][key]) {
            element.textContent = translations[lang][key];
        }

    });


    document.getElementById("currentLanguage").textContent =
        lang === "en" ? "English" : "हिंदी";

}


/* ================= LANGUAGE MENU ================= */

const languageBtn =
    document.getElementById("languageBtn");

const languageMenu =
    document.getElementById("languageMenu");


languageBtn.addEventListener("click", function () {

    languageMenu.classList.toggle("show");

});


document.querySelectorAll("[data-lang]").forEach(button => {

    button.addEventListener("click", function () {

        const lang = this.dataset.lang;

        applyLanguage(lang);

        languageMenu.classList.remove("show");

        showToast(
            lang === "en"
                ? "Language changed to English"
                : "भाषा हिंदी में बदल दी गई"
        );

    });

});


document.addEventListener("click", function (event) {

    if (
        !event.target.closest(".language-wrapper")
    ) {

        languageMenu.classList.remove("show");

    }

});


/* ================= ABOUT MODAL ================= */

const aboutBtn =
    document.getElementById("aboutBtn");

const aboutModal =
    document.getElementById("aboutModal");

const closeAbout =
    document.getElementById("closeAbout");


aboutBtn.addEventListener("click", function () {

    aboutModal.classList.add("show");

});


closeAbout.addEventListener("click", function () {

    aboutModal.classList.remove("show");

});


aboutModal.addEventListener("click", function (event) {

    if (event.target === aboutModal) {

        aboutModal.classList.remove("show");

    }

});


/* ================= ABOUT TABS ================= */

const aboutTabs =
    document.querySelectorAll(".about-tab");

const aboutSections =
    document.querySelectorAll(".about-section");


aboutTabs.forEach(tab => {

    tab.addEventListener("click", function () {

        const selectedTab =
            this.dataset.tab;


        aboutTabs.forEach(item => {

            item.classList.remove("active");

        });


        aboutSections.forEach(section => {

            section.classList.remove("active");

        });


        this.classList.add("active");


        document
            .getElementById(selectedTab + "Tab")
            .classList.add("active");

    });

});


/* ================= SIDEBAR NAVIGATION ================= */

const navItems =
    document.querySelectorAll(".nav-item");


const dashboardPage =
    document.getElementById("dashboardPage");

const modulePage =
    document.getElementById("modulePage");

const pageTitle =
    document.getElementById("pageTitle");

const moduleTitle =
    document.getElementById("moduleTitle");

const moduleDescription =
    document.getElementById("moduleDescription");

const moduleCard1 =
    document.getElementById("moduleCard1");

const moduleCardText =
    document.getElementById("moduleCardText");

const moduleBottomTitle =
    document.getElementById("moduleBottomTitle");

const moduleBottomText =
    document.getElementById("moduleBottomText");

const evidenceWorkspace =
    document.getElementById("evidenceWorkspace");

const casesWorkspace =
    document.getElementById("casesWorkspace");

const reportWorkspace =
    document.getElementById("reportWorkspace");

const caseFileInput = document.getElementById("caseFileInput");
const caseBrowseBtn = document.getElementById("caseBrowseBtn");
const caseDropZone = document.getElementById("caseDropZone");
const caseFileList = document.getElementById("caseFileList");
const caseList = document.getElementById("caseList");
const caseAnalyzeBtn = document.getElementById("caseAnalyzeBtn");
const caseReportBtn = document.getElementById("caseReportBtn");
const caseTerminateBtn = document.getElementById("caseTerminateBtn");
const generateReportBtn = document.getElementById("generateReportBtn");
const downloadJsonBtn = document.getElementById("downloadJsonBtn");
const downloadPdfBtn = document.getElementById("downloadPdfBtn");
const reportSummary = document.getElementById("reportSummary");
const reportStatus = document.getElementById("reportStatus");
let currentReport = null;
let cachedCases = [];

const moduleGrid =
    document.getElementById("moduleGrid");

const moduleEmptyState =
    document.querySelector("#modulePage .empty-module");
const timelineWorkspace = document.getElementById("timelineWorkspace");
const findingsWorkspace = document.getElementById("findingsWorkspace");
const dossierWorkspace = document.getElementById("dossierWorkspace");
const copilotWorkspace = document.getElementById("copilotWorkspace");
const copilotQuestion = document.getElementById("copilotQuestion");
const copilotAskBtn = document.getElementById("copilotAskBtn");
const copilotState = document.getElementById("copilotState");
const copilotAnswer = document.getElementById("copilotAnswer");
const copilotAnswerText = document.getElementById("copilotAnswerText");
const copilotAnswerMode = document.getElementById("copilotAnswerMode");
const copilotModeStatus = document.getElementById("copilotModeStatus");
const copilotProcessingStatus = document.getElementById("copilotProcessingStatus");
const copilotModelStatus = document.getElementById("copilotModelStatus");
const copilotToolsStatus = document.getElementById("copilotToolsStatus");
const copilotToolUsed = document.getElementById("copilotToolUsed");
const copilotArguments = document.getElementById("copilotArguments");
const copilotSources = document.getElementById("copilotSources");
const copilotResult = document.getElementById("copilotResult");
const copilotLimitations = document.getElementById("copilotLimitations");
const dossierGraphBtn = document.getElementById("dossierGraphBtn");
let dossierEntityId = null;
let timelineNewestFirst = true;


const modules = {

    cases: {
        title: "Cases",
        description: "Manage and investigate cyber-fraud cases.",
        card: "Case Management",
        cardText: "Create, monitor and investigate cyber-fraud cases.",
        bottom: "Case Workspace",
        bottomText: "Select a case to open its complete investigation workspace."
    },

    evidence: {
        title: "Evidence",
        description: "Manage digital artifacts and evidence.",
        card: "Evidence Repository",
        cardText: "Upload and organize CDR, IPDR, bank, UPI, email and device artifacts.",
        bottom: "Evidence Analysis",
        bottomText: "Upload evidence to begin forensic processing."
    },

    fundtrace: {
        title: "FundTrace",
        description: "Trace suspicious financial transaction networks.",
        card: "Transaction Graph",
        cardText: "Identify multi-hop routing, fan-in, fan-out and suspicious accounts.",
        bottom: "Financial Investigation",
        bottomText: "Analyze transaction flow from victim to cash-out points."
    },

    device: {
        title: "Device Correlation",
        description: "Correlate devices, SIMs, IMEI and network identifiers.",
        card: "Device Intelligence",
        cardText: "Identify shared IMEI, IMSI, MAC addresses and SIM switching patterns.",
        bottom: "Device Investigation",
        bottomText: "Find relationships between devices and suspicious entities."
    },

    email: {
        title: "Email Analysis",
        description: "Analyze suspicious email headers and metadata.",
        card: "Email Forensics",
        cardText: "Inspect sender information, headers, domains and suspicious indicators.",
        bottom: "Email Investigation",
        bottomText: "Upload an EML file to begin header analysis."
    },

    graph: {
        title: "Unified Graph",
        description: "Visualize relationships between connected entities.",
        card: "Relationship Graph",
        cardText: "Explore relationships between accounts, phones, IPs, devices and URLs.",
        bottom: "Network Intelligence",
        bottomText: "Select an entity to explore its connected network."
    },

    timeline: {
        title: "Timeline",
        description: "View chronological events across a case.",
        card: "Investigation Timeline",
        cardText: "Combine transactions, calls, emails and device events into one timeline.",
        bottom: "Chronological Analysis",
        bottomText: "Events will appear here after evidence correlation."
    },

    findings: {
        title: "Findings",
        description: "Review suspicious patterns and investigation findings.",
        card: "Risk Findings",
        cardText: "Review explainable risk indicators detected across evidence.",
        bottom: "Investigation Findings",
        bottomText: "High-priority findings will appear after analysis."
    },

    dossier: {
        title: "Entity Dossier",
        description: "Build a detailed profile of suspicious entities.",
        card: "Entity Profile",
        cardText: "View identifiers, linked artifacts, risk score and relationships.",
        bottom: "Entity Intelligence",
        bottomText: "Select an entity to view its complete dossier."
    },

    copilot: {
        title: "AI Copilot",
        description: "Grounded investigation assistance.",
        card: "Investigator Assistant",
        cardText: "Ask questions about evidence, relationships and investigation findings.",
        bottom: "AI Investigation Copilot",
        bottomText: "The copilot can assist with grounded case analysis."
    },

    report: {
        title: "Investigation Report",
        description: "Review the evidence-backed case report.",
        card: "Report Output",
        cardText: "Generate a structured investigation report from the current case.",
        bottom: "Evidence and Findings",
        bottomText: "Select a case and complete analysis before generating the final report."
    },

    system: {
        title: "System Status",
        description: "Monitor CyberCore system and processing status.",
        card: "System Health",
        cardText: "Monitor local processing, storage and analysis services.",
        bottom: "System Ready",
        bottomText: "All core frontend services are currently available."
    }

};


navItems.forEach(item => {

    item.addEventListener("click", function () {

        navItems.forEach(nav => {

            nav.classList.remove("active");

        });

        this.classList.add("active");


        const page =
            this.dataset.page;

        const isEvidencePage = page === "evidence";
        const isCasesPage = page === "cases";
        const isReportPage = page === "report";
        const isGraphPage = page === "graph";
        const isCleanPage = isEvidencePage || isGraphPage || ["timeline", "findings", "dossier", "copilot"].includes(page);
        if (evidenceWorkspace) evidenceWorkspace.classList.toggle("active", isEvidencePage);
        if (casesWorkspace) casesWorkspace.classList.toggle("active", isCasesPage);
        modulePage.classList.toggle("focused-workspace", isCleanPage);
        [timelineWorkspace, findingsWorkspace, dossierWorkspace, copilotWorkspace].forEach(workspace => {
            if (workspace) workspace.classList.remove("active");
        });
        if (page === "timeline") timelineWorkspace?.classList.add("active");
        if (page === "findings") findingsWorkspace?.classList.add("active");
        if (page === "dossier") dossierWorkspace?.classList.add("active");
        if (page === "copilot") {
            copilotWorkspace?.classList.add("active");
            loadCopilotWorkspace();
        }
        if (reportWorkspace) reportWorkspace.style.display = isReportPage ? "block" : "none";
        if (moduleGrid) moduleGrid.style.display = isEvidencePage || isGraphPage || isCasesPage || isReportPage || page === "copilot" ? "none" : "";
        if (moduleEmptyState) moduleEmptyState.style.display = isEvidencePage || isGraphPage || isCasesPage || isReportPage || page === "copilot" ? "none" : "";

        if (isCasesPage) loadCasesWorkspace();
        if (isEvidencePage) loadEvidenceWorkspace();
        if (isGraphPage) {
            renderUnifiedGraph();
        }
        if (page === "timeline") loadTimelineWorkspace();
        if (page === "findings") loadFindingsWorkspace();
        if (page === "dossier") loadDossierWorkspace();
        if (isReportPage) loadReportWorkspace();


        if (page === "dashboard") {

            dashboardPage.classList.add("active-page");
            modulePage.classList.remove("active-page");

            pageTitle.textContent = "Dashboard";

            return;

        }


        dashboardPage.classList.remove("active-page");
        modulePage.classList.add("active-page");


        const data = modules[page];

        if (!data) return;


        pageTitle.textContent =
            data.title;

        moduleTitle.textContent =
            data.title;

        moduleDescription.textContent =
            data.description;

        moduleCard1.textContent =
            data.card;

        moduleCardText.textContent =
            data.cardText;

        moduleBottomTitle.textContent =
            data.bottom;

        moduleBottomText.textContent =
            data.bottomText;


        if (page === "graph") {
            renderUnifiedGraph();
        } else {
            const graphPanel = document.getElementById("unifiedGraphPanel");
            const placeholder = document.querySelector(".empty-module");
            if (graphPanel) graphPanel.classList.remove("active");
            if (placeholder) placeholder.style.display = "";
        }

    });

});


document.querySelectorAll(".top-btn[data-page]").forEach(action => {

    action.addEventListener("click", function () {

        const target = document.querySelector(
            `.nav-item[data-page="${this.dataset.page}"]`
        );

        if (target) {
            target.click();
            return;
        }

        const data = modules[this.dataset.page];
        if (!data) return;

        navItems.forEach(nav => nav.classList.remove("active"));
        dashboardPage.classList.remove("active-page");
        modulePage.classList.add("active-page");
        modulePage.classList.toggle("focused-workspace", ["evidence", "graph", "timeline", "findings", "dossier"].includes(this.dataset.page));
        if (reportWorkspace) reportWorkspace.style.display = this.dataset.page === "report" ? "block" : "none";
        if (moduleGrid) moduleGrid.style.display = ["report", "evidence", "graph", "timeline", "findings", "dossier"].includes(this.dataset.page) ? "none" : "";
        if (moduleEmptyState) moduleEmptyState.style.display = ["report", "evidence", "graph", "timeline", "findings", "dossier"].includes(this.dataset.page) ? "none" : "";
        evidenceWorkspace?.classList.toggle("active", this.dataset.page === "evidence");
        [timelineWorkspace, findingsWorkspace, dossierWorkspace].forEach(workspace => workspace?.classList.remove("active"));
        if (this.dataset.page === "timeline") timelineWorkspace?.classList.add("active");
        if (this.dataset.page === "findings") findingsWorkspace?.classList.add("active");
        if (this.dataset.page === "dossier") dossierWorkspace?.classList.add("active");
        pageTitle.textContent = data.title;
        moduleTitle.textContent = data.title;
        moduleDescription.textContent = data.description;
        moduleCard1.textContent = data.card;
        moduleCardText.textContent = data.cardText;
        moduleBottomTitle.textContent = data.bottom;
        moduleBottomText.textContent = data.bottomText;

        if (this.dataset.page === "report") loadReportWorkspace();
        if (this.dataset.page === "evidence") loadEvidenceWorkspace();
        if (this.dataset.page === "graph") {
            renderUnifiedGraph();
        }
        if (this.dataset.page === "timeline") loadTimelineWorkspace();
        if (this.dataset.page === "findings") loadFindingsWorkspace();
        if (this.dataset.page === "dossier") loadDossierWorkspace();

    });

});


/* ================= UNIFIED GRAPH (REAL DATA) ================= */

async function renderUnifiedGraph() {

    const graphPanel = document.getElementById("unifiedGraphPanel");
    const placeholder = document.querySelector(".empty-module");
    const svg = document.getElementById("unifiedGraphSvg");
    const caseLabel = document.getElementById("unifiedGraphCaseId");

    if (!currentCaseId) {
        if (graphPanel) graphPanel.classList.remove("active");
        if (placeholder) placeholder.style.display = "";
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE}/cases/${currentCaseId}/unified-graph`
        );

        if (!response.ok) {
            throw new Error(await readApiError(response));
        }

        const data = await response.json();

        if (!data.nodes || data.nodes.length === 0) {
            if (graphPanel) graphPanel.classList.add("active");
            const readout = document.getElementById("unifiedGraphReadout");
            if (readout) readout.textContent = "No graph relationships were returned for this case.";
            return;
        }

        if (placeholder) placeholder.style.display = "none";
        if (graphPanel) graphPanel.classList.add("active");
        if (caseLabel) caseLabel.textContent = `CASE-${String(currentCaseId).padStart(4, "0")}`;

        drawGraphSvg(svg, data.nodes, data.edges, "unifiedGraphReadout");

    } catch (error) {
        console.error("Unified graph error:", error);
        if (graphPanel) graphPanel.classList.remove("active");
        if (placeholder) placeholder.style.display = "";
    }
}

async function renderConnectionGraph() {
    const graphPanel = document.getElementById("connectionGraphPanel");
    const svg = document.getElementById("connectionGraphSvg");
    const caseLabel = document.getElementById("connectionGraphCaseId");
    const readout = document.getElementById("connectionGraphReadout");
    if (!currentCaseId) return;

    try {
        const response = await fetch(`${API_BASE}/cases/${currentCaseId}/unified-graph`);
        if (!response.ok) throw new Error(await readApiError(response));
        const data = await response.json();
        graphPanel?.classList.add("active");
        if (caseLabel) caseLabel.textContent = `CASE-${String(currentCaseId).padStart(4, "0")}`;
        if (readout) readout.textContent = data.nodes?.length
            ? "Connections show entities, amounts, transaction IDs, and relationship types from this case."
            : "No connections were returned for this case.";
        if (data.nodes?.length) drawConnectionGraphSvg(svg, data.nodes, data.edges);
    } catch (error) {
        if (readout) readout.textContent = `Unable to load connection graph: ${error.message}`;
    }
}

function drawConnectionGraphSvg(svg, nodes, edges) {
    const NS = "http://www.w3.org/2000/svg";
    while (svg.firstChild) svg.removeChild(svg.firstChild);

    const width = 900;
    const height = 480;
    const positions = {};
    const degree = {};

    edges.forEach(edge => {
        degree[edge.source] = (degree[edge.source] || 0) + 1;
        degree[edge.target] = (degree[edge.target] || 0) + 1;
    });

    // Use a small deterministic force layout so connections form a network
    // instead of a ring while keeping the output stable between refreshes.
    const initialColumns = Math.min(7, Math.max(1, Math.ceil(Math.sqrt(nodes.length))));
    nodes.forEach((node, index) => {
        positions[node.id] = {
            x: 90 + (index % initialColumns) * ((width - 180) / Math.max(1, initialColumns - 1)),
            y: 65 + Math.floor(index / initialColumns) * 70
        };
    });

    for (let iteration = 0; iteration < 90; iteration += 1) {
        const movement = {};
        nodes.forEach(node => {
            movement[node.id] = { x: 0, y: 0 };
        });

        for (let first = 0; first < nodes.length; first += 1) {
            for (let second = first + 1; second < nodes.length; second += 1) {
                const a = positions[nodes[first].id];
                const b = positions[nodes[second].id];
                const dx = b.x - a.x;
                const dy = b.y - a.y;
                const distance = Math.max(24, Math.sqrt(dx * dx + dy * dy));
                const force = 900 / (distance * distance);
                const xForce = (dx / distance) * force;
                const yForce = (dy / distance) * force;
                movement[nodes[first].id].x -= xForce;
                movement[nodes[first].id].y -= yForce;
                movement[nodes[second].id].x += xForce;
                movement[nodes[second].id].y += yForce;
            }
        }

        edges.forEach(edge => {
            const a = positions[edge.source];
            const b = positions[edge.target];
            if (!a || !b) return;
            const dx = b.x - a.x;
            const dy = b.y - a.y;
            const distance = Math.max(1, Math.sqrt(dx * dx + dy * dy));
            const force = (distance - 105) * 0.006;
            const xForce = (dx / distance) * force;
            const yForce = (dy / distance) * force;
            movement[edge.source].x += xForce;
            movement[edge.source].y += yForce;
            movement[edge.target].x -= xForce;
            movement[edge.target].y -= yForce;
        });

        nodes.forEach(node => {
            const position = positions[node.id];
            position.x = Math.max(45, Math.min(width - 45, position.x + movement[node.id].x));
            position.y = Math.max(35, Math.min(height - 35, position.y + movement[node.id].y));
        });
    }

    const edgeColor = {
        financial: "#338dff",
        device: "#f6c344",
        email: "#ef6574"
    };

    edges.forEach(edge => {
        const from = positions[edge.source];
        const to = positions[edge.target];
        if (!from || !to) return;

        const line = document.createElementNS(NS, "line");
        line.setAttribute("x1", from.x);
        line.setAttribute("y1", from.y);
        line.setAttribute("x2", to.x);
        line.setAttribute("y2", to.y);
        line.setAttribute("class", "connection-edge");
        line.setAttribute("stroke", edgeColor[edge.kind] || "#6d91aa");
        line.setAttribute("stroke-dasharray", edge.kind === "device" ? "7 5" : "");
        const title = document.createElementNS(NS, "title");
        title.textContent = `${edge.kind || "link"}${edge.transaction_id ? ` · ${edge.transaction_id}` : ""}${edge.amount != null ? ` · ${edge.amount}` : ""}`;
        line.appendChild(title);
        svg.appendChild(line);

        const label = document.createElementNS(NS, "text");
        label.setAttribute("x", (from.x + to.x) / 2);
        label.setAttribute("y", (from.y + to.y) / 2 - 6);
        label.setAttribute("class", "connection-edge-label");
        label.textContent = edge.amount != null
            ? `${edge.transaction_id || edge.kind} · ${edge.amount}`
            : (edge.kind || "link");
        svg.appendChild(label);
    });

    nodes.forEach(node => {
        const position = positions[node.id];
        const nodeDegree = degree[node.id] || 0;
        const group = document.createElementNS(NS, "g");
        group.setAttribute("class", "connection-node");
        group.addEventListener("click", () => {
            const readout = document.getElementById("connectionGraphReadout");
            if (readout) readout.textContent = `${node.id} · ${nodeDegree} visible connection(s)`;
            dossierEntityId = String(node.id);
            document.querySelector(".nav-item[data-page='dossier']")?.click();
        });

        const circle = document.createElementNS(NS, "circle");
        circle.setAttribute("cx", position.x);
        circle.setAttribute("cy", position.y);
        circle.setAttribute("r", Math.min(28, 17 + nodeDegree * 2));
        circle.setAttribute("class", nodeDegree >= 4 ? "connection-node-high" : nodeDegree >= 2 ? "connection-node-medium" : "connection-node-normal");
        group.appendChild(circle);

        const label = document.createElementNS(NS, "text");
        label.setAttribute("x", position.x);
        label.setAttribute("y", position.y + 42);
        label.setAttribute("class", "connection-node-label");
        label.textContent = String(node.id).length > 17 ? `${String(node.id).slice(0, 16)}...` : node.id;
        group.appendChild(label);
        svg.appendChild(group);
    });
}

function drawGraphSvg(svg, nodes, edges, readoutId = "unifiedGraphReadout") {

    const NS = "http://www.w3.org/2000/svg";

    while (svg.firstChild) {
        svg.removeChild(svg.firstChild);
    }

    const width = 900;
    const height = 480;
    const centerX = width / 2;
    const centerY = height / 2;
    const positions = {};
    const radius = Math.min(width, height) / 2 - 60;

    nodes.forEach((node, index) => {
        const angle = (2 * Math.PI * index) / nodes.length;
        positions[node.id] = {
            x: centerX + radius * Math.cos(angle),
            y: centerY + radius * Math.sin(angle)
        };
    });

    edges.forEach(edge => {

        const from = positions[edge.source];
        const to = positions[edge.target];

        if (!from || !to) return;

        const line = document.createElementNS(NS, "line");
        line.setAttribute("x1", from.x);
        line.setAttribute("y1", from.y);
        line.setAttribute("x2", to.x);
        line.setAttribute("y2", to.y);
        line.setAttribute("class", "graph-edge-" + (edge.kind || "financial"));

        let title = edge.kind || "";
        if (edge.amount) title += ": " + edge.amount;
        if (edge.transaction_id) title += " (" + edge.transaction_id + ")";

        const titleEl = document.createElementNS(NS, "title");
        titleEl.textContent = title;
        line.appendChild(titleEl);

        svg.appendChild(line);

        const edgeLabel = document.createElementNS(NS, "text");
        edgeLabel.setAttribute("x", (from.x + to.x) / 2);
        edgeLabel.setAttribute("y", (from.y + to.y) / 2 - 5);
        edgeLabel.setAttribute("class", "graph-edge-label");
        const edgeName = edge.transaction_id || edge.kind || "link";
        edgeLabel.textContent = edge.amount != null ? `${edgeName} · ${edge.amount}` : edgeName;
        svg.appendChild(edgeLabel);

    });

    nodes.forEach(node => {

        const pos = positions[node.id];
        if (!pos) return;

        const circle = document.createElementNS(NS, "circle");
        circle.setAttribute("cx", pos.x);
        circle.setAttribute("cy", pos.y);
        circle.setAttribute("r", 6);
        circle.setAttribute("class", "graph-node-circle");
        circle.addEventListener("click", () => {
            const readout = document.getElementById(readoutId);
            const relationshipCount = edges.filter(edge => edge.source === node.id || edge.target === node.id).length;
            if (readout) readout.textContent = `${node.id} · ${relationshipCount} connected relationship(s)`;
            dossierEntityId = String(node.id);
            document.querySelector(".nav-item[data-page='dossier']")?.click();
        });

        const titleEl = document.createElementNS(NS, "title");
        titleEl.textContent = node.id;
        circle.appendChild(titleEl);

        svg.appendChild(circle);

        const label = document.createElementNS(NS, "text");
        label.setAttribute("x", pos.x + 9);
        label.setAttribute("y", pos.y + 3);
        label.setAttribute("class", "graph-node-label");

        const shortLabel = String(node.id).length > 14
            ? String(node.id).slice(0, 13) + "\u2026"
            : node.id;

        label.textContent = shortLabel;

        svg.appendChild(label);

    });
}


/* ================= FILE UPLOAD ================= */

const uploadBtn =
    document.getElementById("uploadBtn");

const browseBtn =
    document.getElementById("browseBtn");

const fileInput =
    document.getElementById("fileInput");

const dropZone =
    document.getElementById("dropZone");

const fileList =
    document.getElementById("fileList");

const evidenceBrowseBtn =
    document.getElementById("evidenceBrowseBtn");

const evidenceFileInput =
    document.getElementById("evidenceFileInput");

const evidenceDropZone =
    document.getElementById("evidenceDropZone");

const evidenceFileList =
    document.getElementById("evidenceFileList");

const evidenceCatalog = document.getElementById("evidenceCatalog");
const evidenceCaseTitle = document.getElementById("evidenceCaseTitle");
const evidenceCaseSubtitle = document.getElementById("evidenceCaseSubtitle");
const evidenceIntakeTitle = document.getElementById("evidenceIntakeTitle");
const evidenceIntakeSubtitle = document.getElementById("evidenceIntakeSubtitle");


if (uploadBtn && fileInput) {
    uploadBtn.addEventListener("click", function () {
        fileInput.click();
    });
}


if (browseBtn && fileInput) {
    browseBtn.addEventListener("click", function () {
        fileInput.click();
    });
}


if (fileInput) {
    fileInput.addEventListener("change", function () {
        handleFiles(this.files);
    });
}


if (dropZone) dropZone.addEventListener("dragover", function (event) {

    event.preventDefault();

    dropZone.classList.add("dragover");

});


if (dropZone) dropZone.addEventListener("dragleave", function () {

    dropZone.classList.remove("dragover");

});


if (dropZone) dropZone.addEventListener("drop", function (event) {

    event.preventDefault();

    dropZone.classList.remove("dragover");

    handleFiles(event.dataTransfer.files);

});

if (caseBrowseBtn && caseFileInput) {
    caseBrowseBtn.addEventListener("click", () => caseFileInput.click());
    caseFileInput.addEventListener("change", function () {
        handleFiles(this.files, caseFileList);
    });
}

if (caseDropZone) {
    caseDropZone.addEventListener("dragover", event => {
        event.preventDefault();
        caseDropZone.classList.add("dragover");
    });
    caseDropZone.addEventListener("dragleave", () => caseDropZone.classList.remove("dragover"));
    caseDropZone.addEventListener("drop", event => {
        event.preventDefault();
        caseDropZone.classList.remove("dragover");
        handleFiles(event.dataTransfer.files, caseFileList);
    });
}

if (evidenceBrowseBtn && evidenceFileInput && evidenceDropZone) {

    evidenceBrowseBtn.addEventListener("click", function () {
        evidenceFileInput.click();
    });

    evidenceFileInput.addEventListener("change", function () {
        handleFiles(this.files, evidenceFileList);
    });

    evidenceDropZone.addEventListener("dragover", function (event) {
        event.preventDefault();
        evidenceDropZone.classList.add("dragover");
    });

    evidenceDropZone.addEventListener("dragleave", function () {
        evidenceDropZone.classList.remove("dragover");
    });

    evidenceDropZone.addEventListener("drop", function (event) {
        event.preventDefault();
        evidenceDropZone.classList.remove("dragover");
        handleFiles(event.dataTransfer.files, evidenceFileList);
    });

}


const SUPPORTED_UPLOAD_EXTENSIONS = [
    ".csv",
    ".json",
    ".txt",
    ".html",
    ".htm",
    ".xlsx",
    ".xls",
    ".png",
    ".jpg",
    ".jpeg",
    ".eml",
    ".pdf"
];

async function handleFiles(files, targetList = fileList) {

    if (!targetList) return;
    targetList.innerHTML = "";

    if (!files.length) return;

    const supportedFiles = Array.from(files).filter(file => {
        const name = file.name.toLowerCase();
        return SUPPORTED_UPLOAD_EXTENSIONS.some(ext => name.endsWith(ext));
    });

    if (!supportedFiles.length) {
        showToast(
            currentLang === "en"
                ? "Please upload a supported file: CSV, JSON, TXT, HTML, XLSX, image, EML, or PDF"
                : "कृपया समर्थित फाइल अपलोड करें: CSV, JSON, TXT, HTML, XLSX, image, EML, या PDF"
        );
        return;
    }

    if (supportedFiles.length > 1) {
        showToast("Please upload one file at a time for the current backend pipeline.");
        return;
    }

    const file = supportedFiles[0];

    const item = document.createElement("div");
    item.className = "file-item";
    item.innerHTML = `
        <span>⏳</span>
        <strong>${escapeHtml(file.name)}</strong>
        <small>${formatSize(file.size)} • uploading...</small>
    `;
    targetList.appendChild(item);

    try {
        const isCaseEvidenceUpload = targetList === evidenceFileList || targetList === caseFileList;
        if (!currentCaseId && isCaseEvidenceUpload) {
            throw new Error("Select or create a case before uploading evidence");
        }

        const caseResponse = currentCaseId ? null : await fetch(`${API_BASE}/cases/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: `CyberCore Investigation - ${file.name}`
            })
        });

        if (caseResponse && !caseResponse.ok) {
            throw new Error(await readApiError(caseResponse));
        }

        if (caseResponse) {
            const caseData = await caseResponse.json();
            currentCaseId = caseData.id;
            setActiveCase(caseData);
        }

        const formData = new FormData();
        formData.append("file", file);

        let uploadUrl = `${API_BASE}/cases/${currentCaseId}/evidence`;
        const lowerName = file.name.toLowerCase();

        if (lowerName.endsWith(".eml")) {
            uploadUrl = `${API_BASE}/cases/${currentCaseId}/email-evidence`;
        } else if (lowerName.endsWith(".csv") || lowerName.endsWith(".xls") || lowerName.endsWith(".xlsx")) {
            const headerText = await file.text();
            const sniff = headerText.split(/\r?\n/)[0]?.toLowerCase() || "";
            if (sniff.includes("phone_number") || sniff.includes("imei") || sniff.includes("device")) {
                uploadUrl = `${API_BASE}/cases/${currentCaseId}/device-evidence`;
            }
        }

        const uploadResponse = await fetch(uploadUrl, {
            method: "POST",
            body: formData
        });

        if (!uploadResponse.ok) {
            throw new Error(await readApiError(uploadResponse));
        }

        const evidence = await uploadResponse.json();

        item.innerHTML = `
            <span>✓</span>
            <strong>${escapeHtml(file.name)}</strong>
            <small>${formatSize(file.size)} • ${evidence.filename || file.name} • Case #${currentCaseId}</small>
        `;

        showToast(
            currentLang === "en"
                ? `Evidence validated and stored in Case #${currentCaseId}`
                : `Evidence validate होकर Case #${currentCaseId} में store हो गया`
        );

        await refreshCaseOverview();
        renderUnifiedGraph();
        await loadCasesWorkspace();

    } catch (error) {

        item.innerHTML = `
            <span>✕</span>
            <strong>${escapeHtml(file.name)}</strong>
            <small>Upload failed</small>
        `;

        currentCaseId = null;

        showToast(`Backend error: ${error.message}`);
        console.error(error);
    }
}

function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    }[char]));
}

async function readApiError(response) {
    try {
        const data = await response.json();
        return data.detail || response.statusText;
    } catch {
        return response.statusText || "Request failed";
    }
}

function formatSize(bytes) {

    if (bytes < 1024) {

        return bytes + " B";

    }

    if (bytes < 1024 * 1024) {

        return (bytes / 1024).toFixed(1) + " KB";

    }

    return (bytes / (1024 * 1024)).toFixed(1) + " MB";

}

function setActiveCase(caseItem) {
    currentCaseId = caseItem.id;
    lastAnalysis = null;
    updateDashboardStats({
        risk_score: 0,
        risk_level: "LOW",
        total_transactions: 0,
        total_entities: 0,
        case_count: 1
    });
    const title = document.getElementById("activeCaseTitle");
    const description = document.getElementById("activeCaseDescription");
    const status = document.getElementById("activeCaseStatus");
    if (title) title.textContent = `${caseItem.case_number || `CASE-${caseItem.id}`} · ${caseItem.name}`;
    if (description) description.textContent = caseItem.status === "terminated"
        ? `Deleted permanently on ${new Date(caseItem.deletion_at).toLocaleDateString()}`
        : "Evidence is stored in this case and ready for analysis.";
    if (status) status.textContent = caseItem.status.toUpperCase();
    if (caseReportBtn) caseReportBtn.disabled = caseItem.status === "terminated";
    if (caseTerminateBtn) caseTerminateBtn.disabled = !caseItem.report_generated || caseItem.status === "terminated";
    if (evidenceIntakeTitle) evidenceIntakeTitle.textContent = `${caseItem.case_number || `CASE-${caseItem.id}`} Evidence Intake`;
    if (evidenceIntakeSubtitle) evidenceIntakeSubtitle.textContent = caseItem.status === "terminated"
        ? "Add a document to this terminated case or download its existing artifacts."
        : "Add documents to the selected case for forensic processing.";
    loadEvidenceWorkspace();
    renderConnectionGraph();
    loadTimelineWorkspace();
    loadFindingsWorkspace();
    if (document.getElementById("unifiedGraphPanel")?.classList.contains("active")) {
        renderUnifiedGraph();
    }
    if (dossierEntityId) loadDossierWorkspace(dossierEntityId);
    refreshCaseOverview().catch(error => {
        console.error("Active case risk refresh error:", error);
        showToast(`Risk refresh error: ${error.message}`);
    });
}

function currentCaseRequired(stateElement) {
    if (currentCaseId) return true;
    if (stateElement) stateElement.textContent = "Select a case in Cases before loading this workspace.";
    return false;
}

function entityLink(entityId) {
    const value = escapeHtml(entityId || "Unknown entity");
    return `<button class="entity-link" type="button" data-entity-id="${escapeHtml(entityId || "")}">${value}</button>`;
}

async function loadTimelineWorkspace() {
    const state = document.getElementById("timelineState");
    const list = document.getElementById("timelineList");
    if (!currentCaseId) await loadCasesWorkspace();
    if (!currentCaseRequired(state)) return;
    state.textContent = "Loading timeline...";
    try {
        const response = await fetch(`${API_BASE}/cases/${currentCaseId}/timeline`);
        if (!response.ok) throw new Error(await readApiError(response));
        const data = await response.json();
        const selectedType = document.getElementById("timelineTypeFilter")?.value || "all";
        const events = data.events.filter(event => selectedType === "all" || event.event_type === selectedType);
        events.sort((a, b) => (new Date(b.timestamp) - new Date(a.timestamp)) * (timelineNewestFirst ? 1 : -1));
        state.textContent = events.length ? `${events.length} normalized event(s)` : "No timeline events exist for this case.";
        list.innerHTML = events.map((event, index) => `
            <details class="timeline-event" ${index === 0 ? "open" : ""}>
                <summary><time>${new Date(event.timestamp).toLocaleString()}</time><span class="event-badge ${event.event_type}">${escapeHtml(event.event_type.toUpperCase())}</span><strong>${escapeHtml(event.summary || event.description)}</strong></summary>
                <div class="timeline-details"><p>${escapeHtml(event.description || "")}</p><p>Entities: ${(event.entity_ids || []).filter(Boolean).map(entityLink).join(" ") || "Not provided"}</p><p>Source: ${escapeHtml(event.source || "Not provided")}${event.amount != null ? ` · Amount: ${event.amount}` : ""}${event.transaction_id ? ` · Transaction: ${escapeHtml(event.transaction_id)}` : ""}</p></div>
            </details>`).join("");
    } catch (error) { state.textContent = `Unable to load timeline: ${error.message}`; list.innerHTML = ""; }
}

async function loadFindingsWorkspace() {
    const state = document.getElementById("findingsState");
    const list = document.getElementById("findingsList");
    if (!currentCaseId) await loadCasesWorkspace();
    if (!currentCaseRequired(state)) return;
    state.textContent = "Loading findings...";
    try {
        const response = await fetch(`${API_BASE}/cases/${currentCaseId}/findings`);
        if (!response.ok) throw new Error(await readApiError(response));
        const data = await response.json();
        const severity = document.getElementById("findingSeverityFilter")?.value || "all";
        const query = (document.getElementById("findingRuleFilter")?.value || "").toLowerCase();
        const findings = data.findings.filter(item => {
            const searchable = [item.rule, item.source, ...(item.affected_entities || [])].join(" ").toLowerCase();
            return (severity === "all" || item.severity === severity) && (!query || searchable.includes(query));
        });
        document.getElementById("findingsRiskScore").textContent = `${data.risk_score} / 10 (${data.risk_level})`;
        document.getElementById("riskCalculationText").textContent = `Score ${data.risk_score}/10 and level ${data.risk_level} were returned by the deterministic backend analysis.`;
        state.textContent = findings.length ? `${findings.length} finding(s)` : "No findings match the selected filter.";
        list.innerHTML = findings.map((finding, index) => `
            <details class="finding-card" ${index === 0 ? "open" : ""}><summary><span class="severity-badge ${String(finding.severity || "LOW").toLowerCase()}">${escapeHtml(finding.severity || "LOW")}</span><strong>${escapeHtml(finding.title || finding.type || "Investigative Finding")}</strong></summary>
            <div class="finding-details"><p>${escapeHtml(finding.description || finding.note || "No explanation provided.")}</p><p><b>Rule:</b> ${escapeHtml(finding.rule || finding.type || "Backend finding")}</p><p><b>Risk contribution:</b> ${finding.risk_contribution != null ? escapeHtml(finding.risk_contribution) : "Returned in aggregate risk score"}</p><p><b>Affected entities:</b> ${(finding.affected_entities || []).filter(Boolean).map(entityLink).join(" ") || "Not provided"}</p><p><b>Evidence:</b> ${escapeHtml(finding.source || "Case evidence")}</p></div></details>`).join("");
    } catch (error) { state.textContent = `Unable to load findings: ${error.message}`; list.innerHTML = ""; }
}

async function loadDossierWorkspace(entityId = dossierEntityId) {
    const state = document.getElementById("dossierState");
    const content = document.getElementById("dossierContent");
    if (!currentCaseId) await loadCasesWorkspace();
    if (!currentCaseRequired(state)) return;
    if (!entityId) { state.textContent = "Select an entity from the graph, timeline, or findings."; content.innerHTML = ""; return; }
    dossierEntityId = entityId;
    state.textContent = "Loading entity dossier...";
    try {
        const response = await fetch(`${API_BASE}/cases/${currentCaseId}/entities/${encodeURIComponent(entityId)}`);
        if (!response.ok) throw new Error(await readApiError(response));
        const data = await response.json();
        state.textContent = `${data.case_number} · ${data.entity.display_name}`;
        content.innerHTML = `<section class="dossier-header"><h3>${escapeHtml(data.entity.display_name)}</h3><p>Type: ${escapeHtml(data.entity.type)} · Risk: ${data.risk_score}/10 (${escapeHtml(data.risk_level)})</p></section><section><h3>Identifiers</h3><p>${escapeHtml(data.identifiers.value)}</p></section><section><h3>Transactions</h3>${data.transactions.length ? data.transactions.map(item => `<p>${escapeHtml(item.direction)} · ${escapeHtml(item.transaction_id)} · ${item.amount} · ${new Date(item.timestamp).toLocaleString()}</p>`).join("") : "<p>No transactions returned.</p>"}</section><section><h3>Connected Entities</h3><p>${data.connected_entities.length ? data.connected_entities.map(entityLink).join(" ") : "No connected entities returned."}</p></section><section><h3>Device Associations</h3>${data.device_associations.length ? data.device_associations.map(item => `<p>Phone ${escapeHtml(item.phone_number)} · IMEI ${escapeHtml(item.imei)} · ${escapeHtml(item.source)}</p>`).join("") : "<p>No device information returned.</p>"}</section><section><h3>Evidence References</h3>${data.evidence.map(item => `<p>${escapeHtml(item.filename)} · ${escapeHtml(item.kind)}</p>`).join("") || "<p>No evidence references returned.</p>"}</section>`;
    } catch (error) { state.textContent = `Unable to load dossier: ${error.message}`; content.innerHTML = ""; }
}

document.getElementById("timelineTypeFilter")?.addEventListener("change", loadTimelineWorkspace);
document.getElementById("findingSeverityFilter")?.addEventListener("change", loadFindingsWorkspace);
document.getElementById("findingRuleFilter")?.addEventListener("input", loadFindingsWorkspace);
document.getElementById("timelineSortBtn")?.addEventListener("click", event => {
    timelineNewestFirst = !timelineNewestFirst;
    event.currentTarget.textContent = timelineNewestFirst ? "Newest first" : "Oldest first";
    loadTimelineWorkspace();
});
document.addEventListener("click", event => {
    const entity = event.target.closest("[data-entity-id]");
    if (!entity || !entity.dataset.entityId) return;
    dossierEntityId = entity.dataset.entityId;
    document.querySelector(".nav-item[data-page='dossier']")?.click();
});

async function loadEvidenceWorkspace() {
    if (!currentCaseId) {
        if (!cachedCases.length) await loadCasesWorkspace();
        if (cachedCases.length) {
            setActiveCase(cachedCases[0]);
        } else {
            if (evidenceCatalog) evidenceCatalog.innerHTML = "<div><span>INFO</span><small>No cases or stored evidence yet.</small></div>";
            return;
        }
    }

    try {
        const response = await fetch(`${API_BASE}/cases/${currentCaseId}/evidence`);
        if (!response.ok) throw new Error(await readApiError(response));
        const data = await response.json();
        if (evidenceCaseTitle) evidenceCaseTitle.textContent = `${data.case_number} Evidence`;
        if (evidenceCaseSubtitle) evidenceCaseSubtitle.textContent = `${data.case_status.toUpperCase()} case documents and generated reports`;
        const graphCaseLabel = document.getElementById("connectionGraphCaseId");
        if (graphCaseLabel) graphCaseLabel.textContent = data.case_number;
        renderConnectionGraph();
        if (!evidenceCatalog) return;
        evidenceCatalog.innerHTML = data.items.length
            ? data.items.map(item => `
                <div class="evidence-catalog-item">
                    <span class="evidence-kind">${escapeHtml(item.kind.replace("report_", "").toUpperCase())}</span>
                    <div><strong>${escapeHtml(item.filename)}</strong><small>${item.kind === "case_document" ? "Uploaded case document" : "Generated investigation report"} · SHA-256 ${escapeHtml(item.sha256.slice(0, 12))}...</small></div>
                    <a class="table-action" href="${API_BASE}${item.download_url}" download>Download</a>
                </div>
            `).join("")
            : "<div><span>EMPTY</span><small>No stored documents or reports for this case yet.</small></div>";
    } catch (error) {
        if (evidenceCatalog) evidenceCatalog.innerHTML = `<div><span>ERROR</span><small>${escapeHtml(error.message)}</small></div>`;
    }
}

async function loadCasesWorkspace() {
    try {
        const response = await fetch(`${API_BASE}/cases/`);
        if (!response.ok) throw new Error(await readApiError(response));
        cachedCases = await response.json();
        if (!currentCaseId && cachedCases.length) setActiveCase(cachedCases[0]);
        if (caseList) {
            caseList.innerHTML = cachedCases.map(caseItem => `
                <button class="case-list-item ${caseItem.id === currentCaseId ? "active" : ""}" data-case-id="${caseItem.id}">
                    <strong>${caseItem.case_number}</strong>
                    <span>${escapeHtml(caseItem.name)}</span>
                    <small>${caseItem.status}${caseItem.status === "terminated" && caseItem.deletion_at ? ` · deletes ${new Date(caseItem.deletion_at).toLocaleDateString()}` : ""}</small>
                </button>
            `).join("") || "<p class='case-list-empty'>No cases yet. Upload evidence to create one.</p>";
        }
        updateDashboardCaseCounts(cachedCases);
    } catch (error) {
        console.error(error);
    }
}

async function createCaseAndAnalyze() {
    const caseName = `CyberCore Investigation - ${new Date().toLocaleString()}`;
    const response = await fetch(`${API_BASE}/cases/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: caseName })
    });
    if (!response.ok) throw new Error(await readApiError(response));

    const caseItem = await response.json();
    currentCaseId = caseItem.id;
    setActiveCase(caseItem);
    await loadCasesWorkspace();
    await refreshCaseOverview();
    renderUnifiedGraph();
    showToast(`Case ${caseItem.case_number} created and analysis is ready`);
}

function updateDashboardCaseCounts(cases) {
    const active = cases.filter(item => item.status === "active").length;
    const terminated = cases.filter(item => item.status === "terminated").length;
    const history = cases.filter(item => item.report_generated && item.status !== "active").length;
    const targets = {
        activeCasesCount: active,
        recentCasesCount: cases.length,
        caseHistoryCount: history,
        terminatedCasesCount: terminated
    };
    Object.entries(targets).forEach(([id, count]) => {
        const element = document.getElementById(id);
        if (element) element.textContent = count;
    });
}

document.addEventListener("click", event => {
    const item = event.target.closest("[data-case-id]");
    if (!item) return;
    if (item.dataset.action === "terminate-case") return;
    const selected = cachedCases.find(caseItem => caseItem.id === Number(item.dataset.caseId));
    if (selected) {
        setActiveCase(selected);
        if (item.closest("#recentCasesBody")) {
            document.querySelector(".nav-item[data-page='evidence']")?.click();
        } else {
            loadEvidenceWorkspace();
        }
    }
});

if (dossierGraphBtn) {
    dossierGraphBtn.addEventListener("click", () => {
        document.querySelector(".nav-item[data-page='graph']")?.click();
        renderUnifiedGraph();
    });
}

function formatCopilotArguments(argumentsData) {
    const entries = Object.entries(argumentsData || {});
    if (!entries.length) return "No additional filters were used.";
    return entries.map(([key, value]) => `${key.replaceAll("_", " ")}: ${value}`).join(". ") + ".";
}

function formatCopilotSources(sources) {
    if (!sources?.length) return "No source references were returned.";
    return sources.map(source => source.replaceAll("_", " ")).join(", ") + ".";
}

function formatCopilotResult(tool, result) {
    if (!result || typeof result !== "object") return "No structured result was returned.";
    if (tool === "find_entity") {
        const records = (result.matches || []).map(match => {
            const record = match.record || {};
            const details = Object.entries(record)
                .filter(([key, value]) => !["id", "case_id"].includes(key) && value !== null && value !== "")
                .map(([key, value]) => `${key.replaceAll("_", " ")}: ${value}`)
                .join(", ");
            return `${match.source}: ${details}`;
        });
        return `Found ${result.match_count} matching record(s). ${records.join(". ") || "No matching records were returned."}`;
    }
    if (tool === "get_transactions") {
        const transactions = (result.transactions || []).map(item =>
            `${item.transaction_id || "Unknown transaction"}: ${item.sender} sent ${item.amount} to ${item.receiver} on ${item.timestamp}`
        );
        return `Found ${result.transaction_count} matching transaction(s). ${transactions.join(". ") || "No matching transactions were returned."}`;
    }
    if (tool === "get_connected_entities") {
        return `Found ${result.connection_count} observed connected entit${result.connection_count === 1 ? "y" : "ies"}. Connected entities: ${(result.entities || []).join(", ") || "none"}.`;
    }
    if (tool === "get_risk_findings") {
        const signals = (result.signals || []).map(signal => `${signal.name} (+${signal.points})`).join(", ") || "no verified signals";
        return `Observed risk score: ${result.risk_score} out of 10, rated ${result.risk_level}. Verified signals: ${signals}.`;
    }
    if (tool === "get_fund_paths") return `Found ${result.chain_count} observed transaction chain(s).`;
    if (tool === "get_timeline") return `Found ${result.event_count} chronological event(s) in the case timeline.`;
    if (tool === "get_email_findings") return `Found ${result.finding_count} observed email finding(s).`;
    if (tool === "generate_case_brief") return "A verified case brief was generated from the analyzed evidence.";
    return "A verified forensic result was returned.";
}

async function loadCopilotWorkspace() {
    if (!currentCaseId) {
        copilotState.textContent = "Select a case to ask an evidence-grounded question.";
        copilotProcessingStatus.textContent = "Fallback available";
        copilotModelStatus.textContent = "No case selected";
        copilotToolsStatus.textContent = "-";
        return;
    }
    try {
        const response = await fetch(`${API_BASE}/cases/${currentCaseId}/copilot/tools`);
        if (!response.ok) throw new Error(await readApiError(response));
        const status = await response.json();
        copilotProcessingStatus.textContent = status.slm_enabled ? "Local SLM + fallback" : "Offline fallback";
        copilotModelStatus.textContent = status.slm_enabled ? status.model : "SLM disabled";
        copilotToolsStatus.textContent = `${status.tools.length} approved tools`;
        copilotModeStatus.textContent = status.slm_enabled ? "SLM READY" : "FALLBACK READY";
        copilotState.textContent = "Ask a question about the selected case evidence.";
    } catch (error) {
        copilotProcessingStatus.textContent = "Offline fallback";
        copilotModelStatus.textContent = "Status unavailable";
        copilotToolsStatus.textContent = "Fallback active";
        copilotModeStatus.textContent = "FALLBACK READY";
        copilotState.textContent = error.message;
    }
}

async function askCopilot() {
    if (!currentCaseId) {
        copilotState.textContent = "Select a case before asking Copilot.";
        return;
    }
    const question = copilotQuestion.value.trim();
    if (!question) {
        copilotState.textContent = "Enter an investigator question.";
        return;
    }
    copilotAskBtn.disabled = true;
    copilotState.textContent = "Analyzing verified case evidence...";
    try {
        const response = await fetch(`${API_BASE}/cases/${currentCaseId}/copilot/ask`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });
        if (!response.ok) throw new Error(await readApiError(response));
        const result = await response.json();
        copilotAnswer.hidden = false;
        copilotAnswerText.textContent = result.answer;
        copilotAnswerMode.textContent = result.mode === "slm" ? "SLM" : "FALLBACK";
        copilotToolUsed.textContent = result.tool || "No tool selected";
        copilotArguments.textContent = formatCopilotArguments(result.arguments);
        copilotSources.textContent = formatCopilotSources(result.grounded_on);
        copilotResult.textContent = formatCopilotResult(result.tool, result.result);
        copilotLimitations.textContent = result.limitations?.length ? `Limitations: ${result.limitations.join(" ")}` : "";
        copilotState.textContent = "Response grounded in the returned forensic result.";
    } catch (error) {
        copilotState.textContent = error.message;
    } finally {
        copilotAskBtn.disabled = false;
    }
}

if (copilotAskBtn) copilotAskBtn.addEventListener("click", () => askCopilot());
if (copilotQuestion) copilotQuestion.addEventListener("keydown", event => {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") askCopilot();
});

async function loadReportWorkspace() {
    if (!currentCaseId) {
        if (reportSummary) reportSummary.textContent = "Select a case in Cases before generating a report.";
        return;
    }
    const selected = cachedCases.find(caseItem => caseItem.id === currentCaseId);
    if (selected && reportStatus) reportStatus.textContent = selected.report_generated ? "GENERATED" : "NOT GENERATED";
    if (selected && reportSummary) reportSummary.textContent = `${selected.case_number}: ${selected.name}`;
}

async function generateReport() {
    if (!currentCaseId) return showToast("Select a case first");
    const response = await fetch(`${API_BASE}/cases/${currentCaseId}/report`);
    if (!response.ok) throw new Error(await readApiError(response));
    currentReport = await response.json();
    if (reportStatus) reportStatus.textContent = "GENERATED";
    if (reportSummary) reportSummary.textContent = `${currentReport.case.case_number}: report includes ${currentReport.evidence.length} evidence item(s), ${currentReport.timeline.length} timeline event(s), ${currentReport.findings.length} finding(s), and ${currentReport.entities.length} entities.`;
    if (downloadJsonBtn) downloadJsonBtn.disabled = false;
    if (downloadPdfBtn) downloadPdfBtn.disabled = false;
    if (caseTerminateBtn) caseTerminateBtn.disabled = false;
    if (caseReportBtn) caseReportBtn.disabled = false;
    await loadCasesWorkspace();
    showToast("Complete report generated");
}

function downloadJsonReport() {
    if (!currentReport) return;
    const link = document.createElement("a");
    link.href = URL.createObjectURL(new Blob([JSON.stringify(currentReport, null, 2)], { type: "application/json" }));
    link.download = `${currentReport.case.case_number.toLowerCase()}-report.json`;
    link.click();
    URL.revokeObjectURL(link.href);
}

async function downloadPdfReport() {
    if (!currentCaseId) return;
    const response = await fetch(`${API_BASE}/cases/${currentCaseId}/pdf-report`);
    if (!response.ok) throw new Error(await readApiError(response));
    const link = document.createElement("a");
    link.href = URL.createObjectURL(await response.blob());
    link.download = `case-${currentCaseId}-report.pdf`;
    link.click();
    URL.revokeObjectURL(link.href);
}

if (generateReportBtn) generateReportBtn.addEventListener("click", () => generateReport().catch(error => showToast(error.message)));
if (caseReportBtn) caseReportBtn.addEventListener("click", () => {
    document.querySelector(".top-btn[data-page='report']")?.click();
    generateReport().catch(error => showToast(error.message));
});
if (downloadJsonBtn) downloadJsonBtn.addEventListener("click", downloadJsonReport);
if (downloadPdfBtn) downloadPdfBtn.addEventListener("click", () => downloadPdfReport().catch(error => showToast(error.message)));
if (caseAnalyzeBtn) caseAnalyzeBtn.addEventListener("click", async () => {
    if (!currentCaseId) return showToast("Select a case first");
    try {
        await refreshCaseOverview();
        showToast("Analysis updated: timeline, findings and unified graph are ready");
        if (caseReportBtn) caseReportBtn.disabled = false;
    } catch (error) {
        showToast(`Analysis error: ${error.message}`);
    }
});
if (caseTerminateBtn) caseTerminateBtn.addEventListener("click", async () => {
    if (!currentCaseId) return;
    const response = await fetch(`${API_BASE}/cases/${currentCaseId}/terminate`, { method: "POST" });
    if (!response.ok) return showToast(await readApiError(response));
    showToast("Case terminated; permanent deletion is scheduled in 30 days");
    await loadCasesWorkspace();
    setActiveCase(await response.json());
});


/* ================= RECENT CASES ================= */

async function loadRecentCases() {
    const tbody = document.getElementById("recentCasesBody");
    if (!tbody) return;

    try {
        const response = await fetch(`${API_BASE}/cases/`);
        if (!response.ok) {
            throw new Error(await readApiError(response));
        }

        const cases = await response.json();

        cachedCases = cases;
        updateDashboardCaseCounts(cases);

        if (!cases.length) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7">No investigations yet.</td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = cases.map((caseItem) => {
            const statusText = caseItem.status === "terminated"
                ? "Terminated"
                : caseItem.report_generated ? "Report ready" : "Active";
            const statusClass = caseItem.status === "terminated"
                ? "closed"
                : caseItem.report_generated ? "processing" : "investigating";
            const age = `${Math.max(1, (caseItem.id % 5) + 1)} ${caseItem.id % 2 === 0 ? "min" : "hrs"} ago`;
            const deletionTimeline = caseItem.status === "terminated" && caseItem.deletion_at
                ? `Deletes ${new Date(caseItem.deletion_at).toLocaleDateString()}`
                : "";
            const terminationButton = caseItem.status === "terminated"
                ? `<span class="deletion-timeline">${deletionTimeline}</span>`
                : `<button class="table-action terminate-dashboard-btn" type="button" data-action="terminate-case" data-case-id="${caseItem.id}" ${caseItem.report_generated ? "" : "disabled"}>Terminate</button>`;

            return `
                <tr data-case-id="${caseItem.id}" class="case-table-row">
                    <td><strong>${caseItem.case_number || `CASE-${String(caseItem.id).padStart(4, "0")}`}</strong></td>
                    <td>${caseItem.name || "Fraud Analysis"}</td>
                    <td>${(caseItem.id * 3) % 20 + 5}</td>
                    <td><span class="risk-pill low-pill">Select case to calculate</span></td>
                    <td><span class="case-status ${statusClass}">${statusText}</span></td>
                    <td>${age}</td>
                    <td>${terminationButton}</td>
                </tr>
            `;
        }).join("");
    } catch (error) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7">Unable to load recent cases.</td>
            </tr>
        `;
        console.error(error);
    }
}

document.addEventListener("click", function (event) {
    const actionTarget = event.target.closest("[data-action]");
    if (!actionTarget) return;

    const action = actionTarget.dataset.action;

    if (action === "view-graph") {
        showToast(currentLang === "en" ? "Opening graph view..." : "ग्राफ व्यू खुल रहा है...");
        const graphButton = document.querySelector(".nav-item[data-page='graph']");
        if (graphButton) graphButton.click();
        return;
    }

    if (action === "view-all") {
        showToast(currentLang === "en" ? "Opening all investigations..." : "सभी जांचें खोल रही है...");
        const casesButton = document.querySelector(".nav-item[data-page='cases']");
        if (casesButton) casesButton.click();
        return;
    }

    if (action === "terminate-case") {
        const caseId = Number(actionTarget.dataset.caseId);
        if (!caseId || !confirm("Terminate this case? It will be permanently deleted after 30 days.")) return;
        fetch(`${API_BASE}/cases/${caseId}/terminate`, { method: "POST" })
            .then(async response => {
                if (!response.ok) throw new Error(await readApiError(response));
                showToast("Case terminated; deletion scheduled in 30 days");
                await loadRecentCases();
                await loadCasesWorkspace();
            })
            .catch(error => showToast(error.message));
        return;
    }

    if (action === "new-analysis" || action === "start-investigation") {
        createCaseAndAnalyze().catch(error => showToast(`Case creation error: ${error.message}`));
    }
});

/* ================= START ANALYSIS ================= */

const analysisBtn =
    document.getElementById("analysisBtn");


analysisBtn.addEventListener("click", async function () {

    if (!currentCaseId) {
        showToast(
            currentLang === "en"
                ? "Upload a valid evidence file first"
                : "पहले valid evidence file upload करें"
        );
        return;
    }

    analysisBtn.disabled = true;

    try {
        showToast(
            currentLang === "en"
                ? "Running Graph Engine and forensic analysis..."
                : "Graph Engine और forensic analysis चल रहा है..."
        );

        await refreshCaseOverview();
        renderUnifiedGraph();

        const activeStep = document.querySelector(".active-step");

        if (activeStep) {
            activeStep.classList.remove("active-step");
            activeStep.classList.add("completed");
            if (activeStep.querySelector("span")) {
                activeStep.querySelector("span").textContent = "✓";
            }
        }

        const riskValue = lastAnalysis && lastAnalysis.risk_score != null ? lastAnalysis.risk_score : 0;
        const riskLevel = lastAnalysis && lastAnalysis.risk_level ? lastAnalysis.risk_level : "LOW";

        showToast(
            currentLang === "en"
                ? `Analysis complete • Risk ${riskValue}/10 • ${riskLevel}`
                : `Analysis complete • Risk ${riskValue}/10 • ${riskLevel}`
        );

        console.log("CyberCore analysis result:", lastAnalysis);

    } catch (error) {
        showToast(`Analysis error: ${error.message}`);
        console.error(error);
    } finally {
        analysisBtn.disabled = false;
    }
});

async function refreshCaseOverview() {
    if (!currentCaseId) return;

    const [findingsResp, briefResp, graphResp] = await Promise.all([
        fetch(`${API_BASE}/cases/${currentCaseId}/findings`),
        fetch(`${API_BASE}/cases/${currentCaseId}/brief`),
        fetch(`${API_BASE}/cases/${currentCaseId}/unified-graph`)
    ]);

    if (!findingsResp.ok) {
        throw new Error(await readApiError(findingsResp));
    }

    const findings = await findingsResp.json();
    const brief = briefResp.ok ? await briefResp.json() : null;
    const graph = graphResp.ok ? await graphResp.json() : null;

    lastAnalysis = {
        case_id: currentCaseId,
        risk_score: findings.risk_score ?? 0,
        risk_level: findings.risk_level ?? "LOW",
        total_transactions: brief?.evidence_summary?.total_transactions ?? 0,
        total_entities: graph?.total_nodes ?? 0,
        total_connections: graph?.total_edges ?? 0,
        findings: findings.findings ?? [],
        case_count: 1
    };

    updateDashboardStats(lastAnalysis);
    return lastAnalysis;
}

function updateDashboardStats(analysis) {
    const totalCases = document.getElementById("totalCasesStat");
    const highRisk = document.getElementById("highRiskStat");
    const connected = document.getElementById("connectedArtifactsStat");
    const entities = document.getElementById("suspiciousEntitiesStat");
    const avg = document.getElementById("avgRiskStat");
    const subtext = document.getElementById("connectedArtifactsSubtext");
    const moduleCases = document.getElementById("moduleCaseCount");
    const moduleEntities = document.getElementById("moduleEntityCount");
    const moduleRisk = document.getElementById("moduleRiskScore");
    const activeCaseRisk = document.getElementById("activeCaseRisk");
    const caseRiskScore = document.getElementById("caseRiskScore");
    const caseRiskProgress = document.getElementById("caseRiskProgress");

    const txCount = analysis.total_transactions ?? 0;
    const entityCount = analysis.total_entities ?? 0;
    const riskScore = analysis.risk_score ?? 0;
    const caseCount = analysis.case_count ?? 1;
    const highRiskCount = analysis.risk_level && ["HIGH", "CRITICAL"].includes(analysis.risk_level) ? 1 : 0;

    if (totalCases) totalCases.textContent = caseCount;
    if (highRisk) highRisk.textContent = highRiskCount;
    if (connected) connected.textContent = txCount;
    if (entities) entities.textContent = entityCount;
    if (avg) avg.textContent = riskScore;
    if (subtext) subtext.textContent = `Across ${caseCount} case${caseCount === 1 ? "" : "s"}`;
    if (moduleCases) moduleCases.textContent = caseCount;
    if (moduleEntities) moduleEntities.textContent = entityCount;
    if (moduleRisk) moduleRisk.textContent = `${riskScore}/10`;
    if (caseRiskScore) caseRiskScore.textContent = riskScore;
    if (caseRiskProgress) caseRiskProgress.style.width = `${Math.max(0, Math.min(10, riskScore)) * 10}%`;
    if (activeCaseRisk) {
        const normalizedLevel = String(analysis.risk_level || "LOW").toLowerCase();
        activeCaseRisk.textContent = `${String(analysis.risk_level || "LOW").toUpperCase()} · ${riskScore}/10`;
        activeCaseRisk.className = `risk-pill ${normalizedLevel === "high" || normalizedLevel === "critical" ? "high-pill" : normalizedLevel === "medium" ? "medium-pill" : "low-pill"}`;
    }
}

/* ================= TOAST ================= */

function showToast(message) {

    const toast =
        document.getElementById("toast");

    const toastText =
        document.getElementById("toastText");

    toastText.textContent = message;

    toast.classList.add("show");


    setTimeout(() => {

        toast.classList.remove("show");

    }, 2800);

}


/* ================= INITIAL LANGUAGE ================= */

applyLanguage("en");
loadRecentCases();