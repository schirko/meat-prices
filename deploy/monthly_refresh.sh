#!/usr/bin/env bash
# Monthly data refresh for the VPS (D29, D31, item 6.5).
# Installed in Milestone 7. Suggested crontab line (runs at 06:00 on the 20th of each month,
# after BLS and USDA have published the previous month's data):
#
#   0 6 20 * * /path/to/meat-prices/deploy/monthly_refresh.sh >> /path/to/meat-prices/refresh.log 2>&1
#
# The refresh only replaces the data if every check passes; otherwise the app keeps
# showing the current data and REFRESH_REPORT.md explains what failed.
set -euo pipefail

cd "$(dirname "$0")/.."
source .venv/bin/activate

echo "=== Refresh started $(date) ==="
python -m src.refresh
pytest -q
echo "=== Refresh finished $(date) ==="
