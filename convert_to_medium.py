#!/usr/bin/env python3
"""
Convert semantic_view_best_practices.html to Medium-ready Markdown.
Uses only standard library - no external dependencies.
"""

import re
from pathlib import Path


def extract_text_between_tags(html, start_tag, end_tag, include_tags=False):
    """Extract text between HTML tags."""
    pattern = f'{start_tag}(.*?){end_tag}'
    matches = re.findall(pattern, html, re.DOTALL)
    return matches


def strip_html_tags(text):
    """Remove HTML tags from text."""
    # Remove tags but keep content
    text = re.sub(r'<[^>]+>', '', text)
    # Clean up HTML entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
    text = text.replace('&#x27;', "'")
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def html_to_markdown(html_file, output_file):
    """Convert HTML presentation to Medium-compatible Markdown."""

    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    markdown = []

    # Title and intro
    markdown.append("# Snowflake Semantic View Best Practices: A Complete Guide\n\n")
    markdown.append("*A comprehensive guide to building accurate, scalable semantic layers for Cortex Analyst and Snowflake Intelligence*\n\n")
    markdown.append("---\n\n")
    markdown.append("Snowflake semantic views are the bridge between your raw data and AI-powered analytics. ")
    markdown.append("They translate natural language questions into accurate SQL queries, enabling self-service analytics ")
    markdown.append("for everyone — no SQL knowledge required.\n\n")
    markdown.append("This guide covers everything from creation to optimization, drawing from ")
    markdown.append("internal best practices, the semantic-view Cortex Code skill, and real-world production experience.\n\n")

    # Extract all sections
    sections = re.findall(r'<!-- SECTION \d+:.*?-->(.*?)(?=<!-- SECTION|\Z)', html_content, re.DOTALL)

    print(f"Found {len(sections)} sections")

    # Table of contents
    markdown.append("## Table of Contents\n\n")
    toc_pattern = r'<h2>(.*?)</h2>'

    for i, section in enumerate(sections, 1):
        title_match = re.search(toc_pattern, section)
        if title_match:
            title = strip_html_tags(title_match.group(1))
            markdown.append(f"{i}. [{title}](#section-{i})\n")

    markdown.append("\n---\n\n")

    # Process each section
    for i, section in enumerate(sections, 1):
        print(f"Processing section {i}...")

        # Section anchor
        markdown.append(f'<a name="section-{i}"></a>\n\n')

        # Section title
        title_match = re.search(r'<h2>(.*?)</h2>', section)
        if title_match:
            title = strip_html_tags(title_match.group(1))
            markdown.append(f"## {title}\n\n")

        # Section image
        img_match = re.search(r'<img class="section-img" src="(.*?)".*?alt="(.*?)"', section)
        if img_match:
            img_src = img_match.group(1)
            img_alt = img_match.group(2)
            markdown.append(f"![{img_alt}]({img_src})\n\n")

        # Extract cards
        cards = re.findall(r'<div class="card">(.*?)</div>\s*(?=<div class="card">|</section>|<div class="section-header">|$)', section, re.DOTALL)

        for card in cards:
            # Card title
            card_title_match = re.search(r'<h3>(.*?)</h3>', card)
            if card_title_match:
                card_title = strip_html_tags(card_title_match.group(1))
                markdown.append(f"### {card_title}\n\n")

            # Process paragraphs
            paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', card, re.DOTALL)
            for p in paragraphs:
                text = strip_html_tags(p)
                if text:
                    # Check for strong/bold
                    text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', text)
                    text = re.sub(r'<b>(.*?)</b>', r'**\1**', text)
                    markdown.append(f"{text}\n\n")

            # Process lists
            ul_matches = re.findall(r'<ul[^>]*>(.*?)</ul>', card, re.DOTALL)
            for ul in ul_matches:
                li_items = re.findall(r'<li[^>]*>(.*?)</li>', ul, re.DOTALL)
                for li in li_items:
                    text = strip_html_tags(li)
                    markdown.append(f"- {text}\n")
                markdown.append("\n")

            # Process code blocks
            code_blocks = re.findall(r'<pre><code[^>]*>(.*?)</code></pre>', card, re.DOTALL)
            for code in code_blocks:
                code_text = code.strip()
                # Unescape HTML entities in code
                code_text = code_text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')

                # Detect language
                lang = ''
                if 'name:' in code_text or 'database:' in code_text or 'description:' in code_text:
                    lang = 'yaml'
                elif 'SELECT' in code_text or 'FROM' in code_text or 'WHERE' in code_text:
                    lang = 'sql'
                elif 'def ' in code_text or 'import ' in code_text:
                    lang = 'python'
                elif code_text.startswith('/'):
                    lang = 'bash'

                markdown.append(f"```{lang}\n{code_text}\n```\n\n")

            # Process info boxes
            info_boxes = re.findall(r'<div class="info-box"[^>]*>(.*?)</div>', card, re.DOTALL)
            for box in info_boxes:
                box_text = strip_html_tags(box)
                markdown.append(f"> ℹ️ **Note**: {box_text}\n\n")

            # Process warning boxes
            warning_boxes = re.findall(r'<div class="warning-box"[^>]*>(.*?)</div>', card, re.DOTALL)
            for box in warning_boxes:
                box_text = strip_html_tags(box)
                markdown.append(f"> ⚠️ **Warning**: {box_text}\n\n")

            # Process error boxes
            error_boxes = re.findall(r'<div class="error-box"[^>]*>(.*?)</div>', card, re.DOTALL)
            for box in error_boxes:
                box_text = strip_html_tags(box)
                markdown.append(f"> ❌ **Critical**: {box_text}\n\n")

            # Process tables
            tables = re.findall(r'<table[^>]*>(.*?)</table>', card, re.DOTALL)
            for table in tables:
                markdown.append(convert_table(table))
                markdown.append("\n")

            # Process grids (do/don't sections)
            grids = re.findall(r'<div class="grid-2"[^>]*>(.*?)</div>\s*(?=<div class="card">|</div>|$)', card, re.DOTALL)
            for grid in grids:
                markdown.append(convert_grid(grid))

            # Process flowcharts
            flows = re.findall(r'<div class="flow"[^>]*>(.*?)</div>', card, re.DOTALL)
            for flow in flows:
                steps = re.findall(r'<div class="flow-step"[^>]*>(.*?)</div>', flow)
                for j, step in enumerate(steps, 1):
                    step_text = strip_html_tags(step)
                    markdown.append(f"{j}. {step_text}\n")
                markdown.append("\n")

        markdown.append("---\n\n")

    # Add footer
    markdown.append("## Want More?\n\n")
    markdown.append("📊 **Interactive version**: Check out the [live presentation]")
    markdown.append("(https://sfc-gh-pmanowiecki.github.io/semantic-view-best-practices/semantic_view_best_practices.html) ")
    markdown.append("with full visual styling and navigation.\n\n")
    markdown.append("💡 **Cortex Code skill**: Use the `semantic-view` skill in Cortex Code CLI ")
    markdown.append("or Snowsight to automate semantic view creation, auditing, and optimization.\n\n")
    markdown.append("🔖 **Tags**: #snowflake #data-engineering #ai\n\n")

    # Write output
    output_content = ''.join(markdown)
    Path(output_file).write_text(output_content, encoding='utf-8')
    print(f"\n✅ Markdown file created: {output_file}")
    print(f"📝 Total sections processed: {len(sections)}")
    print(f"📊 Total size: {len(output_content)} characters")


