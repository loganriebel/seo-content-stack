"""
JSON-LD Schema Markup Validator for Blog Posts

Validates that a blog post's JSON-LD structured data contains all required
fields for Google's Article rich result. Checks field presence, types, and
format constraints.

Usage:
    python seo_tools/validate_schema.py blog/my-post.html
    python seo_tools/validate_schema.py deploy/blog/my-post.html
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path


REQUIRED_ARTICLE_FIELDS = {
    "@context": {"type": str, "expected": "https://schema.org"},
    "@type": {"type": str, "expected": ["Article", "BlogPosting"]},
    "headline": {"type": str, "max_length": 110},
    "datePublished": {"type": str, "format": "iso8601"},
    "author": {"type": dict, "required_subfields": ["@type", "name"]},
    "publisher": {
        "type": dict,
        "required_subfields": ["@type", "name", "logo"],
    },
    "image": {"type": (str, list, dict)},
    "description": {"type": str},
    "mainEntityOfPage": {"type": (str, dict)},
}

RECOMMENDED_FIELDS = [
    "dateModified",
    "url",
    "wordCount",
    "keywords",
]


def extract_jsonld(html_content: str) -> list[dict]:
    """Extract all JSON-LD blocks from HTML content."""
    pattern = r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>'
    matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)

    results = []
    for match in matches:
        try:
            data = json.loads(match.strip())
            results.append(data)
        except json.JSONDecodeError as e:
            results.append({"_parse_error": str(e), "_raw": match.strip()})

    return results


def is_valid_iso8601(date_str: str) -> bool:
    """Check if a string is a valid ISO 8601 date."""
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S.%fZ",
    ]
    for fmt in formats:
        try:
            datetime.strptime(date_str.replace("+00:00", "Z").rstrip("Z") if "Z" not in fmt else date_str, fmt)
            return True
        except ValueError:
            continue

    # Fallback: try the basic date pattern
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}", date_str))


def is_absolute_url(url: str) -> bool:
    """Check if a URL is absolute (starts with http:// or https://)."""
    return url.startswith("http://") or url.startswith("https://")


def validate_article_schema(schema: dict) -> tuple[list[str], list[str], list[str]]:
    """
    Validate a JSON-LD Article/BlogPosting schema.

    Returns (errors, warnings, passes) — lists of human-readable messages.
    """
    errors = []
    warnings = []
    passes = []

    if "_parse_error" in schema:
        errors.append(f"JSON-LD parse error: {schema['_parse_error']}")
        return errors, warnings, passes

    # Check required fields
    for field, rules in REQUIRED_ARTICLE_FIELDS.items():
        if field not in schema:
            errors.append(f"Missing required field: {field}")
            continue

        value = schema[field]

        # Type check
        expected_type = rules["type"]
        if not isinstance(value, expected_type):
            errors.append(
                f"Field '{field}' has wrong type: expected {expected_type}, got {type(value).__name__}"
            )
            continue

        # Specific value check
        if "expected" in rules:
            expected = rules["expected"]
            if isinstance(expected, list):
                if value not in expected:
                    errors.append(
                        f"Field '{field}' has unexpected value: '{value}' (expected one of {expected})"
                    )
                else:
                    passes.append(f"{field}: '{value}'")
            else:
                if value != expected:
                    errors.append(
                        f"Field '{field}' has unexpected value: '{value}' (expected '{expected}')"
                    )
                else:
                    passes.append(f"{field}: '{value}'")
            continue

        # Max length check
        if "max_length" in rules and isinstance(value, str):
            if len(value) > rules["max_length"]:
                warnings.append(
                    f"Field '{field}' exceeds recommended max length: {len(value)} chars (max {rules['max_length']})"
                )
            else:
                passes.append(f"{field}: {len(value)} chars (within {rules['max_length']} limit)")

        # ISO 8601 format check
        if rules.get("format") == "iso8601" and isinstance(value, str):
            if is_valid_iso8601(value):
                passes.append(f"{field}: '{value}' (valid ISO 8601)")
            else:
                errors.append(
                    f"Field '{field}' is not valid ISO 8601: '{value}'"
                )

        # Required subfields check
        if "required_subfields" in rules and isinstance(value, dict):
            for subfield in rules["required_subfields"]:
                if subfield not in value:
                    errors.append(
                        f"Field '{field}' is missing required subfield: '{subfield}'"
                    )
                else:
                    passes.append(f"{field}.{subfield}: present")

        # For non-string, non-dict fields with no special rules, just note presence
        if field not in [p.split(":")[0] for p in passes] and field not in [
            e.split("'")[1] if "'" in e else "" for e in errors
        ]:
            passes.append(f"{field}: present")

    # Validate image URL is absolute
    if "image" in schema:
        image = schema["image"]
        image_url = None
        if isinstance(image, str):
            image_url = image
        elif isinstance(image, dict) and "url" in image:
            image_url = image["url"]
        elif isinstance(image, list) and len(image) > 0:
            image_url = image[0] if isinstance(image[0], str) else image[0].get("url", "")

        if image_url and not is_absolute_url(image_url):
            warnings.append(
                f"Image URL should be absolute: '{image_url}'"
            )

    # Validate publisher logo
    if "publisher" in schema and isinstance(schema["publisher"], dict):
        publisher = schema["publisher"]
        if "logo" in publisher:
            logo = publisher["logo"]
            if isinstance(logo, dict):
                if "url" not in logo:
                    errors.append("publisher.logo is missing 'url' field")
                elif not is_absolute_url(logo["url"]):
                    warnings.append(f"publisher.logo.url should be absolute: '{logo['url']}'")
                else:
                    passes.append("publisher.logo.url: absolute URL")
            elif isinstance(logo, str):
                if not is_absolute_url(logo):
                    warnings.append(f"publisher.logo should be absolute URL: '{logo}'")
                else:
                    passes.append("publisher.logo: absolute URL")

    # Check recommended fields
    for field in RECOMMENDED_FIELDS:
        if field in schema:
            passes.append(f"{field}: present (recommended)")
        else:
            warnings.append(f"Missing recommended field: {field}")

    return errors, warnings, passes


def validate_file(filepath: str) -> int:
    """Validate JSON-LD in an HTML file. Returns exit code (0 = pass, 1 = fail)."""
    path = Path(filepath)
    if not path.exists():
        print(f"ERROR: File not found: {filepath}")
        return 1

    html_content = path.read_text(encoding="utf-8")
    schemas = extract_jsonld(html_content)

    if not schemas:
        print(f"ERROR: No JSON-LD blocks found in {filepath}")
        return 1

    print(f"Found {len(schemas)} JSON-LD block(s) in {filepath}\n")

    exit_code = 0

    for i, schema in enumerate(schemas):
        schema_type = schema.get("@type", "unknown")
        print(f"--- Block {i + 1}: @type = {schema_type} ---\n")

        if schema_type not in ("Article", "BlogPosting"):
            print(f"  Skipping (not Article/BlogPosting)\n")
            continue

        errors, warnings, passes = validate_article_schema(schema)

        if passes:
            print("  PASS:")
            for msg in passes:
                print(f"    [OK] {msg}")
            print()

        if warnings:
            print("  WARNINGS:")
            for msg in warnings:
                print(f"    [WARN] {msg}")
            print()

        if errors:
            print("  ERRORS:")
            for msg in errors:
                print(f"    [FAIL] {msg}")
            print()
            exit_code = 1

        # Summary
        total = len(errors) + len(warnings) + len(passes)
        print(f"  Summary: {len(passes)} passed, {len(warnings)} warnings, {len(errors)} errors")
        if errors:
            print("  Result: FAIL")
        elif warnings:
            print("  Result: PASS WITH WARNINGS")
        else:
            print("  Result: PASS")
        print()

    return exit_code


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python seo_tools/validate_schema.py <html-file>")
        print("Example: python seo_tools/validate_schema.py blog/my-post.html")
        sys.exit(1)

    sys.exit(validate_file(sys.argv[1]))
