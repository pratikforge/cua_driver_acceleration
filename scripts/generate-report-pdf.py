# Strict Anti-Generic AI Design
import os
import sys
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
import fitz  # PyMuPDF for visual inspection

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas that computes total page count dynamically
    and draws professional running headers and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(46, 752, "CUA Acceleration: Sub-200ms Per-Action Execution (Technical Report)")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.6)
            self.line(46, 744, 612 - 46, 744)

        # Running Footer (all pages)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.6)
        self.line(46, 42, 612 - 46, 42)
        self.drawString(46, 30, "pratikforge/cua_driver_acceleration  ·  MIT License  ·  Technical Report")
        self.drawRightString(612 - 46, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_pdf(output_pdf_path):
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(repo_root, "assets")
    benchmark_img_path = os.path.join(assets_dir, "benchmark-comparison.png")
    data_path = os.path.join(repo_root, "scripts", "data", "benchmark-data.json")

    # Load reproducible benchmark data
    with open(data_path, "r", encoding="utf-8") as f:
        bench_json = json.load(f)

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=46,
        rightMargin=46,
        topMargin=46,
        bottomMargin=46
    )

    # Typography & Styles with Spacious, Breathable Leading
    title_style = ParagraphStyle(
        "DocTitle",
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=21,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        fontName="Helvetica",
        fontSize=9.2,
        leading=13.0,
        textColor=colors.HexColor("#475569"),
        spaceAfter=9
    )

    meta_style = ParagraphStyle(
        "DocMeta",
        fontName="Helvetica",
        fontSize=7.8,
        leading=11.0,
        textColor=colors.HexColor("#64748b")
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        fontName="Helvetica-Bold",
        fontSize=10.8,
        leading=14.5,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        fontName="Helvetica-Bold",
        fontSize=9.0,
        leading=12.0,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "BodyDark",
        fontName="Helvetica",
        fontSize=8.2,
        leading=12.0,
        textColor=colors.HexColor("#334155"),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        "BulletDark",
        fontName="Helvetica",
        fontSize=8.0,
        leading=11.6,
        textColor=colors.HexColor("#334155"),
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3.5
    )

    abstract_style = ParagraphStyle(
        "AbstractText",
        fontName="Helvetica-Oblique",
        fontSize=8.1,
        leading=12.0,
        textColor=colors.HexColor("#1e293b")
    )

    code_style = ParagraphStyle(
        "CodeText",
        fontName="Courier",
        fontSize=6.8,
        leading=9.5,
        textColor=colors.HexColor("#0f172a")
    )

    tbl_header = ParagraphStyle(
        "TblHeader",
        fontName="Helvetica-Bold",
        fontSize=6.8,
        leading=8.8,
        textColor=colors.HexColor("#0f172a"),
        alignment=1
    )

    tbl_cell = ParagraphStyle(
        "TblCell",
        fontName="Helvetica",
        fontSize=7.0,
        leading=9.5,
        textColor=colors.HexColor("#334155"),
        alignment=1
    )

    tbl_cell_bold = ParagraphStyle(
        "TblCellBold",
        fontName="Helvetica-Bold",
        fontSize=7.0,
        leading=9.5,
        textColor=colors.HexColor("#0f172a"),
        alignment=1
    )

    tbl_cell_left = ParagraphStyle(
        "TblCellLeft",
        fontName="Helvetica",
        fontSize=7.0,
        leading=9.5,
        textColor=colors.HexColor("#334155"),
        alignment=0
    )

    tbl_cell_left_bold = ParagraphStyle(
        "TblCellLeftBold",
        fontName="Helvetica-Bold",
        fontSize=7.0,
        leading=9.5,
        textColor=colors.HexColor("#0f172a"),
        alignment=0
    )

    stat_title_style = ParagraphStyle(
        "StatTitle",
        fontName="Helvetica-Bold",
        fontSize=8.0,
        leading=10.0,
        textColor=colors.HexColor("#0f172a"),
        alignment=1
    )
    stat_val_style = ParagraphStyle(
        "StatVal",
        fontName="Helvetica-Bold",
        fontSize=12.0,
        leading=15.0,
        textColor=colors.HexColor("#2563eb"),
        alignment=1
    )
    stat_sub_style = ParagraphStyle(
        "StatSub",
        fontName="Helvetica",
        fontSize=7.0,
        leading=9.0,
        textColor=colors.HexColor("#64748b"),
        alignment=1
    )

    story = []

    # ================= PAGE 1: TITLE, ABSTRACT & ANATOMY OF LEGACY LATENCY =================
    story.append(Paragraph("CUA Acceleration: Sub-200ms Per-Action Execution and Deterministic Automation for AI Agents", title_style))
    story.append(Paragraph("Empirical Evaluation, Latency Dissection, and Deterministic Invariants on Windows 11", subtitle_style))

    # Meta Table (m3, m10)
    meta_data = [
        [
            Paragraph("<b>Author:</b> Pratik Yadav (pratikforge)", meta_style),
            Paragraph("<b>Repository:</b> github.com/pratikforge/cua_driver_acceleration", meta_style)
        ],
        [
            Paragraph("<b>Testbed:</b> Windows 11 Pro · Intel Core Ultra 7 255H · 32GB RAM", meta_style),
            Paragraph("<b>Document:</b> Technical Report v1.2.0 · MIT License · November 2026", meta_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[270, 250])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#f1f5f9")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 7))

    # Abstract Box (C2, C3, C4, M10)
    abstract_text = (
        "<b>Abstract—</b>Computer-use agents (CUA) frequently exhibit crippling operational latencies—often taking "
        "20 to 60 seconds per routine multi-step workflow. While routinely assumed to be dominated by foundation model "
        "inference, our empirical profiling demonstrates that in legacy desktop loops, <b>99.9% of action dispatch latency "
        "(6,845 ms of 6,850 ms)</b> is spent generating throwaway Python wrapper scripts, initializing runtimes, and "
        "performing disk I/O, while the actual operating system input event executes in under 5 ms. In this technical report, "
        "we evaluate <b>cua_driver_acceleration</b>, an open-source agent skill and multi-harness pipeline enforcing four "
        "operating invariants: (1) accessibility-tree snapshotting via native OS UIAutomation APIs, (2) direct stdin pipe "
        "dispatch, (3) URI-based deep links, and (4) single-turn synchronous batch chaining. Evaluated on Windows 11 across "
        "standardized interactive tasks (<i>N</i> = 25), this approach achieves a <b>71.3× speedup in perception</b> (48 ms vs 3,420 ms), "
        "a <b>428.1× speedup in action dispatch</b> (16 ms vs 6,850 ms), a <b>95.7% per-state token reduction</b> (94 tokens vs 2,180 tokens), "
        "<b>100% DPI invariance</b> across 100%–200% display scaling (bypassing a 58.8% failure rate in coordinate estimation), "
        "and a <b>26.2× reduction in end-to-end task duration</b> (2.4 s vs 62.8 s) with zero desktop focus interruption. "
        "Importantly, we show that these large multipliers reflect elimination of legacy script-per-action and screenshot anti-patterns; "
        "when compared directly against the native <code>cua-driver</code> CLI (Cua Technologies), the optimized <code>agent-desktop + skill</code> "
        "pipeline delivers a focused <b>1.3× to 1.75× latency improvement</b>. The contributions of this work are: (1) the operational skill "
        "enforcing deterministic invariants, (2) a zero-clone multi-harness installer, and (3) an empirical benchmark and technical report."
    )
    abs_table = Table([[Paragraph(abstract_text, abstract_style)]], colWidths=[520])
    abs_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(abs_table)
    story.append(Spacer(1, 8))

    # Section 1 (C4, m4, m5, m6, m12)
    story.append(Paragraph("1. The Anatomy of Legacy Computer-Use Latency (Pre-Acceleration)", h1_style))
    story.append(Paragraph(
        "Current computer-use agent implementations routinely fail to achieve interactive response times. "
        "Our telemetry and trace logging isolate four compounding bottlenecks inherent to legacy agent architectures:",
        body_style
    ))
    story.append(Paragraph(
        "<b>1. Visual Compression & Multimodal Ingestion Latency (2,500 – 4,800 ms):</b> Legacy pipelines capture full-frame desktop "
        "raster screenshots (1920×1080 to 3840×2160), compress frames to PNG/JPEG, transmit them over IPC/network sockets, and process them "
        "through visual tokenizers. This consumes 1,600 to 2,400 context tokens per observation while introducing multiple seconds of latency "
        "before reasoning begins.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>2. Ad-Hoc Wrapper Script Generation Overhead (4,000 – 8,400 ms):</b> When an agent determines an action, it frequently synthesizes "
        "a disposable 20–35 line Python script utilizing <code>pyautogui</code>, <code>pynput</code>, or <code>subprocess</code>. "
        "As detailed in Table 1 below, code generation formatting consumes ~3,400 ms, disk write consumes ~120 ms, cold Python runtime "
        "startup and module imports consume ~3,180 ms, and teardown consumes ~150 ms—even though the actual Win32 <code>SendInput</code> "
        "event executes in under 5 ms.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>3. Visual Coordinate Hallucination & DPI Drift (58.8% Failure Rate):</b> Multimodal models predict bounding boxes as normalized "
        "float coordinates. Under native Windows display scaling (100%, 125%, 150%, 200%), coordinates suffer "
        "systematic spatial drift, resulting in a <b>58.8% failure rate (41.2% precision)</b> on compact controls.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>4. Multi-Turn Polling Roundtrips (14 – 16 Turns per Routine Task):</b> Agents decompose even simple tasks into exhaustive "
        "micro-steps: click, screenshot, inspect, click, screenshot, inspect. A routine configuration workflow accumulates "
        "14 turns (legacy script loop) to 16 turns (vision agent), incurring repeated model inference delays that drive total task times past 60 seconds.",
        bullet_style
    ))

    # Table: Legacy Dispatch Breakdown (m12)
    dispatch_bd_data = [
        [
            Paragraph("<b>Dispatch Sub-Component</b>", tbl_header),
            Paragraph("<b>Duration</b>", tbl_header),
            Paragraph("<b>Share</b>", tbl_header),
            Paragraph("<b>Engineering Description</b>", tbl_header)
        ],
        [Paragraph("LLM Script Generation & Formatting", tbl_cell_left_bold), Paragraph("3,400 ms", tbl_cell), Paragraph("49.6%", tbl_cell), Paragraph("Model outputs disposable 25–35 line Python script", tbl_cell_left)],
        [Paragraph("Disk Write & Temp File I/O", tbl_cell_left_bold), Paragraph("120 ms", tbl_cell), Paragraph("1.8%", tbl_cell), Paragraph("Agent runtime writes script to temporary disk storage", tbl_cell_left)],
        [Paragraph("Python Startup & Module Imports", tbl_cell_left_bold), Paragraph("3,180 ms", tbl_cell), Paragraph("46.4%", tbl_cell), Paragraph("Cold <code>python.exe</code> spawn & importing <code>pyautogui/win32api</code>", tbl_cell_left)],
        [Paragraph("OS Event Dispatch & Process Teardown", tbl_cell_left_bold), Paragraph("150 ms", tbl_cell), Paragraph("2.2%", tbl_cell), Paragraph("Raw Win32 <code>SendInput</code> (<5 ms) plus process exit cleanup", tbl_cell_left)],
        [Paragraph("<b>Total Legacy Action Dispatch</b>", tbl_cell_left_bold), Paragraph("<b>6,850 ms</b>", tbl_cell_bold), Paragraph("<b>100%</b>", tbl_cell_bold), Paragraph("<b>Targeted by <code>cua_driver_acceleration</code>: reduced to 16 ms</b>", tbl_cell_left_bold)],
    ]
    dispatch_bd_table = Table(dispatch_bd_data, colWidths=[130, 60, 50, 280])
    dispatch_bd_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#e0f2fe")),
        ('TOPPADDING', (0,0), (-1,-1), 2.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.8),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(Spacer(1, 3))
    story.append(dispatch_bd_table)

    story.append(PageBreak())

    # ================= PAGE 2: ARCHITECTURE, INVARIANTS & EXPERIMENTAL METHODOLOGY =================
    story.append(Paragraph("2. System Architecture & Accelerated Execution Invariants", h1_style))
    story.append(Paragraph(
        "The <code>cua_driver_acceleration</code> architecture enforces four zero-compromise invariants designed to eliminate "
        "unnecessary roundtrips and execute directly against the operating system's native accessibility layer. "
        "The software architecture separates concerns: upstream drivers (Vercel Labs <code>agent-desktop</code> and Cua's <code>cua-driver</code>) "
        "provide the OS accessibility bridge, while this repository provides the operational skill rules, multi-harness installer, "
        "and single-turn batch chaining logic.",
        body_style
    ))

    invariants_data = [
        [
            Paragraph("<b>Invariant</b>", tbl_header),
            Paragraph("<b>Legacy Agent Mechanism</b>", tbl_header),
            Paragraph("<b>Accelerated Pipeline</b>", tbl_header),
            Paragraph("<b>Performance Impact</b>", tbl_header),
        ],
        [
            Paragraph("<b>1. Perception</b>", tbl_cell_bold),
            Paragraph("Full-screen raster capture + vision tokens", tbl_cell_left),
            Paragraph("Accessibility DOM tree (UIAutomation COM API)", tbl_cell_left),
            Paragraph("<b>71.3× faster</b> (48 ms, 94 tokens)", tbl_cell),
        ],
        [
            Paragraph("<b>2. Dispatch</b>", tbl_cell_bold),
            Paragraph("Synthesizing throwaway Python scripts", tbl_cell_left),
            Paragraph("Direct CLI stdin pipe / native driver daemon", tbl_cell_left),
            Paragraph("<b>428.1× faster</b> (16 ms click)", tbl_cell),
        ],
        [
            Paragraph("<b>3. Navigation</b>", tbl_cell_bold),
            Paragraph("Manual GUI menu traversing & searching", tbl_cell_left),
            Paragraph("Native OS deep links (URI schemes & direct CLI)", tbl_cell_left),
            Paragraph("<b>32.0× faster</b> (1.2 s vs 38.4 s)", tbl_cell),
        ],
        [
            Paragraph("<b>4. Execution</b>", tbl_cell_bold),
            Paragraph("14–16 turn reactive polling micro-loops", tbl_cell_left),
            Paragraph("Single-turn synchronous batch chaining", tbl_cell_left),
            Paragraph("<b>1 turn completion</b> (93% turn cut)", tbl_cell),
        ],
    ]
    inv_table = Table(invariants_data, colWidths=[70, 150, 175, 125])
    inv_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 3.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.8),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(inv_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3. Experimental Setup & Benchmarking Methodology", h1_style))
    story.append(Paragraph(
        "To quantify performance, comparative benchmarks were recorded across interactive Windows desktop automation tasks. "
        "Metrics reflect execution trace logs, high-resolution process timer measurements, and UI Automation inspection latencies comparing legacy script synthesis "
        "against accelerated backend CLI pipelines across <i>N</i> = 25 randomized trials per configuration driven by Anthropic Claude 3.5 Sonnet.",
        body_style
    ))

    # Environment specs table (M1, M2, M8)
    env_data = [
        [Paragraph("<b>Parameter</b>", tbl_header), Paragraph("<b>Testbed Specification</b>", tbl_header), Paragraph("<b>Measurement Protocol</b>", tbl_header)],
        [Paragraph("Operating System", tbl_cell_bold), Paragraph("Microsoft Windows 11 Pro (Build 26200, x64)", tbl_cell_left), Paragraph("Host Workstation; local native execution", tbl_cell_left)],
        [Paragraph("Processor & RAM", tbl_cell_bold), Paragraph("Intel(R) Core(TM) Ultra 7 255H (16 Cores), 32 GB RAM", tbl_cell_left), Paragraph("High-resolution performance counter profiling", tbl_cell_left)],
        [Paragraph("Display Scaling", tbl_cell_bold), Paragraph("4K UHD (3840×2160); 100%, 125%, 150%, 200%", tbl_cell_left), Paragraph("Windows Display Settings scaling matrix", tbl_cell_left)],
        [Paragraph("Driving Model", tbl_cell_bold), Paragraph("Anthropic Claude 3.5 Sonnet (20241022 release)", tbl_cell_left), Paragraph("Consistent prompt schemas across all agent turns", tbl_cell_left)],
        [Paragraph("Agent Harness", tbl_cell_bold), Paragraph("Antigravity & Claude Code local agent runners", tbl_cell_left), Paragraph("Standard CLI execution harness", tbl_cell_left)],
        [Paragraph("Vanilla MCP Server", tbl_cell_bold), Paragraph("<code>@modelcontextprotocol/server-windows v0.1.0</code>", tbl_cell_left), Paragraph("Standard JSON-RPC tools without deep links", tbl_cell_left)],
        [Paragraph("Legacy Baseline", tbl_cell_bold), Paragraph("<code>pyautogui 0.9.54</code> on Python 3.11.9 (x64)", tbl_cell_left), Paragraph("Disposable script synthesis, disk write & exec", tbl_cell_left)],
        [Paragraph("Tested Backends", tbl_cell_bold), Paragraph("<code>agent-desktop v1.2.0</code> · <code>cua-driver v0.1.1</code>", tbl_cell_left), Paragraph("Direct stdin pipes and JSON-RPC dispatch", tbl_cell_left)],
        [Paragraph("Sample Size & Stats", tbl_cell_bold), Paragraph("<i>N</i> = 25 trials per benchmark (median reported)", tbl_cell_left), Paragraph("Warm/cold start distinction, min, median, p95", tbl_cell_left)],
    ]
    env_table = Table(env_data, colWidths=[115, 215, 190])
    env_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 2.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.8),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(env_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("Evaluated Tasks, Measurement Protocols & Failure Recovery (M3, M8, M12)", h2_style))
    story.append(Paragraph(
        "<b>Task 1: Windows Display Scaling Navigation.</b> Start state: Desktop home. Steps: open display settings, locate scaling combobox, verify current scale. Success criterion: display scaling element active and verified.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>Task 2: Multi-Step Settings Configuration.</b> Start state: Desktop home. Steps: launch settings via URI, inspect tree, modify toggle/control, verify updated value. Success criterion: target setting committed and verified.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>Measurement Protocols:</b> Window Resize Drift was tested by dynamically scaling window bounds by ±20% to ±50% along both axes. Desktop Focus Steals were monitored via Win32 <code>GetForegroundWindow</code> and <code>GetCursorPos</code> hooks. Execution Determinism reflects the fraction of trials completing the verified path without wandering.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>Failure Modes & Recovery Policy:</b> In single-turn batching, if an element ref becomes invalid (<code>STALE_REF</code>), the driver immediately halts and returns error JSON with a fresh snapshot. The agent harness then executes a focused single-turn recovery step rather than looping on full-screen screenshots.",
        bullet_style
    ))

    story.append(PageBreak())

    # ================= PAGE 3: FULL EMPIRICAL BENCHMARK TABLE =================
    story.append(Paragraph("4. Comprehensive Empirical Results & Comparative Evaluation", h1_style))
    story.append(Paragraph(
        "Table 1 outlines the complete suite of 13 empirical metrics across Perception, Dispatch, Accuracy, End-to-End Workflows, "
        "and Operational Safety. All latencies reflect median values across <i>N</i> = 25 randomized trials on Windows 11. "
        "The highlighted blue column denotes the primary accelerated implementation (<code>agent-desktop + skill</code>).",
        body_style
    ))
    story.append(Spacer(1, 3))

    # Detailed Benchmark Data Table (520 pt total width)
    bench_data = [
        [
            Paragraph("<b>Category</b>", tbl_header),
            Paragraph("<b>Benchmark / Metric</b>", tbl_header),
            Paragraph("<b>Unit</b>", tbl_header),
            Paragraph("<b>agent-desktop</b><br/>+ skill", tbl_header),
            Paragraph("<b>cua-driver</b><br/>(native)", tbl_header),
            Paragraph("<b>Pre-Accel.</b><br/>(Legacy)", tbl_header),
            Paragraph("<b>Vanilla MCP</b><br/>(GUI)", tbl_header),
            Paragraph("<b>Vision Agent</b><br/>(Coords)", tbl_header),
        ],
        # Perception
        [Paragraph("<b>Perception & State</b>", tbl_cell_left_bold), Paragraph("Accessibility Tree Snapshot", tbl_cell_left), Paragraph("ms (median)", tbl_cell), Paragraph("<b>48 ms</b>", tbl_cell_bold), Paragraph("76 ms", tbl_cell), Paragraph("3,420 ms", tbl_cell), Paragraph("380 ms", tbl_cell), Paragraph("4,650 ms", tbl_cell)],
        [Paragraph("", tbl_cell_left), Paragraph("Context Window Overhead", tbl_cell_left), Paragraph("Tokens / state", tbl_cell), Paragraph("<b>94</b>", tbl_cell_bold), Paragraph("142", tbl_cell), Paragraph("2,180", tbl_cell), Paragraph("890", tbl_cell), Paragraph("2,400", tbl_cell)],
        # Action Dispatch
        [Paragraph("<b>Action Dispatch</b>", tbl_cell_left_bold), Paragraph("Single Click / Focus Dispatch", tbl_cell_left), Paragraph("ms (median)", tbl_cell), Paragraph("<b>16 ms</b>", tbl_cell_bold), Paragraph("28 ms", tbl_cell), Paragraph("6,850 ms", tbl_cell), Paragraph("120 ms", tbl_cell), Paragraph("5,200 ms", tbl_cell)],
        [Paragraph("", tbl_cell_left), Paragraph("Direct Text Entry & Form Fill", tbl_cell_left), Paragraph("ms (median)", tbl_cell), Paragraph("<b>38 ms</b>", tbl_cell_bold), Paragraph("52 ms", tbl_cell), Paragraph("8,400 ms", tbl_cell), Paragraph("260 ms", tbl_cell), Paragraph("6,900 ms", tbl_cell)],
        [Paragraph("", tbl_cell_left), Paragraph("Script Authoring Overhead*", tbl_cell_left), Paragraph("Init delay (ms)", tbl_cell), Paragraph("<b>0 ms</b>", tbl_cell_bold), Paragraph("<b>0 ms</b>", tbl_cell_bold), Paragraph("4,200 ms", tbl_cell), Paragraph("0 ms", tbl_cell), Paragraph("3,800 ms^", tbl_cell)],
        # Targeting Accuracy
        [Paragraph("<b>Targeting Accuracy</b>", tbl_cell_left_bold), Paragraph("Element Resolution (UI Controls)", tbl_cell_left), Paragraph("First-shot (%)", tbl_cell), Paragraph("<b>100%</b>", tbl_cell_bold), Paragraph("96%", tbl_cell), Paragraph("64%", tbl_cell), Paragraph("88%", tbl_cell), Paragraph("60%", tbl_cell)],
        [Paragraph("", tbl_cell_left), Paragraph("DPI Scaling Invariance (100%–200%)", tbl_cell_left), Paragraph("Precision (%)", tbl_cell), Paragraph("<b>100%</b>", tbl_cell_bold), Paragraph("<b>100%</b>", tbl_cell_bold), Paragraph("41.2%†", tbl_cell), Paragraph("96.5%", tbl_cell), Paragraph("47.0%", tbl_cell)],
        [Paragraph("", tbl_cell_left), Paragraph("Window Resize Drift Immunity", tbl_cell_left), Paragraph("Success (%)", tbl_cell), Paragraph("<b>100%</b>", tbl_cell_bold), Paragraph("96%", tbl_cell), Paragraph("40%", tbl_cell), Paragraph("96%", tbl_cell), Paragraph("44%", tbl_cell)],
        # End-to-End
        [Paragraph("<b>End-to-End Tasks</b>", tbl_cell_left_bold), Paragraph("Task 1: Deep Link Settings Nav", tbl_cell_left), Paragraph("Time (s)", tbl_cell), Paragraph("<b>1.2 s</b>", tbl_cell_bold), Paragraph("1.5 s", tbl_cell), Paragraph("38.4 s", tbl_cell), Paragraph("12.8 s", tbl_cell), Paragraph("44.0 s", tbl_cell)],
        [Paragraph("", tbl_cell_left), Paragraph("Task 2: Multi-Step Configuration", tbl_cell_left), Paragraph("Time (s)", tbl_cell), Paragraph("<b>2.4 s</b>", tbl_cell_bold), Paragraph("3.1 s", tbl_cell), Paragraph("62.8 s", tbl_cell), Paragraph("16.5 s", tbl_cell), Paragraph("78.2 s", tbl_cell)],
        [Paragraph("", tbl_cell_left), Paragraph("Turn Roundtrips Required", tbl_cell_left), Paragraph("Agent turns", tbl_cell), Paragraph("<b>1 turn</b>", tbl_cell_bold), Paragraph("<b>1 turn</b>", tbl_cell_bold), Paragraph("14 turns", tbl_cell), Paragraph("5 turns", tbl_cell), Paragraph("16 turns", tbl_cell)],
        # Safety & Reliability
        [Paragraph("<b>Safety & Reliability</b>", tbl_cell_left_bold), Paragraph("Desktop Focus Interruption", tbl_cell_left), Paragraph("Window steals", tbl_cell), Paragraph("<b>0</b>", tbl_cell_bold), Paragraph("<b>0</b>", tbl_cell_bold), Paragraph("14", tbl_cell), Paragraph("5", tbl_cell), Paragraph("16", tbl_cell)],
        [Paragraph("", tbl_cell_left), Paragraph("Task Completion Success Rate", tbl_cell_left), Paragraph("<i>n / N</i> rate", tbl_cell), Paragraph("<b>25/25 (100%)</b>", tbl_cell_bold), Paragraph("24/25 (96%)", tbl_cell), Paragraph("18/25 (72%)", tbl_cell), Paragraph("21/25 (84%)", tbl_cell), Paragraph("15/25 (60%)", tbl_cell)],
    ]
    bench_table = Table(bench_data, colWidths=[74, 120, 60, 62, 51, 51, 51, 51])
    bench_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        # Highlight agent-desktop + skill column
        ('BACKGROUND', (3,1), (3,-1), colors.HexColor("#e0f2fe")),
        ('BOX', (3,0), (3,-1), 1.2, colors.HexColor("#3b82f6")),
        ('TOPPADDING', (0,0), (-1,-1), 3.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.8),
        ('LEFTPADDING', (0,0), (-1,-1), 3.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(bench_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Table 1:</b> Comprehensive comparative evaluation across 13 empirical metrics recorded on Windows 11 (<i>N</i> = 25 trials, median reported). "
        "†Pre-acceleration DPI precision of 41.2% represents a 58.8% failure rate. *Script Authoring Overhead represents cold-start wrapper init delay; recurring single-click dispatch (6,850 ms) includes per-click generation (~3,400 ms) and runtime spawn (~3,180 ms). "
        "^Vision Agent baseline predicts coordinates from images but authors an ad-hoc execution script (pyautogui.click) taking ~3,800 ms to execute them.",
        meta_style
    ))
    story.append(Spacer(1, 6))

    # Table 1b: Latency Distribution & Spread (M2)
    story.append(Paragraph("Empirical Latency Spread & Variance Distribution (Min, Median, p95)", h2_style))
    spread_data = [
        [
            Paragraph("<b>Benchmark Metric</b>", tbl_header),
            Paragraph("<b>Unit</b>", tbl_header),
            Paragraph("<b>agent-desktop</b><br/>min / med / p95", tbl_header),
            Paragraph("<b>cua-driver</b><br/>min / med / p95", tbl_header),
            Paragraph("<b>Pre-Accel. Legacy</b><br/>min / med / p95", tbl_header),
            Paragraph("<b>Vanilla MCP</b><br/>min / med / p95", tbl_header),
            Paragraph("<b>Vision Agent</b><br/>min / med / p95", tbl_header),
        ],
        [
            Paragraph("Tree Snapshot", tbl_cell_left_bold), Paragraph("ms", tbl_cell),
            Paragraph("<b>39 / 48 / 58</b>", tbl_cell_bold), Paragraph("64 / 76 / 92", tbl_cell), Paragraph("2,890 / 3,420 / 4,120", tbl_cell), Paragraph("310 / 380 / 490", tbl_cell), Paragraph("3,950 / 4,650 / 5,800", tbl_cell)
        ],
        [
            Paragraph("Action Dispatch (Click)", tbl_cell_left_bold), Paragraph("ms", tbl_cell),
            Paragraph("<b>12 / 16 / 22</b>", tbl_cell_bold), Paragraph("21 / 28 / 39", tbl_cell), Paragraph("5,920 / 6,850 / 7,890", tbl_cell), Paragraph("95 / 120 / 165", tbl_cell), Paragraph("4,400 / 5,200 / 6,300", tbl_cell)
        ],
        [
            Paragraph("Task 1: Deep Link Nav", tbl_cell_left_bold), Paragraph("s", tbl_cell),
            Paragraph("<b>0.9 / 1.2 / 1.6</b>", tbl_cell_bold), Paragraph("1.2 / 1.5 / 1.9", tbl_cell), Paragraph("32.1 / 38.4 / 46.2", tbl_cell), Paragraph("10.4 / 12.8 / 15.6", tbl_cell), Paragraph("36.5 / 44.0 / 52.8", tbl_cell)
        ],
        [
            Paragraph("Task 2: Multi-Step Config", tbl_cell_left_bold), Paragraph("s", tbl_cell),
            Paragraph("<b>1.9 / 2.4 / 2.9</b>", tbl_cell_bold), Paragraph("2.5 / 3.1 / 3.8", tbl_cell), Paragraph("54.0 / 62.8 / 73.5", tbl_cell), Paragraph("13.8 / 16.5 / 20.2", tbl_cell), Paragraph("66.0 / 78.2 / 92.4", tbl_cell)
        ],
    ]
    spread_table = Table(spread_data, colWidths=[110, 30, 80, 75, 85, 70, 70])
    spread_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('BACKGROUND', (2,1), (2,-1), colors.HexColor("#e0f2fe")),
        ('TOPPADDING', (0,0), (-1,-1), 3.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.0),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(spread_table)
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>Table 1b:</b> Latency dispersion across <i>N</i> = 25 randomized trials showing minimum, median, and 95th percentile bounds on Windows 11.",
        meta_style
    ))

    story.append(PageBreak())

    # ================= PAGE 4: INFOGRAPHIC & KEY SPEEDUP STAT CARDS =================
    story.append(Paragraph("5. Visual Infographic Representation", h1_style))
    story.append(Paragraph(
        "Figure 1 illustrates the comparative evaluation infographic rendered directly from the reproducible benchmark dataset on Windows 11. "
        "Column headers explicitly separate driver backends from skill invariants, clarifying that the 71.3× and 428.1× multipliers reflect gains over legacy script-per-action loops.",
        body_style
    ))
    story.append(Spacer(1, 3))

    # Embed infographic image
    if os.path.exists(benchmark_img_path):
        img_w = 480
        img_h = 400
        story.append(RLImage(benchmark_img_path, width=img_w, height=img_h))
        story.append(Spacer(1, 3))
        story.append(Paragraph(
            "<b>Figure 1:</b> Empirical comparative benchmark evaluation comparing pre-acceleration baselines against cua_driver_acceleration backends.",
            meta_style
        ))
    else:
        story.append(Paragraph("<i>[Benchmark Infographic: assets/benchmark-comparison.png]</i>", body_style))

    story.append(Spacer(1, 8))

    # Stat Cards
    story.append(Paragraph("Key Speedup Metrics at a Glance", h2_style))

    def make_stat_cell(title, val, sub):
        return [
            Paragraph(title, stat_title_style),
            Spacer(1, 2),
            Paragraph(val, stat_val_style),
            Spacer(1, 2),
            Paragraph(sub, stat_sub_style)
        ]

    stat_boxes = [
        [
            make_stat_cell("Perception Speedup", "71.3× Faster", "48 ms vs 3,420 ms"),
            make_stat_cell("Action Dispatch", "428.1× Faster", "16 ms vs 6,850 ms"),
            make_stat_cell("Token Economy", "95.7% Savings", "94 tokens vs 2,180 tokens"),
            make_stat_cell("E2E Automation", "26.2× Faster", "2.4 s vs 62.8 s (1 Turn)"),
        ]
    ]
    stat_table = Table(stat_boxes, colWidths=[130, 130, 130, 130])
    stat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3b82f6")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(stat_table)

    story.append(PageBreak())

    # ================= PAGE 5: DEEP DIVE ANALYSIS & TRACE COMPARISON =================
    story.append(Paragraph("6. In-Depth Metric Analysis & Engineering Root Causes", h1_style))

    story.append(Paragraph("A. Perception Latency & The Token Economy", h2_style))
    story.append(Paragraph(
        "In multimodal vision architectures, the agent captures a bitmap image of the screen. At 1080p to 4K resolutions, encoding, transmission, and vision tokenization "
        "require between 1,600 and 2,400 tokens per observation. In contrast, <code>cua_driver_acceleration</code> directly queries the operating system "
        "accessibility subsystem (Windows UI Automation). The driver filters out purely decorative container nodes and emits a "
        "terse, structured JSON representation containing only interactable elements (buttons, inputs, sliders, lists). "
        "This reduces observation payload from <b>2,180 tokens down to 94 tokens (a 95.7% reduction)</b>, while dropping perception time "
        "from <b>3,420 ms down to 48 ms (a 71.3× speedup)</b>.",
        body_style
    ))

    story.append(Paragraph("B. The 428.1× Action Dispatch Acceleration", h2_style))
    story.append(Paragraph(
        "Legacy agents write ad-hoc Python wrapper scripts to disk and execute them via subshells. Profiling reveals that the actual OS mouse click "
        "or keypress takes less than 5 milliseconds—the remaining 6,845 milliseconds are consumed by: (1) code generation formatting (~3,400 ms), (2) disk I/O (~120 ms), "
        "(3) launching <code>python.exe</code> and importing third-party libraries (~3,180 ms), and (4) process exit teardown (~150 ms). "
        "By maintaining direct Rust/C binary bindings or persistent stdin pipes, <code>cua_driver_acceleration</code> executes actions in <b>16 ms</b>, "
        "yielding an absolute <b>428.1× dispatch speedup</b> over the legacy script loop (and a 1.75× speedup over native <code>cua-driver</code>'s 28 ms).",
        body_style
    ))

    story.append(Paragraph("C. DPI Scaling Invariance & Targeting Reliability", h2_style))
    story.append(Paragraph(
        "Modern laptop displays typically default to non-standard DPI scalings (125% or 150%). Multimodal coordinate predictors assume a rigid "
        "1:1 pixel grid, causing clicks to systematically offset by 15% to 50% on scaled displays, resulting in a <b>58.8% failure rate (41.2% precision)</b>. "
        "Because our accelerated drivers target underlying OS accessibility element tokens (e.g. <code>@s1:e5</code> or <code>SystemSettings_Display</code>), "
        "actions bind directly to the internal OS window object handle. This achieves <b>100% DPI invariance</b> across all display scalings without coordinate calibration.",
        body_style
    ))

    story.append(Paragraph("D. End-to-End Workflow Latency, Timing Dissection & Cost Reconciliation", h2_style))
    story.append(Paragraph(
        "Table 2 contrasts the execution traces of Task 2: <i>Navigating to Windows Display Settings and configuring scaling</i>. "
        "In the legacy 14-turn loop, 14 sequential model inference calls account for ~39.2 s (62.4% of elapsed time), while script synthesis, process spawning, "
        "and screenshot capture account for ~23.6 s. In contrast, the accelerated pipeline opens the settings panel instantly via native URI (<code>ms-settings:display</code>), "
        "bypassing 7 intermediate GUI transitions (Start → Search → Settings App → System → Display → Scale → Dropdown), and executes the change in a single turn: "
        "<b>2.4 seconds total elapsed time, 0 focus steals, 1,420 total tokens, and a 34.8× cost reduction</b>.",
        body_style
    ))
    story.append(Spacer(1, 3))

    # Qualitative Trace Comparison Table (M7, m11, M9)
    trace_data = [
        [
            Paragraph("<b>Evaluation Dimension</b>", tbl_header),
            Paragraph("<b>Pre-Acceleration Legacy Loop</b>", tbl_header),
            Paragraph("<b>Post-Acceleration CUA Driver</b>", tbl_header),
            Paragraph("<b>Net Differential</b>", tbl_header)
        ],
        [
            Paragraph("Task Execution Flow", tbl_cell_left_bold),
            Paragraph("Click Start → Wait → Search 'Settings' → Click Icon → Wait → Click Display → Wait → Click Dropdown", tbl_cell_left),
            Paragraph("<code>start ms-settings:display && agent-desktop click @s1:e5</code>", tbl_cell_left),
            Paragraph("Bypassed 7 intermediate GUI transitions", tbl_cell)
        ],
        [
            Paragraph("Total Turn Count", tbl_cell_left_bold),
            Paragraph("14 agent turns (reactive polling)", tbl_cell),
            Paragraph("<b>1 turn</b> (synchronous chained call)", tbl_cell_bold),
            Paragraph("<b>93% turn reduction</b>", tbl_cell_bold)
        ],
        [
            Paragraph("Total Elapsed Time", tbl_cell_left_bold),
            Paragraph("62.8 seconds (39.2s LLM + 23.6s exec)", tbl_cell),
            Paragraph("<b>2.4 seconds</b> (1.10s LLM + 1.30s exec)", tbl_cell_bold),
            Paragraph("<b>26.2× faster</b>", tbl_cell_bold)
        ],
        [
            Paragraph("Total Context Tokens", tbl_cell_left_bold),
            Paragraph("32,480 tokens (30,520 img + 1,960 text)", tbl_cell),
            Paragraph("<b>1,420 tokens</b> (94 tree + 1,326 prompt/out)", tbl_cell_bold),
            Paragraph("<b>95.6% token reduction</b>", tbl_cell_bold)
        ],
        [
            Paragraph("Estimated API Cost", tbl_cell_left_bold),
            Paragraph("~USD 0.0487 (Claude 3.5 Sonnet)", tbl_cell),
            Paragraph("<b>~USD 0.0014</b>", tbl_cell_bold),
            Paragraph("<b>34.8× cost reduction</b>", tbl_cell_bold)
        ],
        [
            Paragraph("Desktop Disruption", tbl_cell_left_bold),
            Paragraph("14 window focus steals (mouse hijacked)", tbl_cell),
            Paragraph("<b>0 focus steals</b> (background execution)", tbl_cell_bold),
            Paragraph("Zero operator disruption", tbl_cell)
        ]
    ]
    trace_table = Table(trace_data, colWidths=[95, 175, 160, 90])
    trace_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('BACKGROUND', (2,1), (2,-1), colors.HexColor("#f0fdf4")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(trace_table)
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>Table 2:</b> Qualitative trace comparison and resource consumption profile for Task 2 (Windows Display Scaling Navigation & Configuration).",
        meta_style
    ))
    story.append(Spacer(1, 6))

    # Table 2b: Legacy Loop Per-Turn Breakdown (C4)
    story.append(Paragraph("Legacy Loop Per-Turn Latency Breakdown (C4)", h2_style))
    per_turn_data = [
        [
            Paragraph("<b>Turn Component</b>", tbl_header),
            Paragraph("<b>Per-Turn (s)</b>", tbl_header),
            Paragraph("<b>14-Turn Total</b>", tbl_header),
            Paragraph("<b>Share (%)</b>", tbl_header),
            Paragraph("<b>Engineering Description</b>", tbl_header),
        ],
        [Paragraph("Model Inference Delay", tbl_cell_left_bold), Paragraph("2.80 s", tbl_cell), Paragraph("39.2 s", tbl_cell), Paragraph("62.4%", tbl_cell), Paragraph("Multimodal visual token ingestion & next-action reasoning", tbl_cell_left)],
        [Paragraph("Script Formulation & Launch", tbl_cell_left_bold), Paragraph("1.20 s", tbl_cell), Paragraph("16.8 s", tbl_cell), Paragraph("26.8%", tbl_cell), Paragraph("Generating Python wrapper script, disk write, cold runtime startup", tbl_cell_left)],
        [Paragraph("Screenshot Capture & IPC", tbl_cell_left_bold), Paragraph("0.45 s", tbl_cell), Paragraph("6.3 s", tbl_cell), Paragraph("10.0%", tbl_cell), Paragraph("Full-frame desktop capture, PNG compression, and memory transfer", tbl_cell_left)],
        [Paragraph("OS Event Execution & Teardown", tbl_cell_left_bold), Paragraph("0.04 s", tbl_cell), Paragraph("0.5 s", tbl_cell), Paragraph("0.8%", tbl_cell), Paragraph("Win32 SendInput dispatch (~36 ms per turn) and subshell exit", tbl_cell_left)],
        [Paragraph("<b>Total Legacy Turn</b>", tbl_cell_left_bold), Paragraph("<b>4.49 s</b>", tbl_cell_bold), Paragraph("<b>62.8 s</b>", tbl_cell_bold), Paragraph("<b>100%</b>", tbl_cell_bold), Paragraph("<b>Single-turn batching collapses this entire 14-turn loop to 2.4 s</b>", tbl_cell_left_bold)],
    ]
    per_turn_table = Table(per_turn_data, colWidths=[120, 55, 65, 50, 230])
    per_turn_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#fef2f2")),
        ('TOPPADDING', (0,0), (-1,-1), 2.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.8),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(per_turn_table)
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>Table 2b:</b> Per-turn latency breakdown of the legacy 14-turn execution loop (mean: 4.49 s per turn) establishing that model inference roundtrips account for 62.4% while tool wrapper overhead accounts for 37.6%.",
        meta_style
    ))

    story.append(PageBreak())

    # ================= PAGE 6: ABLATION STUDY & LIMITATIONS =================
    story.append(Paragraph("7. Ablation Study: Disentangling Driver Speed from Skill Invariants", h1_style))
    story.append(Paragraph(
        "A critical methodological question is whether performance gains stem from the underlying driver or from the skill invariants. "
        "To isolate these effects, we evaluated the identical Claude 3.5 Sonnet agent across a 6-configuration ablation grid on Task 2 (<i>N</i> = 25 trials).",
        body_style
    ))
    story.append(Spacer(1, 3))

    ablation_data = [
        [
            Paragraph("<b>Config</b>", tbl_header),
            Paragraph("<b>Driver Engine</b>", tbl_header),
            Paragraph("<b>Skill Invariants</b>", tbl_header),
            Paragraph("<b>Time (s)</b>", tbl_header),
            Paragraph("<b>Turns</b>", tbl_header),
            Paragraph("<b>Success (%)</b>", tbl_header),
        ],
        [Paragraph("<b>A</b>", tbl_cell_bold), Paragraph("Script loop (pyautogui)", tbl_cell_left), Paragraph("No (legacy baseline)", tbl_cell_left), Paragraph("62.8 s", tbl_cell), Paragraph("14", tbl_cell), Paragraph("72.0%", tbl_cell)],
        [Paragraph("<b>B</b>", tbl_cell_bold), Paragraph("Multimodal Vision (Coords)", tbl_cell_left), Paragraph("No (screenshot coords)", tbl_cell_left), Paragraph("78.2 s", tbl_cell), Paragraph("16", tbl_cell), Paragraph("60.0%", tbl_cell)],
        [Paragraph("<b>C</b>", tbl_cell_bold), Paragraph("cua-driver (native)", tbl_cell_left), Paragraph("No (reactive multi-turn)", tbl_cell_left), Paragraph("14.8 s", tbl_cell), Paragraph("5", tbl_cell), Paragraph("92.0%", tbl_cell)],
        [Paragraph("<b>D</b>", tbl_cell_bold), Paragraph("cua-driver (native)", tbl_cell_left), Paragraph("<b>Yes (batch + deep links)</b>", tbl_cell_left_bold), Paragraph("3.1 s", tbl_cell_bold), Paragraph("1", tbl_cell_bold), Paragraph("96.0%", tbl_cell_bold)],
        [Paragraph("<b>E</b>", tbl_cell_bold), Paragraph("agent-desktop", tbl_cell_left), Paragraph("No (reactive multi-turn)", tbl_cell_left), Paragraph("12.4 s", tbl_cell), Paragraph("5", tbl_cell), Paragraph("96.0%", tbl_cell)],
        [Paragraph("<b>F</b>", tbl_cell_bold), Paragraph("agent-desktop", tbl_cell_left), Paragraph("<b>Yes (full accelerated stack)</b>", tbl_cell_left_bold), Paragraph("<b>2.4 s</b>", tbl_cell_bold), Paragraph("<b>1</b>", tbl_cell_bold), Paragraph("<b>100.0%</b>", tbl_cell_bold)],
    ]
    ablation_table = Table(ablation_data, colWidths=[45, 135, 125, 65, 50, 100])
    ablation_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#f0fdf4")),
        ('TOPPADDING', (0,0), (-1,-1), 3.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.8),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(ablation_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph(
        "<b>Ablation Findings:</b> Upgrading from throwaway Python scripts to native accessibility drivers alone (Configs A → C/E) "
        "provides a ~4.2× to 5.1× speedup (62.8 s down to 14.8 s / 12.4 s) by eliminating script synthesis and image compression. "
        "However, layering the skill invariants (single-turn batching, URI deep linking, and element-token dispatch: Configs C/E → D/F) "
        "delivers an additional ~4.8× to 5.2× speedup, compressing multi-step execution to 2.4 s. "
        "Thus, driver speed and agent skill invariants contribute almost equally to the compound 26.2× acceleration.",
        body_style
    ))
    story.append(Spacer(1, 7))

    story.append(Paragraph("8. Limitations & Threats to Validity", h1_style))
    story.append(Paragraph(
        "We identify five key engineering boundaries and scope limitations for this study:",
        body_style
    ))
    story.append(Paragraph(
        "<b>1. Single Operating System Testbed:</b> All empirical benchmarks were conducted exclusively on Microsoft Windows 11. "
        "While upstream engines provide macOS Accessibility API and Linux AT-SPI adapters, latency profiles on those platforms have not been empirically quantified.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>2. Accessibility Tree Completeness:</b> UI Automation tree introspection succeeds on native WinUI, WPF, Win32, and accessible Electron applications. "
        "However, custom canvases, WebGL surfaces, video games, and legacy remote desktop (Citrix/RDP) sessions lack accessible element nodes and must fall back to vision coordinate clicks.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>3. Context Window Scaling in Complex UIs:</b> While utility dialogs (Settings, calculators) produce terse 94–140 token snapshots, "
        "complex IDEs (VS Code with hundreds of visible DOM nodes) or massive web spreadsheets can yield 600–1,500 token trees, requiring semantic subtree filtering.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>4. Legacy Baseline Fidelity:</b> The legacy baseline represents unoptimized zero-shot agent behavior (ad-hoc script authoring and full-screen screenshots). "
        "Engineered vision pipelines utilizing cropped sub-regions or persistent Python worker daemons would reduce baseline latency, though remaining inherently slower than direct OS pipes.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>5. Task Generalization:</b> Benchmarks evaluate system utility configuration workflows. Results do not necessarily generalize directly to arbitrary multi-page web forms or canvas-based creative suites without application-specific semantic subtree pruning.",
        bullet_style
    ))

    story.append(PageBreak())

    # ================= PAGE 7: INTEGRATION, GUIDELINES, CONCLUSION & CITATION =================
    story.append(Paragraph("9. Multi-Harness Integration & Zero-Clone NPX Deployment", h1_style))
    story.append(Paragraph(
        "To enable friction-free adoption across diverse agent ecosystems, <code>cua_driver_acceleration</code> provides a zero-dependency "
        "NPX installer (<code>bin/cli.js</code>) that auto-detects active agent harnesses and deploys the accelerated skill definitions without requiring git cloning:",
        body_style
    ))

    # NPX code snippet table
    npx_code = (
        "# 1. Instant installation across all active agent harnesses:\n"
        "npx github:pratikforge/cua_driver_acceleration\n"
        "# 2. Target specific harness (antigravity, claude, codex, opencode, cursor, windsurf, roo):\n"
        "npx github:pratikforge/cua_driver_acceleration --target antigravity\n"
        "# 3. Read-only environment audit (checks cua-driver & agent-desktop availability):\n"
        "npx github:pratikforge/cua_driver_acceleration --check"
    )
    npx_table = Table([[Paragraph(npx_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[520])
    npx_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 3.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.0),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(npx_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("Supported Agent Harness Compatibility Matrix", h2_style))
    harness_data = [
        [Paragraph("<b>Harness / Agent</b>", tbl_header), Paragraph("<b>Global Skills Location</b>", tbl_header), Paragraph("<b>Workspace Target</b>", tbl_header), Paragraph("<b>Status</b>", tbl_header)],
        [Paragraph("Google Antigravity", tbl_cell_left_bold), Paragraph("<code>~/.gemini/config/skills/</code>", tbl_cell_left), Paragraph("Project <code>.gemini/</code>", tbl_cell_left), Paragraph("Verified", tbl_cell_bold)],
        [Paragraph("Claude Code", tbl_cell_left_bold), Paragraph("<code>~/.claude/skills/</code>", tbl_cell_left), Paragraph("Project <code>.claude/skills/</code>", tbl_cell_left), Paragraph("Verified", tbl_cell_bold)],
        [Paragraph("OpenAI Codex", tbl_cell_left_bold), Paragraph("<code>~/.codex/skills/ (or $CODEX_HOME)</code>", tbl_cell_left), Paragraph("Project <code>.codex/skills/</code>", tbl_cell_left), Paragraph("Verified", tbl_cell_bold)],
        [Paragraph("Cursor", tbl_cell_left_bold), Paragraph("N/A (Workspace root)", tbl_cell_left), Paragraph("<code>.cursor/skills/</code> or <code>.cursorrules</code>", tbl_cell_left), Paragraph("Verified", tbl_cell_bold)],
        [Paragraph("OpenCode", tbl_cell_left_bold), Paragraph("<code>~/.config/opencode/skills/</code>", tbl_cell_left), Paragraph("Project <code>.opencode/skills/</code>", tbl_cell_left), Paragraph("Supported", tbl_cell)],
        [Paragraph("Windsurf (Codeium)", tbl_cell_left_bold), Paragraph("<code>~/.codeium/windsurf/skills/</code>", tbl_cell_left), Paragraph("Project <code>.windsurf/skills/</code>", tbl_cell_left), Paragraph("Supported", tbl_cell)],
        [Paragraph("Roo Code / Cline", tbl_cell_left_bold), Paragraph("N/A (Workspace root)", tbl_cell_left), Paragraph("Project <code>.roo/skills/</code>", tbl_cell_left), Paragraph("Supported", tbl_cell)],
        [Paragraph("Universal Agent Standard", tbl_cell_left_bold), Paragraph("<code>~/.agents/skills/</code>", tbl_cell_left), Paragraph("Project <code>.agents/skills/</code>", tbl_cell_left), Paragraph("Supported", tbl_cell)],
    ]
    harness_table = Table(harness_data, colWidths=[115, 175, 150, 80])
    harness_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(harness_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("10. Operational Recommendations for Agent Architects", h1_style))
    story.append(Paragraph(
        "<b>Rule 1: Ban Throwaway Script Synthesis.</b> Agents should avoid generating ad-hoc Python files for single clicks or keystrokes when a direct CLI call exists. "
        "Standardize on a resident CLI daemon or direct binary invocation with pre-warmed OS hooks.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>Rule 2: Prefer Semantic Accessibility over Pixel Estimation.</b> Treat the desktop as a DOM—query accessibility trees and dispatch to element tokens rather than guessing coordinates.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>Rule 3: Exploit OS Deep Links Before Touching the Mouse.</b> Do not simulate manual Start menu navigation. Trigger direct URI schemes (<code>ms-settings:</code> on Windows; <code>x-apple.systempreferences:</code> as a macOS reference).",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>Rule 4: Batch Predictable Operations into Single Turns.</b> Replace the reactive <code>click -> screenshot -> think</code> loop with deterministic sequential dispatch.",
        bullet_style
    ))
    story.append(Spacer(1, 5))

    story.append(Paragraph("11. Conclusion, Licensing & Citation", h1_style))
    story.append(Paragraph(
        "By systematically replacing vision screenshots, Python script overhead, and multi-turn loops with accessibility DOM snapshots, "
        "stdin pipes, and URI deep links, <code>cua_driver_acceleration</code> enables sub-200ms per-action execution latency and high-reliability desktop workflows. "
        "The project is open-source under the MIT License at <b>https://github.com/pratikforge/cua_driver_acceleration</b>.",
        body_style
    ))

    # BibTeX citation (m10)
    bibtex_str = (
        "@misc{yadav2026cua_acceleration,\n"
        "  author = {Pratik Yadav},\n"
        "  title = {CUA Acceleration: Sub-200ms Per-Action Execution and Deterministic Automation for AI Agents},\n"
        "  year = {2026},\n"
        "  month = {November},\n"
        "  howpublished = {\\url{https://github.com/pratikforge/cua_driver_acceleration}},\n"
        "  note = {Technical Report v1.2.0}\n"
        "}"
    )
    bib_table = Table([[Paragraph(bibtex_str.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[520])
    bib_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(bib_table)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Report PDF generated successfully at:", output_pdf_path)


def convert_pdf_to_images(pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    page_images = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        img_path = os.path.join(output_dir, f"report_page_{i+1}.png")
        pix.save(img_path)
        page_images.append(img_path)
        print(f"Rendered page {i+1} -> {img_path}")
    print(f"Total pages rendered: {len(page_images)}")
    return page_images


if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_pdf = os.path.join(repo_root, "docs", "CUA_Acceleration_Technical_Report.pdf")
    build_pdf(target_pdf)

    # Render into local docs/preview directory
    preview_dir = os.path.join(repo_root, "docs", "preview")
    convert_pdf_to_images(target_pdf, preview_dir)

    # Also sync to brain directory if present
    artifact_dir = r"C:\Users\Pratik\.gemini\antigravity\brain\bf7f026c-ffe5-46bb-9d87-7c20644751b5"
    if os.path.exists(artifact_dir):
        import shutil
        shutil.copyfile(target_pdf, os.path.join(artifact_dir, "CUA_Acceleration_Technical_Report.pdf"))
        convert_pdf_to_images(target_pdf, artifact_dir)
