import sys
import pandas as pd
from pathlib import Path
import yaml
import re
import unicodedata
from typing import Any, Dict, List, Optional


# Improvement over v5: reads the newly added description column for pages and populates the markdown.

# -------------------------------------------------
# CONFIGURATION
# -------------------------------------------------
DATA_FILE = "assets/web_layout/pages.xlsx"      # master spreadsheet
RESOURCES_DIR = Path("assets/resources")        # YAML submissions from Streamlit app
OUTPUT_DOCS_DIR = Path("pages")                  # final Jekyll pages (nested folders)

OUTPUT_DOCS_DIR.mkdir(exist_ok=True)

# Toggle: show page_id footer at bottom of each generated page
SHOW_PAGE_ID_FOOTER = True

# Default intro text when spreadsheet "description" is empty
DEFAULT_TOPIC_INTRO = "Introductory content for this topic will be added here."



# Marker used inside generated page bodies
INJECTION_MARKER = "<!--INJECT_RESOURCE_LIST_HERE-->"


# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------
def sanitize_name(name: str) -> str:
    """
    Turn a human-readable name into a filesystem-safe, ascii-ish slug.
    Used for reconstructing paths under docs/.
    """
    if not name:
        return ""
    name = str(name).strip()

    # Normalize accents (ä -> a, é -> e, etc.)
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")

    name = name.lower()
    # keep only letters, digits, spaces, underscores, hyphens
    name = re.sub(r"[^\w\s-]", "", name)
    # collapse spaces/hyphens into single underscore
    name = re.sub(r"[\s-]+", "_", name)
    return name


def safe_code(x: Any) -> str:
    """
    Convert codes to 2-digit strings:
    1 -> '01', 0/''/NaN -> '00'.
    """
    if x is None or x == "" or pd.isna(x):
        return "00"
    try:
        return f"{int(x):02d}"
    except (ValueError, TypeError):
        return str(x).zfill(2)


def as_bool(x: Any) -> bool:
    """
    Robust boolean cast for YAML/string values.
    Accepts True, "true", "yes", "y", "1", "on".
    """
    if isinstance(x, bool):
        return x
    if x is None:
        return False
    return str(x).strip().lower() in {"true", "yes", "y", "1", "on"}


def as_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except (ValueError, TypeError):
        return default


def as_list(x: Any) -> List[str]:
    """
    Normalize a YAML field to a list of strings.

    - list -> list of str
    - str  -> [str] if not empty
    - None/"" -> []
    """
    if isinstance(x, list):
        return [str(v).strip() for v in x if str(v).strip()]
    if x is None:
        return []
    s = str(x).strip()
    if not s:
        return []
    return [s]


def slugify(text: str) -> str:
    text = (text or "").strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "resource"

def normalize_nav_title(title: Optional[str]) -> Optional[str]:
    """
    Normalize titles used in parent / grand_parent so they match
    the actual visible titles in your Jekyll site.

    - "00 Welcome" -> "Welcome"
    (you can add more special cases later if needed)
    """
    if not title:
        return title

    t = title.strip()
    if t == "00 Welcome":
        return "Welcome"

    return t

def split_page_id_codes(page_id: str) -> List[str]:
    """
    Extract 2-digit code segments from page_id like '040100_en' -> ['04','01','00'].
    Returns [] if not parseable.
    """
    if not page_id:
        return []
    m = re.match(r"^(\d{6})_", str(page_id).strip())
    if not m:
        return []
    digits = m.group(1)  # e.g. '040100'
    return [digits[i:i+2] for i in range(0, 6, 2)]


def page_prefix_from_page_id(page_id: str) -> str:
    """
    Build deepest available prefix by dropping trailing '00' segments.
    Examples:
      010000_en -> '01'
      010400_en -> '01-04'
      040102_en -> '04-01-02'
    """
    parts = split_page_id_codes(page_id)
    while parts and parts[-1] == "00":
        parts.pop()
    return "-".join(parts) if parts else ""


