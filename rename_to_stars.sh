#!/bin/bash
echo "Renaming TARS to STARS..."

# Text replacements
for file in $(find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.txt" -o -name "*.toml" \) | grep -v ".git" | grep -v "venv"); do
    sed -i '' 's/T\.A\.R\.S/S.T.A.R.S/g' "$file"
    sed -i '' 's/Technical Assistance & Reliability/Site Technical Assistance \&  Reliability/g' "$file"
    sed -i '' 's/TARS CLI/STARS CLI/g' "$file"
    sed -i '' 's/TARS /STARS /g' "$file"
    sed -i '' 's/tars-cli/stars-cli/g' "$file"
    sed -i '' 's/tars_cli/stars_cli/g' "$file"
    sed -i '' 's/from tars/from stars/g' "$file"
    sed -i '' 's/\.tars/.stars/g' "$file"
    sed -i '' 's/TARS_/STARS_/g' "$file"
done

# Rename directory
[ -d "src/tars" ] && mv src/tars src/stars

echo "✅ Done!"
