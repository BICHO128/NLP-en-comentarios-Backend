import random

# Rutas de entrada y salida
input_file  = "data/all_comments.jsonl"
train_file  = "data/train.jsonl"
dev_file    = "data/dev.jsonl"

# Leer y mezclar
with open(input_file, encoding="utf8") as f:
    lines = f.read().splitlines()
random.shuffle(lines)

# Calcular punto de corte (80/20)
split_idx = int(0.8 * len(lines))

# Escribir archivos
with open(train_file, "w", encoding="utf8") as f_train:
    f_train.write("\n".join(lines[:split_idx]))
with open(dev_file, "w", encoding="utf8") as f_dev:
    f_dev.write("\n".join(lines[split_idx:]))

print(f"Total ejemplos: {len(lines)}")
print(f"→ {len(lines[:split_idx])} en train.jsonl")
print(f"→ {len(lines[split_idx:])} en dev.jsonl")
