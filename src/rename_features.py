import sys
import os
import glob
import pandas as pd

if len(sys.argv) != 2:
    print("Uso: python rename_features_taxonomy.py <carpeta_exportada>")
    sys.exit(1)

export_dir = sys.argv[1]

# ==============================
# 1. Buscar archivos
# ==============================
table_candidates = glob.glob(os.path.join(export_dir, "*table.tsv"))
taxonomy_candidates = glob.glob(os.path.join(export_dir, "*taxo*.tsv"))

if not table_candidates:
    print("❌ No se encontró ninguna tabla de abundancia (*.tsv) en:", export_dir)
    sys.exit(1)

if not taxonomy_candidates:
    print("❌ No se encontró ningún archivo de taxonomía (*.tsv) en:", export_dir)
    sys.exit(1)

feature_file = table_candidates[0]
taxonomy_file = taxonomy_candidates[0]

print("📂 Usando archivos:")
print(" - Tabla:", feature_file)
print(" - Taxonomía:", taxonomy_file)

# ==============================
# 2. Leer tabla de abundancias
# ==============================
with open(feature_file) as f:
    lines = [line.strip() for line in f if line.strip()]

# header = lines[0].split("\t")
# rows = [line.split("\t") for line in lines[1:]]




# Buscar línea con el header correcto
header_idx = None
for i, line in enumerate(lines):
    if line.strip().startswith("#OTU ID") or line.strip().startswith("Feature ID"):
        header_idx = i
        break

if header_idx is None:
    raise ValueError("No se encontró el header en la tabla (ni #OTU ID ni Feature ID)")

# Procesar header y filas
header = lines[header_idx].strip().split("\t")
rows = [line.strip().split("\t") for line in lines[header_idx+1:] if line.strip() and not line.startswith("#")]
feature_ids = [row[0] for row in rows]









# ==============================
# 3. Leer taxonomía
# ==============================
tax = pd.read_csv(taxonomy_file, sep="\t")

# Diccionario directo
tax_dict = {row["Feature ID"]: row["Taxon"] for _, row in tax.iterrows()}

# Diccionario extendido: cada código separado por "|"
tax_index = {}
for fid, taxon in tax_dict.items():
    for part in fid.split("|"):
        tax_index[part] = (fid, taxon)

# ==============================
# 4. Construir archivo de chequeo
# ==============================
check_rows = []
otu_counter = 1

for fid in feature_ids:
    otu_id = f"OTU_{otu_counter}"
    otu_counter += 1

    if fid in tax_dict:  # match exacto
        check_rows.append([fid, otu_id, fid, tax_dict[fid], "exact"])
    else:
        parts = fid.split("|")
        found = False
        for p in parts:
            if p in tax_index:
                tax_fid, taxon = tax_index[p]
                check_rows.append([fid, otu_id, tax_fid, taxon, "partial"])
                found = True
                break
        if not found:
            check_rows.append([fid, otu_id, "NO_MATCH", "Unassigned", "no_match"])

check_df = pd.DataFrame(
    check_rows, columns=["FeatureID_table", "OTU_ID", "FeatureID_tax", "Taxon", "MatchType"]
)

check_file = os.path.join(export_dir, "feature_taxa_check.tsv")
check_df.to_csv(check_file, sep="\t", index=False)

print(f"📄 Archivo de chequeo generado: {check_file}")

# ==============================
# 5. Usar el check para renombrar
# ==============================
mapping = dict(zip(check_df["FeatureID_table"], check_df["OTU_ID"]))

# ---- Tabla de abundancias renombrada
feature_out = os.path.join(export_dir, "feature-table-renamed.tsv")
with open(feature_out, "w") as fw:
    fw.write("\t".join(header) + "\n")
    for row in rows:
        old_id = row[0]
        new_id = mapping.get(old_id, old_id)
        fw.write(new_id + "\t" + "\t".join(row[1:]) + "\n")

# ---- Taxonomía renombrada
taxonomy_out = os.path.join(export_dir, "taxonomy-renamed.tsv")
tax_out_df = check_df[["OTU_ID", "Taxon"]].rename(columns={"OTU_ID": "Feature ID"})
tax_out_df.to_csv(taxonomy_out, sep="\t", index=False)

print("✅ Archivos generados:")
print(f" - {feature_out}")
print(f" - {taxonomy_out}")
