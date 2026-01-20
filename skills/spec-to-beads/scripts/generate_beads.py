#!/usr/bin/env python3
"""
Generate br commands from a structured bead plan.

Usage:
    python generate_beads.py plan.json > create_beads.sh
    bash create_beads.sh

Input JSON format:
{
    "epic": {
        "title": "Epic title",
        "description": "Epic description",
        "priority": 1
    },
    "beads": [
        {
            "id": "auth-spike",  // local reference id
            "title": "Spike: Auth architecture",
            "type": "spike",
            "priority": 1,
            "description": "Decide JWT vs sessions",
            "acceptance": "ADR document created",
            "labels": ["backend", "architecture"],
            "depends_on": [],  // list of local reference ids
            "assignee": "human:@techlead"
        },
        {
            "id": "users-migration",
            "title": "Create users table migration",
            "type": "task",
            "priority": 1,
            "depends_on": ["auth-spike"],
            "labels": ["backend", "database"]
        }
    ]
}
"""

import json
import sys
import shlex
from typing import Optional


def escape_for_shell(s: str) -> str:
    """Escape a string for safe shell inclusion."""
    return shlex.quote(s)


def generate_create_command(bead: dict) -> str:
    """Generate a br create command for a bead."""
    parts = ["br create", escape_for_shell(bead["title"])]
    
    if "type" in bead:
        parts.append(f"--type {bead['type']}")
    
    if "priority" in bead:
        parts.append(f"--priority {bead['priority']}")
    
    if "description" in bead:
        parts.append(f"--description {escape_for_shell(bead['description'])}")
    
    if "acceptance" in bead:
        parts.append(f"--acceptance {escape_for_shell(bead['acceptance'])}")
    
    if "assignee" in bead:
        parts.append(f"--assignee {escape_for_shell(bead['assignee'])}")
    
    # Output JSON to capture the ID
    parts.append("--json")
    
    return " \\\n  ".join(parts)


def generate_script(plan: dict) -> str:
    """Generate a complete shell script from a bead plan."""
    lines = [
        "#!/bin/bash",
        "# Auto-generated bead creation script",
        "# Review before running!",
        "",
        "set -e  # Exit on error",
        "",
        "# Ensure br is initialized",
        "if [ ! -d .beads ]; then",
        '    echo "Error: br not initialized. Run: br init"',
        "    exit 1",
        "fi",
        "",
        "# Associative array to map local IDs to br IDs",
        "declare -A BEAD_IDS",
        "",
    ]
    
    # Create epic if present
    if "epic" in plan:
        epic = plan["epic"]
        lines.append("# Create epic")
        lines.append(f"EPIC_ID=$({generate_create_command({**epic, 'type': 'epic'})} | jq -r '.id')")
        lines.append('echo "Created epic: $EPIC_ID"')
        lines.append("")
    
    # Create all beads
    lines.append("# Create beads")
    for bead in plan.get("beads", []):
        local_id = bead.get("id", bead["title"].lower().replace(" ", "-")[:20])
        lines.append(f"# {bead['title']}")
        lines.append(f"BEAD_IDS['{local_id}']=$({generate_create_command(bead)} | jq -r '.id')")
        lines.append(f'echo "Created {local_id}: ${{BEAD_IDS[\'{local_id}\']}}"')
        lines.append("")
    
    # Set up dependencies
    deps_needed = False
    for bead in plan.get("beads", []):
        if bead.get("depends_on"):
            deps_needed = True
            break
    
    if deps_needed:
        lines.append("# Set up dependencies")
        for bead in plan.get("beads", []):
            local_id = bead.get("id", bead["title"].lower().replace(" ", "-")[:20])
            for dep_id in bead.get("depends_on", []):
                lines.append(f"br dep add ${{BEAD_IDS['{local_id}']}} ${{BEAD_IDS['{dep_id}']}}")
                lines.append(f'echo "  {local_id} depends on {dep_id}"')
        lines.append("")
    
    # Add labels
    labels_needed = False
    for bead in plan.get("beads", []):
        if bead.get("labels"):
            labels_needed = True
            break
    
    if labels_needed:
        lines.append("# Add labels")
        for bead in plan.get("beads", []):
            local_id = bead.get("id", bead["title"].lower().replace(" ", "-")[:20])
            labels = bead.get("labels", [])
            if labels:
                labels_str = " ".join(labels)
                lines.append(f"br label add ${{BEAD_IDS['{local_id}']}} {labels_str}")
        lines.append("")
    
    # Sync
    lines.append("# Sync to JSONL for git")
    lines.append("br sync --flush-only")
    lines.append("")
    lines.append('echo "Done! Created ${#BEAD_IDS[@]} beads"')
    lines.append("br ready  # Show actionable work")
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_beads.py plan.json", file=sys.stderr)
        print("       Reads from stdin if no file specified", file=sys.stderr)
        sys.exit(1)
    
    if sys.argv[1] == "-":
        plan = json.load(sys.stdin)
    else:
        with open(sys.argv[1]) as f:
            plan = json.load(f)
    
    print(generate_script(plan))


if __name__ == "__main__":
    main()
