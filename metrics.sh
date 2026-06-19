#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Configuration
# =============================================================================

REPO="ArthurMillet44/simeis"

API="https://api.github.com/repos/${REPO}"

# =============================================================================
# Fonctions
# =============================================================================

# Récupère toutes les issues
fetch_all_issues() {
  local page=1
  local per_page=100
  local all_issues="[]"

  while true; do
    local response
    response=$(curl -sf \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      "${API}/issues?state=all&per_page=${per_page}&page=${page}" \
    )

    local count
    count=$(echo "$response" | jq 'length')

    [[ "$count" -eq 0 ]] && break

    # Exclue les pull requests
    local issues_only
    issues_only=$(echo "$response" | jq '[.[] | select(.pull_request == null)]')

    all_issues=$(echo "$all_issues $issues_only" | jq -s 'add')

    [[ "$count" -lt "$per_page" ]] && break
    ((page++))
  done

  echo "$all_issues"
}

# Affiche une ligne de séparation
separator() {
  printf '%0.s─' {1..50}
  echo
}

# =============================================================================
# Main
# =============================================================================

echo
echo "GitHub Issues Metrics"
echo "Repo : $REPO"
echo

separator

echo "Récupération des issues"
issues=$(fetch_all_issues)

total=$(echo "$issues" | jq 'length')
total_open=$(echo "$issues" | jq '[.[] | select(.state == "open")] | length')
total_closed=$(echo "$issues" | jq '[.[] | select(.state == "closed")] | length')

echo
separator
printf "  %-30s %s\n" "Total issues"  "$total"
printf "  %-30s %s\n" "Ouvertes"      "$total_open"
printf "  %-30s %s\n" "Fermées"       "$total_closed"
separator

echo
echo "Nombre d'issues par label"
echo
printf "  %-30s %8s %8s %8s\n" "Label" "Total" "Ouvertes" "Fermées"
printf "  %-30s %8s %8s %8s\n" "-----" "-----" "--------" "-------"

# Extrait les différents labels 
echo "$issues" | jq -r '
  [ .[] | { state: .state, labels: [.labels[].name] } ]
  | [ .[] | .labels[] as $label | { label: $label, state: .state } ]
  | group_by(.label)[]
  | {
      label: .[0].label,
      total: length,
      open:  [ .[] | select(.state == "open")   ] | length,
      closed: [ .[] | select(.state == "closed") ] | length
    }
  | [.label, .total, .open, .closed]
  | @tsv
' | sort -t$'\t' -k2 -rn | \
while IFS=$'\t' read -r label total open closed; do
  printf "  %-30s %8s %8s %8s\n" "$label" "$total" "$open" "$closed"
done

echo
separator

# Issues sans aucun label
no_label=$(echo "$issues" | jq '[.[] | select(.labels | length == 0)] | length')
no_label_open=$(echo "$issues" | jq '[.[] | select(.labels | length == 0) | select(.state == "open")] | length')
no_label_closed=$(echo "$issues" | jq '[.[] | select(.labels | length == 0) | select(.state == "closed")] | length')
printf "  %-30s %8s %8s %8s\n" "(sans label)" "$no_label" "$no_label_open" "$no_label_closed"

separator
echo