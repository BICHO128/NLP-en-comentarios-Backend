# C:\PROYECTO DE NLP\BACKEND\nlp_training\train.py

import os
# 1) Oculta las GPUs para que ni PyTorch ni Thinc las vean
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import keyword_matcher        # registra tu factory de matcher
from spacy.cli.train import train
from thinc.util import require_cpu
import torch
torch.cuda.set_per_process_memory_fraction(0.9, device=0)


# 2) Asegura que Thinc use CPU
require_cpu()

if __name__ == "__main__":
    # 3) Llamada limpia sin parámetros de GPU
    train(
        "config.cfg",
        output_path="../models/sentiment"
    )
