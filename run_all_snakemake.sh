#!/usr/bin/env bash
set -euo pipefail

CORES=${1:-1}
# go to the directory this script is in
cd "$(dirname "${BASH_SOURCE[0]}")"
# then go up twice to the project root

snakefiles=(
  "src/snakemake/rules/register.smk"
  "src/snakemake/rules/binary_mask.smk"
  "src/snakemake/rules/patch_gen.smk"
)

for sf in "${snakefiles[@]}"; do
  echo "————————————————————————————"
  echo "Running workflow: $sf (using $CORES cores)"
  start=$(date +%s)
  snakemake -s "$sf" --cores "$CORES"
  end=$(date +%s)
  elapsed=$((end - start))
  printf "%s took %dm%ds\n" "$sf" $((elapsed/60)) $((elapsed%60))
done

echo "All done!"
