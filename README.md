# MSc SSE Individual Research Project Submission Details

This markdown document contains the details of the code artifiact submissions made for the MSc research project.

## About
This repository contains the python file that is used to compare the branch paths from the coverage report of the baseline and the enhanced tool. 

# Coverage Comparison Tool

A Python script that compares two Istanbul coverage JSON files and reports differences in branch coverage between baseline and enhanced test runs.

## Purpose

This tool helps you identify which code branches are covered by different test suites by comparing two coverage reports. It's particularly useful for:

- Analyzing the impact of test suite improvements
- Finding branches that are only covered by specific test configurations
- Understanding coverage differences between different test runs

## Usage

```bash
python3 compare_coverage.py
```

The script expects two files in the same directory:
- `coverage-baseline.json` - Your baseline coverage report
- `coverage-enhanced.json` - Your enhanced/improved coverage report

## Requirements

- Python 3.x
- Two Istanbul coverage JSON files in the same directory as the script

## Output

The script generates a detailed report showing:

**✅ Branches covered ONLY by baseline:** Code branches that are covered in the baseline but not in the enhanced version

**💥 Branches covered ONLY by enhanced:** Code branches that are covered in the enhanced version but not in the baseline

For each branch, you'll see:
- File path
- Branch ID and path number
- Exact line and column location

## Example Output

```
================================================================================
✅ Branches covered ONLY by 'coverage-baseline.json':
================================================================================

  📂 File: src/utils/helper.js
    - Branch #2 (path 0) at Line 45, Col 12
    - Branch #5 (path 1) at Line 67, Col 8

================================================================================
💥 Branches covered ONLY by 'coverage-enhanced.json':
================================================================================

  📂 File: src/components/Button.js
    - Branch #1 (path 0) at Line 23, Col 15
```

## Error Handling

The script handles common issues gracefully:
- Missing coverage files
- Corrupted JSON files
- Empty or malformed coverage data

If files are missing or corrupted, the script will display helpful error messages and exit cleanly.