def strip_leading_code(title: str) -> str:
    """
    Remove leading 'NN ' or 'NN-NN ' code from titles.
    Examples:
      '04 Vadose Physics' -> 'Vadose Physics'
      '01 Soil Properties' -> 'Soil Properties'
    """
    t = (title or "").strip()
    return re.sub(r"^\d{2}(?:-\d{2})*\s+", "", t).strip() or t

# -------------------------------------------------
# IMAGE / COVER HELPERS
# -------------------------------------------------
def pick_cover_figure(figures: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Decide which figure to use as the cover image for a resource.

    Priority:
    1. First figure with 'is_cover: true' (set in CataLogger).
    2. Otherwise, the first figure in the list.
    """
    if not figures:
        return None

    # 1) explicit cover flag from CataLogger
    for fig in figures:
        if fig.get("is_cover"):
            return fig

    # 2) fallback: first figure
    return figures[0]


def infer_figure_url(resource: Dict[str, Any], fig: Dict[str, Any]) -> Optional[str]:
    """
    Build the URL for a specific figure of this resource.
    Uses the same naming convention as the ZIP export.

    /assets/resources/<stem>/<stem>_fig<ID>.<ext>
    """
    base_name = resource.get("_file_stem")
    if not base_name:
        return None

    fig_id = fig.get("id")
    orig = fig.get("original_filename") or ""
    ext = Path(orig).suffix.lower()  # keep original extension

    if not fig_id or not ext:
        return None

    # Use Jekyll's relative_url filter so baseurl is handled correctly
    path = f"/assets/resources/{base_name}/{base_name}_fig{fig_id}{ext}"
    return f'{{{{ "{path}" | relative_url }}}}'



def infer_cover_url(resource: Dict[str, Any]) -> Optional[str]:
    """
    Wrapper around pick_cover_figure + infer_figure_url.
    """
    figures = resource.get("figures") or []
    if not figures:
        return None

    cover_fig = pick_cover_figure(figures)
    if not cover_fig:
        return None

    return infer_figure_url(resource, cover_fig)


def render_html_figure(
    img_url: str,
    alt: str,
    figure_number: int,
    caption_text: Optional[str] = None,
    width_pct: int = 90,
    caption_left_margin_pct: int = 5,
) -> str:
    """
    Render a figure using HTML (for better control in Just-the-Docs),
    following the style your professor used.

    - Centered image with controlled width
    - Caption below, left-aligned with a small left margin
    """
    alt_escaped = (alt or "").replace('"', "&quot;")

    # If no caption provided, still show a generic figure label
    caption_final = caption_text.strip() if caption_text and caption_text.strip() else f"Figure {figure_number}."
    if not caption_final.lower().startswith("figure"):
        caption_final = f"Figure {figure_number}: {caption_final}"
    else:
        # If caller already provided "Figure X: ...", keep it.
        caption_final = caption_final

    return (
        f'<p style="text-align: center;">\n'
        f'  <img src="{img_url}" alt="{alt_escaped}" style="width:{width_pct}%; height:auto;">\n'
        f"</p>\n\n"
        f'<p style="text-align: left; margin-left: {caption_left_margin_pct}%;">\n'
        f"  <em>{caption_final}</em>\n"
        f"</p>\n\n"
    )



# -------------------------------------------------
# RESOURCE LOADING (YAML FROM STREAMLIT APP)
# -------------------------------------------------
def load_all_resources(resources_dir: Path) -> Dict[str, List[Dict[str, Any]]]:
    """
    Load all YAML resource files and group them by the "topic_page_id" (if present)
    or by "topic" (which should match the page title).

    Supports:
    - New CataLogger format (item_id, authors[], fit_for, Streamlit metadata, etc.)
    - Older format with author / author_institute fields.
    """
    resource_data: Dict[str, List[Dict[str, Any]]] = {}

    for yaml_file in resources_dir.rglob("*.yaml"):
        try:
            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading {yaml_file.name}: {e}")
            continue

        # --- Common core fields (with fallbacks) ---
        title = (data.get("title") or yaml_file.stem).strip()
        topic = str(data.get("topic") or "").strip()
        topic_page_id = str(data.get("topic_page_id") or "").strip()  # optional, future use

        # remember where this YAML came from + its figures
        data["_file_stem"] = yaml_file.stem
        data["figures"] = data.get("figures") or []  # list of {id, original_filename, ..., is_cover}

        # Prefer explicit ID-based mapping if available
        if topic_page_id:
            key = topic_page_id
        elif topic:
            key = topic
        else:
            print(
                f"Warning: Resource {yaml_file.name} missing 'topic_page_id' "
                f"and 'topic'. Skipping."
            )
            continue

        # --- Normalize lists/booleans from CataLogger ---
        data["keywords"] = as_list(data.get("keywords"))
        data["fit_for"] = as_list(data.get("fit_for"))

        # references: ensure list of strings
        refs = data.get("references", [])
        if isinstance(refs, list):
            data["references"] = [str(r).strip() for r in refs if str(r).strip()]
        elif refs:
            data["references"] = [str(refs).strip()]
        else:
            data["references"] = []

        # --- Authors normalization ---
        # New format: authors: [ {name, affiliation}, ... ]
        authors = data.get("authors")
        if isinstance(authors, list) and authors:
            normalized_authors = []
            for a in authors:
                if not isinstance(a, dict):
                    continue
                name = (a.get("name") or "").strip()
                aff = (a.get("affiliation") or "").strip()
                if not name:
                    continue
                if not aff:
                    aff = "TO_BE_FILLED_BY_COURSE_MANAGER"
                normalized_authors.append({"name": name, "affiliation": aff})
            data["authors"] = normalized_authors
        else:
            # Fallback: older single-author fields
            author_name = (data.get("author") or "").strip()
            author_inst = (data.get("author_institute") or "").strip()
            if author_name:
                data["authors"] = [{"name": author_name, "affiliation": author_inst or "N/A"}]
            else:
                data["authors"] = []

        # --- item_id / resource_id alignment ---
        item_id = (data.get("item_id") or "").strip()
        if item_id and not item_id.startswith("TO_BE_FILLED_BY_COURSE_MANAGER"):
            resource_id = item_id
        else:
            resource_id = slugify(title)
        data["resource_id"] = resource_id

        # Store under key
        resource_data.setdefault(key, []).append(data)

    return resource_data


# -------------------------------------------------
# RESOURCE → MARKDOWN
# -------------------------------------------------
def format_authors_for_table(authors: List[Dict[str, str]]) -> str:
    """
    Convert list of {name, affiliation} into a single string:
    'Name1 (Aff1); Name2 (Aff2)' or 'N/A' if empty.
    """
    if not authors:
        return "N/A"
    chunks = []
    for a in authors:
        name = (a.get("name") or "").strip()
        aff = (a.get("affiliation") or "").strip()
        if name and aff:
            chunks.append(f"{name} ({aff})")
        elif name:
            chunks.append(name)
    return "; ".join(chunks) if chunks else "N/A"


def format_resource_markdown(resource: Dict[str, Any], item_code: str) -> str:
    """
    Format a single resource block as markdown, compatible with
    the YAML generated by the CataLogger Streamlit app.
    """
    title = resource.get("title", "Untitled Resource")
    resource_type = resource.get("resource_type", "N/A")
    time_required = resource.get("time_required", "N/A")
    date_released = resource.get("date_released", "N/A")
    description_short = resource.get("description_short", "No description provided.")
    url = resource.get("url", "#")

    keywords = as_list(resource.get("keywords"))
    fit_for = as_list(resource.get("fit_for"))
    authors = resource.get("authors", [])
    authors_str = format_authors_for_table(authors)

    figures = resource.get("figures") or []
    cover_fig = pick_cover_figure(figures) if figures else None



    cover_url = infer_cover_url(resource)
    fig_counter = 1

    md = ""

    # --- Header first (H3 so page title stays dominant) ---
    md += f"### {item_code} {title}\n\n"

    # --- Main summary line ---
    # Released: only show if a meaningful value exists
    release_value = str(date_released).strip()
    if release_value and not release_value.upper().startswith("TO_BE_FILLED"):
        release_part = f" | **Released:** {release_value}"
    else:
        release_part = ""

    md += (
        f"**Type:** {resource_type} | "
        f"**Time:** {time_required}"
        f"{release_part}\n\n"
    )

    # --- Then optional cover image (per-resource) ---
    
    if cover_url:
    # Build caption text from YAML if present
        caption_parts: List[str] = []
        if cover_fig:
            fcap = (cover_fig.get("caption") or "").strip()
            ftype = (cover_fig.get("type") or "").strip()
            if fcap:
                caption_parts.append(fcap)
            if ftype:
                caption_parts.append(f"({ftype})")

        caption_text = " ".join(caption_parts) if caption_parts else None

        md += render_html_figure(
            img_url=cover_url,
            alt=title,
            figure_number=fig_counter,
            caption_text=caption_text,
            width_pct=90,
            caption_left_margin_pct=5,
        )

        fig_counter += 1



    md += f"{description_short}\n\n"

    # --- Launch link + main detail table ---
    md += f"[**LAUNCH RESOURCE**]({url})\n\n"
    md += "| Detail | Value |\n"
    md += "| :--- | :--- |\n"
    md += f"| **URL** | [{url}]({url}) |\n"
    md += f"| **Author(s)** | {authors_str} |\n"
    md += f"| **Keywords** | {', '.join(keywords) if keywords else '—'} |\n"
    md += f"| **Fit For** | {', '.join(fit_for) if fit_for else '—'} |\n"
    md += f"| **Prerequisites** | {resource.get('prerequisites', 'None specified.')} |\n"

    refs = resource.get("references", [])
    if refs:
        ref_text = "<br>".join(refs)
        md += f"| **References** | {ref_text} |\n"

    # --- Extra table only for Streamlit apps (CataLogger metadata) ---
    if str(resource_type).lower().startswith("streamlit"):
        multipage_app = as_bool(resource.get("multipage_app", False))
        num_pages = as_int(resource.get("num_pages", 0))

        interactive_plots = as_bool(resource.get("interactive_plots", False))
        num_interactive_plots = as_int(resource.get("num_interactive_plots", 0))

        assessments_included = as_bool(resource.get("assessments_included", False))
        num_assessment_questions = as_int(resource.get("num_assessment_questions", 0))

        videos_included = as_bool(resource.get("videos_included", False))
        num_videos = as_int(resource.get("num_videos", 0))

        # only keep rows where the feature is actually present
        details_rows: List[tuple] = []

        if multipage_app:
            pages_str = str(num_pages) if num_pages > 0 else "unknown"
            details_rows.append(("Multipage app", f"yes – approx. {pages_str} page(s)"))

        if interactive_plots:
            plots_str = (
                str(num_interactive_plots)
                if num_interactive_plots > 0
                else "unknown number of"
            )
            details_rows.append(("Interactive plots", f"{plots_str} interactive plot(s)"))

        if assessments_included:
            q_str = (
                str(num_assessment_questions)
                if num_assessment_questions > 0
                else "unknown number of"
            )
            details_rows.append(("Assessments included", f"{q_str} question(s)"))

        if videos_included:
            v_str = str(num_videos) if num_videos > 0 else "unknown number of"
            details_rows.append(("Videos included", f"{v_str} video(s)"))

        # Only show the section if at least one feature is actually present
        if details_rows:
            md += "\n### Streamlit app details\n\n"
            md += "| Detail | Value |\n"
            md += "| :--- | :--- |\n"
            for label, value in details_rows:
                md += f"| {label} | {value} |\n"

    # --- Images section for remaining figures ---
    other_figs: List[Dict[str, Any]] = []
    if figures:
        if cover_fig is not None and cover_fig.get("id") is not None:
            cover_id = cover_fig.get("id")
            other_figs = [f for f in figures if f.get("id") != cover_id]
        else:
            other_figs = figures

    if other_figs:
        md += "\n### Images\n\n"
        for fig in other_figs:
            url_fig = infer_figure_url(resource, fig)
            if not url_fig:
                continue

            fcap = (fig.get("caption") or "").strip()
            ftype = (fig.get("type") or "").strip()

            caption_parts: List[str] = []
            if fcap:
                caption_parts.append(fcap)
            if ftype:
                caption_parts.append(f"({ftype})")

            caption_text = " ".join(caption_parts) if caption_parts else None
            alt = fcap or f"Image for {title}"

            md += render_html_figure(
                img_url=url_fig,
                alt=alt,
                figure_number=fig_counter,
                caption_text=caption_text,
                width_pct=90,
                caption_left_margin_pct=5,
            )

        fig_counter += 1



    md += "\n---\n\n"
    return md


# -------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------
def main(target_page_ids: Optional[List[str]] = None) -> None:
    # Load full spreadsheet for title/parent lookup
    df_full = pd.read_excel(DATA_FILE, dtype=str).fillna("")
    all_resources = load_all_resources(RESOURCES_DIR)

    title_by_page_id: Dict[str, str] = dict(zip(df_full["page_id"], df_full["title"]))
    parent_by_page_id: Dict[str, str] = dict(zip(df_full["page_id"], df_full["parent_id"]))

    if target_page_ids:
        df = df_full[df_full["page_id"].isin(target_page_ids)].copy()
        print(f"Loaded {len(df)} target rows from {DATA_FILE}")
    else:
        df = df_full
        print(f"Loaded {len(df)} pages from {DATA_FILE}")

    print(f"Loaded {sum(len(v) for v in all_resources.values())} resources.")

    for _, row in df.iterrows():
        page_id = row["page_id"]
        parent_id = row["parent_id"]
        title = row["title"]
        layout = (row.get("layout") or "home") or "home"
        lang_code = (row.get("lang_code") or "en") or "en"
        # Optional descriptive intro text from spreadsheet
        description = (row.get("description") or "").strip()

        # --- Skip generating the root Welcome page ---
        # We already have an index.md with title "Welcome" in the repo.
        # The spreadsheet still uses page_id 000000_en for hierarchy,
        # but we don't want a separate pages/000000_en.md file.
        if page_id == "000000_en":
            print(f"Skipping root Welcome page {page_id} ({title})")
            continue

        # nav_order from display_order
        try:
            nav_order = int(row["display_order"])
        except (ValueError, TypeError):
            print(f"Warning: display_order invalid for {page_id} ({title}). Skipping.")
            continue

        has_children = as_bool(row.get("has_children", ""))

        # --- Jekyll / Just-the-Docs front matter ---
        frontmatter: Dict[str, Any] = {
            "title": title,
            "layout": layout,
            "nav_order": nav_order,
            "has_children": has_children,
        }

        # JTD parent / grand_parent resolved by title from page_id
        if parent_id:
            parent_title = title_by_page_id.get(parent_id)
            if parent_title:
                # normalize for special cases like "00 Welcome" -> "Welcome"
                norm_parent = normalize_nav_title(parent_title)
                frontmatter["parent"] = norm_parent

                # optional grand_parent
                gp_id = parent_by_page_id.get(parent_id, "")
                if gp_id:
                    gp_title = title_by_page_id.get(gp_id)
                    if gp_title:
                        norm_gp = normalize_nav_title(gp_title)
                        frontmatter["grand_parent"] = norm_gp


        fm_text = "---\n" + yaml.safe_dump(frontmatter, sort_keys=False) + "---\n\n"

        # Internal metadata as HTML comments (safe for JTD)
        meta_comments = (
            f"<!-- page_id: {page_id} -->\n"
            f"<!-- parent_id: {parent_id} -->\n"
            f"<!-- lang_code: {lang_code} -->\n\n"
        )

        # Base body (no contents/ tree anymore)
        # --- Build hierarchical headings (H1/H2/H3) ---
        # Root welcome is already skipped above.
        this_parts = split_page_id_codes(page_id)          # ['04','01','00']
        this_prefix = page_prefix_from_page_id(page_id)    # '04-01' or '04-01-02' etc.
        
        # Find top-level category page_id (xx0000_en)
        cat_id = f"{this_parts[0]}0000_{lang_code}" if len(this_parts) >= 1 else ""
        cat_title = title_by_page_id.get(cat_id, title) if cat_id else title
        cat_title_clean = cat_title.strip()
        
        # Current page title without leading 'NN '
        this_title_clean = strip_leading_code(title)
        
        lines: List[str] = []
        
        # Category page itself: only H1
        is_category_page = (len(this_parts) == 3 and this_parts[1] == "00" and this_parts[2] == "00")
        is_subcategory_page = (len(this_parts) == 3 and this_parts[1] != "00" and this_parts[2] == "00")
        is_subsub_page = (len(this_parts) == 3 and this_parts[2] != "00")
        
        if is_category_page:
            lines.append(f"# {cat_title_clean}")
        elif is_subcategory_page:
            # H1 = category, H2 = xx-yy + subcategory title (without its 'yy ')
            lines.append(f"# {cat_title_clean}")
            # this_prefix is 'xx-yy'
            lines.append(f"## {this_prefix} {this_title_clean}")
        elif is_subsub_page:
            # H1 = category
            lines.append(f"# {cat_title_clean}")
        
            # H2 uses parent's (subcategory) title
            sub_id = f"{this_parts[0]}{this_parts[1]}00_{lang_code}"  # xxYY00_en
            sub_title = title_by_page_id.get(sub_id, "")
            sub_title_clean = strip_leading_code(sub_title) if sub_title else ""
            sub_prefix = f"{this_parts[0]}-{this_parts[1]}"
            lines.append(f"## {sub_prefix} {sub_title_clean}".strip())
        
            # H3 = xx-yy-zz + subsub title
            lines.append(f"### {this_prefix} {this_title_clean}")
        else:
            # Fallback: keep something sensible
            lines.append(f"# {title.strip()}")
        
        # Use spreadsheet description if provided; otherwise fallback to placeholder
        intro_text = description if description else DEFAULT_TOPIC_INTRO

        existing_body = (
            "\n".join(lines)
            + "\n\n"
            + f"{intro_text}\n\n"
            + f"{INJECTION_MARKER}\n"
        )



        # 3. Gather resources for this page
        # Prefer page_id-based mapping; fallback to title (= topic)
        resources_for_topic = all_resources.get(page_id, [])
        if not resources_for_topic:
            resources_for_topic = all_resources.get(title, [])

        resources_list_md = "## Interactive Resources\n\n"
        if resources_for_topic:
            # stable order by title
            resources_for_topic = sorted(
                resources_for_topic,
                key=lambda r: str(r.get("title", "")).lower(),
            )
        
            page_prefix = page_prefix_from_page_id(page_id)  # '04', '04-01', '04-01-02', etc.


            # If more than one resource, add a small TOC
            if len(resources_for_topic) > 1:
                resources_list_md += "### Contents\n\n"
                for idx, res in enumerate(resources_for_topic, start=1):
                    r_title = (str(res.get("title") or "").strip()) or "Untitled Resource"
                    item_code = f"{page_prefix}-{idx:03d}" if page_prefix else f"{idx:03d}"
                    anchor = slugify(f"{item_code} {r_title}")
                    resources_list_md += f"* **{item_code}**: [{r_title}](#{anchor})\n"

                resources_list_md += "\n"

            # Then the actual resource blocks
            for idx, res in enumerate(resources_for_topic, start=1):
                item_code = f"{page_prefix}-{idx:03d}" if page_prefix else f"{idx:03d}"
                resources_list_md += format_resource_markdown(res, item_code)

        else:
            resources_list_md += "No resources submitted for this topic yet.\n\n"

        # 4. Inject resource list at marker (or append at the end)
        if INJECTION_MARKER in existing_body:
            before_marker, _, after_marker = existing_body.partition(INJECTION_MARKER)
            final_body = (
                before_marker
                + INJECTION_MARKER
                + "\n\n"
                + resources_list_md
                + after_marker
            )
        else:
            final_body = existing_body + "\n\n" + resources_list_md
            print(f"Note: marker not found for page {page_id}, appended resources at end.")

        # Optional footer showing page_id (for maintainers)
        if SHOW_PAGE_ID_FOOTER:
            final_body += f"\n---\n\n_Page ID: {page_id}_\n"

        # 5. Write final Jekyll page
        # Currently: flat files under docs/; build_output_path() kept for reference
        out_path = OUTPUT_DOCS_DIR / f"{page_id}.md"
        out_path.write_text(fm_text + meta_comments + final_body, encoding="utf-8")
        print(f"✅ Wrote {out_path}")


if __name__ == "__main__":
    main()
