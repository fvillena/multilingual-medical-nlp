for file in data/processed/de/*.txt; do cat "$file"; done > data/processed/merged/de.merged
for file in data/processed/en/*.txt; do cat "$file"; done > data/processed/merged/en.merged
for file in data/processed/es/*.txt; do cat "$file"; done > data/processed/merged/es.merged