def convert_table(table_html):
    """Convert HTML table to Markdown."""
    rows = []

    # Extract headers
    thead = re.search(r'<thead[^>]*>(.*?)</thead>', table_html, re.DOTALL)
    if thead:
        headers = re.findall(r'<th[^>]*>(.*?)</th>', thead.group(1))
        if headers:
            header_row = '| ' + ' | '.join([strip_html_tags(h) for h in headers]) + ' |'
            rows.append(header_row)
            rows.append('|' + '|'.join(['---' for _ in headers]) + '|')

    # Extract rows
    tbody = re.search(r'<tbody[^>]*>(.*?)</tbody>', table_html, re.DOTALL)
    if tbody:
        table_rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tbody.group(1), re.DOTALL)
    else:
        table_rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_html, re.DOTALL)

    for tr in table_rows:
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', tr, re.DOTALL)
        if cells:
            row = '| ' + ' | '.join([strip_html_tags(cell) for cell in cells]) + ' |'
            rows.append(row)

    return '\n'.join(rows) + '\n'


def convert_grid(grid_html):
    """Convert grid to sequential do/don't sections."""
    result = []

    # Extract grid items
    items = re.findall(r'<div[^>]*>(.*?)</div>\s*(?=<div>|$)', grid_html, re.DOTALL)

    for item in items:
        # Extract header
        header_match = re.search(r'<h4[^>]*>(.*?)</h4>', item)
        if header_match:
            header_text = strip_html_tags(header_match.group(1))

            if '✅' in header_text or 'DO:' in header_text.upper():
                result.append(f"**✅ DO: {header_text.replace('✅', '').strip()}**\n\n")
            elif '❌' in header_text or "DON'T:" in header_text.upper():
                result.append(f"**❌ DON'T: {header_text.replace('❌', '').strip()}**\n\n")
            else:
                result.append(f"**{header_text}**\n\n")

        # Extract paragraphs
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', item, re.DOTALL)
        for p in paragraphs:
            text = strip_html_tags(p)
            if text:
                result.append(f"{text}\n\n")

        # Extract code
        code_blocks = re.findall(r'<pre><code[^>]*>(.*?)</code></pre>', item, re.DOTALL)
        for code in code_blocks:
            code_text = code.strip().replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            lang = 'yaml' if 'name:' in code_text else 'sql' if 'SELECT' in code_text else ''
            result.append(f"```{lang}\n{code_text}\n```\n\n")

    return ''.join(result)


if __name__ == '__main__':
    html_file = 'semantic_view_best_practices.html'
    output_file = 'semantic_view_best_practices_medium.md'

    print(f"Converting {html_file} to {output_file}...")
    html_to_markdown(html_file, output_file)
    print("✨ Conversion complete!")
