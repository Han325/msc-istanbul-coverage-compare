#!/usr/bin/env python3

import json
import sys

def compare_coverage(file_baseline_path, file_enhanced_path):
    """
    Compares two Istanbul coverage JSON files ('coverage-baseline.json' and 
    'coverage-enhanced.json') and reports the differences in branch coverage.
    """
    try:
        with open(file_baseline_path, 'r') as f:
            report_baseline = json.load(f)
        with open(file_enhanced_path, 'r') as f:
            report_enhanced = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: Cannot find file - {e.filename}", file=sys.stderr)
        print("Please make sure both 'coverage-baseline.json' and 'coverage-enhanced.json' are in the same directory as the script.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in a file. Check if it is corrupted.", file=sys.stderr)
        sys.exit(1)

    only_in_baseline = {}
    only_in_enhanced = {}

    all_files = set(report_baseline.keys()) | set(report_enhanced.keys())

    for file_path in sorted(list(all_files)):
        file_baseline_data = report_baseline.get(file_path, {})
        file_enhanced_data = report_enhanced.get(file_path, {})
        
        branch_map = file_baseline_data.get('branchMap', file_enhanced_data.get('branchMap', {}))
        if not branch_map:
            continue

        branches_baseline = file_baseline_data.get('b', {})
        branches_enhanced = file_enhanced_data.get('b', {})
        
        only_in_baseline[file_path] = []
        only_in_enhanced[file_path] = []

        for branch_id, branch_meta in branch_map.items():
            hits_baseline = branches_baseline.get(branch_id, [])
            hits_enhanced = branches_enhanced.get(branch_id, [])
            
            num_paths = max(len(hits_baseline), len(hits_enhanced))

            for i in range(num_paths):
                was_hit_in_baseline = (hits_baseline[i] > 0) if i < len(hits_baseline) else False
                was_hit_in_enhanced = (hits_enhanced[i] > 0) if i < len(hits_enhanced) else False

                if was_hit_in_baseline and not was_hit_in_enhanced:
                    only_in_baseline[file_path].append({
                        "id": branch_id,
                        "path": i,
                        "loc": branch_meta['locations'][i]
                    })
                elif was_hit_in_enhanced and not was_hit_in_baseline:
                    only_in_enhanced[file_path].append({
                        "id": branch_id,
                        "path": i,
                        "loc": branch_meta['locations'][i]
                    })

    # --- Print the final report ---
    print_report("✅ Branches covered ONLY by 'coverage-baseline.json':", only_in_baseline)
    print_report("💥 Branches covered ONLY by 'coverage-enhanced.json':", only_in_enhanced)


def print_report(title, data):
    """Helper function to print the results in a readable format."""
    print("\n" + "="*80)
    print(title)
    print("="*80)
    
    has_content = False
    for file_path, branches in sorted(data.items()):
        if branches:
            has_content = True
            print(f"\n  📂 File: {file_path}")
            for b in branches:
                loc = b['loc']
                print(f"    - Branch #{b['id']} (path {b['path']}) at Line {loc['start']['line']}, Col {loc['start']['column']}")
    
    if not has_content:
        print("    (None)")


if __name__ == "__main__":
    # The file names are now hardcoded
    baseline_file = "coverage-baseline.json"
    enhanced_file = "coverage-enhanced.json"
    
    compare_coverage(baseline_file, enhanced_file)