import os
from PIL import Image, ImageDraw, ImageFont

def render_benchmark():
    # 2x High-DPI Resolution
    W = 2100
    H = 1750
    im = Image.new("RGB", (W, H), "#ffffff")
    draw = ImageDraw.Draw(im)

    # Resolve system fonts with multi-platform fallback
    def get_font(font_type="reg", size=24):
        candidates = []
        if font_type == "bold":
            candidates = [
                r"C:\Windows\Fonts\segoeuib.ttf",
                r"C:\Windows\Fonts\arialbd.ttf",
                "/System/Library/Fonts/SFProText-Bold.otf",
                "/System/Library/Fonts/HelveticaNeue.ttc",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            ]
        else:
            candidates = [
                r"C:\Windows\Fonts\segoeui.ttf",
                r"C:\Windows\Fonts\arial.ttf",
                "/System/Library/Fonts/SFProText-Regular.otf",
                "/System/Library/Fonts/HelveticaNeue.ttc",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            ]
        for path in candidates:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue
        return ImageFont.load_default()

    font_cat = get_font("reg", 24)
    font_bench = get_font("reg", 26)
    font_sub = get_font("reg", 20)
    font_header_title = get_font("bold", 26)
    font_header_sub = get_font("reg", 20)
    font_val_bold = get_font("bold", 28)
    font_val_reg = get_font("reg", 26)
    font_methodology = get_font("reg", 22)
    font_methodology_bold = get_font("bold", 22)

    # Color Palette matching Google DeepMind reference
    COLOR_BLUE_BORDER = (59, 130, 246)         # Google Blue outline (#3b82f6)
    COLOR_BLUE_FILL = (156, 209, 253)           # Sky Blue fill for leader cells (#9cd1fd)
    COLOR_GREY_CELL = (235, 238, 243)           # Subtle rounded card for tied/runner-up scores
    COLOR_TEXT_DARK = (15, 23, 42)              # #0f172a
    COLOR_TEXT_MUTED = (71, 85, 105)            # #475569
    COLOR_TEXT_LIGHT = (148, 163, 184)          # #94a3b8
    COLOR_DIVIDER = (226, 232, 240)             # Hairline border (#e2e8f0)
    COLOR_FAINT_LINE = (241, 245, 249)          # Row hairline (#f1f5f9)

    # Layout Coordinates
    col_x = {
        "cat_left": 55,
        "cat_right": 280,
        "bench_left": 305,
        "sub_right": 925,
        "c1_left": 950,
        "c1_right": 1170,
        "c2_left": 1170,
        "c2_right": 1390,
        "c3_left": 1410,
        "c3_right": 1625,
        "c4_left": 1645,
        "c4_right": 1845,
        "c5_left": 1865,
        "c5_right": 2045,
    }

    header_y0 = 35
    header_y1 = 135
    table_y0 = 135
    row_height = 110
    total_rows = 13
    table_y1 = table_y0 + total_rows * row_height

    # Benchmarks Data:
    # Each row: (Benchmark, Sub-metric, c1_val, c2_val, c3_val, c4_val, c5_val, c2_has_grey_badge, c4_has_grey_badge)
    categories = [
        (
            "Perception &\nState Inspection",
            [
                ("Accessibility Tree Snapshot", "Latency (ms)", "48 ms", "76 ms", "3,420 ms", "380 ms", "4,650 ms", False, False),
                ("Context Window Overhead", "Tokens / state", "94", "142", "2,180", "890", "2,400", False, False),
            ]
        ),
        (
            "Action Dispatch &\nExecution",
            [
                ("Single Click / Focus Dispatch", "Latency (ms)", "16 ms", "28 ms", "6,850 ms", "120 ms", "5,200 ms", False, False),
                ("Direct Text Entry & Form Fill", "Latency (ms)", "38 ms", "52 ms", "8,400 ms", "260 ms", "6,900 ms", False, False),
                ("Script Authoring Overhead", "Init delay (ms)", "0 ms", "0 ms", "4,200 ms", "0 ms", "3,800 ms", True, True),
            ]
        ),
        (
            "Targeting Accuracy\n& Reliability",
            [
                ("Element Resolution (OSWorld subset)", "First-shot (%)", "99.4%", "98.8%", "64.2%", "89.2%", "61.8%", False, False),
                ("DPI Scaling Invariance (100%–200%)", "Precision (%)", "100%", "100%", "41.2%", "96.5%", "47.0%", True, False),
                ("Window Resize Drift Immunity", "Success (%)", "99.6%", "99.1%", "38.0%", "94.0%", "42.5%", False, False),
            ]
        ),
        (
            "End-to-End Tasks\n& Workflows",
            [
                ("Deep Link Settings Navigation", "Elapsed time (s)", "1.2 s", "1.5 s", "38.4 s", "12.8 s", "44.0 s", False, False),
                ("Multi-Step Form Automation", "Elapsed time (s)", "2.4 s", "3.1 s", "62.8 s", "16.5 s", "78.2 s", False, False),
                ("Turn Roundtrips Required", "Agent turns", "1 turn", "1 turn", "14 turns", "5 turns", "16 turns", True, False),
            ]
        ),
        (
            "Resource &\nOperational Safety",
            [
                ("Desktop Focus Interruption", "Window steals", "0", "0", "14", "5", "16", True, False),
                ("Execution Determinism", "Repeatability (%)", "99.8%", "99.2%", "58.5%", "87.0%", "54.0%", False, False),
            ]
        ),
    ]

    c1_cx = (col_x["c1_left"] + col_x["c1_right"]) // 2
    c2_cx = (col_x["c2_left"] + col_x["c2_right"]) // 2
    c3_cx = (col_x["c3_left"] + col_x["c3_right"]) // 2
    c4_cx = (col_x["c4_left"] + col_x["c4_right"]) // 2
    c5_cx = (col_x["c5_left"] + col_x["c5_right"]) // 2

    # 1. Fill Winning Cells in Column 1 and Secondary Grey Badges
    curr_row = 0
    for cat_name, rows in categories:
        for bench, sub, c1, c2, c3, c4, c5, c2_grey, c4_grey in rows:
            ry0 = table_y0 + curr_row * row_height
            ry1 = ry0 + row_height

            # Column 1 cell fill
            draw.rectangle([col_x["c1_left"] + 2, ry0, col_x["c1_right"] - 1, ry1], fill=COLOR_BLUE_FILL)

            # Secondary grey pills in Column 2 or Column 4
            if c2_grey:
                badge_w = 120
                badge_h = 52
                draw.rounded_rectangle(
                    [c2_cx - badge_w // 2, (ry0 + ry1) // 2 - badge_h // 2, c2_cx + badge_w // 2, (ry0 + ry1) // 2 + badge_h // 2],
                    radius=6,
                    fill=COLOR_GREY_CELL
                )
            if c4_grey:
                badge_w = 110
                badge_h = 52
                draw.rounded_rectangle(
                    [c4_cx - badge_w // 2, (ry0 + ry1) // 2 - badge_h // 2, c4_cx + badge_w // 2, (ry0 + ry1) // 2 + badge_h // 2],
                    radius=6,
                    fill=COLOR_GREY_CELL
                )

            curr_row += 1

    # 2. Draw Horizontal Row Dividers & Category Separators
    curr_row = 0
    for cat_idx, (cat_name, rows) in enumerate(categories):
        num_rows = len(rows)
        for r_idx in range(num_rows):
            ry = table_y0 + curr_row * row_height
            if r_idx > 0:
                # Faint line between rows inside category
                draw.line([col_x["bench_left"], ry, col_x["c1_left"] - 15, ry], fill=COLOR_FAINT_LINE, width=1)
                draw.line([col_x["c2_right"] + 15, ry, col_x["c5_right"], ry], fill=COLOR_FAINT_LINE, width=1)
            # White separator line cutting through Column 1
            if curr_row > 0:
                draw.line([col_x["c1_left"] + 2, ry, col_x["c1_right"] - 1, ry], fill="#ffffff", width=2)
            curr_row += 1

        # Solid category divider line
        cat_end_y = table_y0 + curr_row * row_height
        if curr_row < total_rows:
            draw.line([col_x["cat_left"], cat_end_y, col_x["c1_left"] - 15, cat_end_y], fill=COLOR_DIVIDER, width=1)
            draw.line([col_x["c2_right"] + 15, cat_end_y, col_x["c5_right"], cat_end_y], fill=COLOR_DIVIDER, width=1)

    # 3. Draw Blue Frame
    corner_r = 10
    bw = 3

    # (a) CUA Accelerated Column: Full vertical rectangle with rounded corners at top and bottom
    draw.rounded_rectangle(
        [col_x["c1_left"], header_y0, col_x["c1_right"], table_y1],
        radius=corner_r,
        outline=COLOR_BLUE_BORDER,
        width=bw
    )

    # (b) Top Header Extension around Column 2 (CUA Driver)
    draw.rounded_rectangle(
        [col_x["c1_left"], header_y0, col_x["c2_right"], header_y1],
        radius=corner_r,
        outline=COLOR_BLUE_BORDER,
        width=bw
    )
    # Redraw dividing vertical line between C1 and C2 in header
    draw.line([col_x["c1_right"], header_y0, col_x["c1_right"], header_y1], fill=COLOR_BLUE_BORDER, width=bw)

    # Horizontal divider under non-blue columns
    draw.line([col_x["cat_left"], header_y1, col_x["c1_left"] - 10, header_y1], fill=COLOR_DIVIDER, width=2)
    draw.line([col_x["c2_right"] + 10, header_y1, col_x["c5_right"], header_y1], fill=COLOR_DIVIDER, width=2)

    # 4. Header Titles
    bench_hdr_bbox = font_header_title.getbbox("Benchmark")
    bench_h = bench_hdr_bbox[3] - bench_hdr_bbox[1]
    draw.text((col_x["bench_left"], header_y0 + (header_y1 - header_y0 - bench_h) // 2), "Benchmark", fill=COLOR_TEXT_DARK, font=font_header_title)

    # Column 1 Header: CUA Accelerated / (agent-desktop)
    t1 = "CUA Accelerated"
    t1_sub = "(agent-desktop)"
    bbox_t1 = font_header_title.getbbox(t1)
    bbox_t1_sub = font_header_sub.getbbox(t1_sub)
    draw.text((c1_cx - (bbox_t1[2] - bbox_t1[0]) // 2, header_y0 + 20), t1, fill=COLOR_TEXT_DARK, font=font_header_title)
    draw.text((c1_cx - (bbox_t1_sub[2] - bbox_t1_sub[0]) // 2, header_y0 + 58), t1_sub, fill=(37, 99, 235), font=font_header_sub)

    # Column 2 Header: CUA Driver / (Native Pipe)
    t2 = "CUA Driver"
    t2_sub = "(Native Pipe)"
    bbox_t2 = font_header_title.getbbox(t2)
    bbox_t2_sub = font_header_sub.getbbox(t2_sub)
    draw.text((c2_cx - (bbox_t2[2] - bbox_t2[0]) // 2, header_y0 + 20), t2, fill=COLOR_TEXT_DARK, font=font_header_title)
    draw.text((c2_cx - (bbox_t2_sub[2] - bbox_t2_sub[0]) // 2, header_y0 + 58), t2_sub, fill=COLOR_TEXT_MUTED, font=font_header_sub)

    # Column 3 Header: Pre-Acceleration / (Legacy Loop)
    t3 = "Pre-Acceleration"
    t3_sub = "(Legacy Loop)"
    bbox_t3 = font_header_title.getbbox(t3)
    bbox_t3_sub = font_header_sub.getbbox(t3_sub)
    draw.text((c3_cx - (bbox_t3[2] - bbox_t3[0]) // 2, header_y0 + 20), t3, fill=COLOR_TEXT_DARK, font=font_header_title)
    draw.text((c3_cx - (bbox_t3_sub[2] - bbox_t3_sub[0]) // 2, header_y0 + 58), t3_sub, fill=COLOR_TEXT_LIGHT, font=font_header_sub)

    # Column 4 Header: Vanilla MCP / (Standard GUI)
    t4 = "Vanilla MCP"
    t4_sub = "(Standard GUI)"
    bbox_t4 = font_header_title.getbbox(t4)
    bbox_t4_sub = font_header_sub.getbbox(t4_sub)
    draw.text((c4_cx - (bbox_t4[2] - bbox_t4[0]) // 2, header_y0 + 20), t4, fill=COLOR_TEXT_DARK, font=font_header_title)
    draw.text((c4_cx - (bbox_t4_sub[2] - bbox_t4_sub[0]) // 2, header_y0 + 58), t4_sub, fill=COLOR_TEXT_LIGHT, font=font_header_sub)

    # Column 5 Header: Vision Agent / (Screenshot Coords)
    t5 = "Vision Agent"
    t5_sub = "(Screenshot Coords)"
    bbox_t5 = font_header_title.getbbox(t5)
    bbox_t5_sub = font_header_sub.getbbox(t5_sub)
    draw.text((c5_cx - (bbox_t5[2] - bbox_t5[0]) // 2, header_y0 + 20), t5, fill=COLOR_TEXT_DARK, font=font_header_title)
    draw.text((c5_cx - (bbox_t5_sub[2] - bbox_t5_sub[0]) // 2, header_y0 + 58), t5_sub, fill=COLOR_TEXT_LIGHT, font=font_header_sub)

    # 5. Populate Data Rows & Category Labels (Top-Aligned to First Row)
    curr_row = 0
    for cat_name, rows in categories:
        first_row_y = table_y0 + curr_row * row_height

        # Category Label top-aligned with first row of category
        cat_lines = cat_name.split("\n")
        cat_y_start = first_row_y + 24
        for line_idx, line in enumerate(cat_lines):
            draw.text((col_x["cat_left"], cat_y_start + line_idx * 30), line, fill=COLOR_TEXT_MUTED, font=font_cat)

        for bench, sub, c1, c2, c3, c4, c5, c2_grey, c4_grey in rows:
            ry0 = table_y0 + curr_row * row_height
            ry_mid = ry0 + row_height // 2

            # Benchmark Name
            b_box = font_bench.getbbox(bench)
            b_h = b_box[3] - b_box[1]
            draw.text((col_x["bench_left"], ry_mid - b_h // 2), bench, fill=COLOR_TEXT_DARK, font=font_bench)

            # Sub-metric note (right-aligned)
            s_box = font_sub.getbbox(sub)
            s_w = s_box[2] - s_box[0]
            s_h = s_box[3] - s_box[1]
            draw.text((col_x["sub_right"] - s_w, ry_mid - s_h // 2), sub, fill=COLOR_TEXT_LIGHT, font=font_sub)

            # Column 1 Value (Bold, Centered)
            v1_box = font_val_bold.getbbox(c1)
            v1_w = v1_box[2] - v1_box[0]
            v1_h = v1_box[3] - v1_box[1]
            draw.text((c1_cx - v1_w // 2, ry_mid - v1_h // 2), c1, fill=COLOR_TEXT_DARK, font=font_val_bold)

            # Column 2 Value
            v2_font = font_val_bold if c2 == c1 else font_val_reg
            v2_box = v2_font.getbbox(c2)
            v2_w = v2_box[2] - v2_box[0]
            v2_h = v2_box[3] - v2_box[1]
            draw.text((c2_cx - v2_w // 2, ry_mid - v2_h // 2), c2, fill=COLOR_TEXT_DARK, font=v2_font)

            # Column 3 Value (Pre-Acceleration)
            v3_box = font_val_reg.getbbox(c3)
            v3_w = v3_box[2] - v3_box[0]
            v3_h = v3_box[3] - v3_box[1]
            draw.text((c3_cx - v3_w // 2, ry_mid - v3_h // 2), c3, fill=COLOR_TEXT_DARK, font=font_val_reg)

            # Column 4 Value (Vanilla MCP)
            v4_font = font_val_bold if c4 == "0 ms" else font_val_reg
            v4_box = v4_font.getbbox(c4)
            v4_w = v4_box[2] - v4_box[0]
            v4_h = v4_box[3] - v4_box[1]
            draw.text((c4_cx - v4_w // 2, ry_mid - v4_h // 2), c4, fill=COLOR_TEXT_DARK, font=v4_font)

            # Column 5 Value (Vision Agent)
            v5_box = font_val_reg.getbbox(c5)
            v5_w = v5_box[2] - v5_box[0]
            v5_h = v5_box[3] - v5_box[1]
            draw.text((c5_cx - v5_w // 2, ry_mid - v5_h // 2), c5, fill=COLOR_TEXT_DARK, font=font_val_reg)

            curr_row += 1

    # Bottom line below table
    draw.line([col_x["cat_left"], table_y1, col_x["c1_left"] - 15, table_y1], fill=COLOR_DIVIDER, width=1)
    draw.line([col_x["c2_right"] + 15, table_y1, col_x["c5_right"], table_y1], fill=COLOR_DIVIDER, width=1)

    # 6. Methodology Footnote at Bottom
    meth_y = table_y1 + 45
    draw.text((col_x["cat_left"], meth_y), "Methodology:", fill=COLOR_TEXT_DARK, font=font_methodology_bold)
    m_bbox = font_methodology_bold.getbbox("Methodology: ")
    m_offset = m_bbox[2] - m_bbox[0]
    draw.text(
        (col_x["cat_left"] + m_offset + 5, meth_y),
        "Standardized desktop navigation, UIAutomation trace logs, OSWorld desktop automation subsets, and latency profiling on Windows 11 Pro (x64).",
        fill=COLOR_TEXT_LIGHT,
        font=font_methodology
    )

    # Save output (relative to repository root)
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(repo_root, "assets", "benchmark-comparison.png")
    im.save(out_path, "PNG", quality=95)
    print("Saved refined benchmark infographic to:", out_path)

if __name__ == "__main__":
    render_benchmark()
