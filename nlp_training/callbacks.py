# nlp_training/callbacks.py
import torch, gc

def clear_memory(nlp):
    """Callback para liberar caché GPU/CPU antes de guardar."""
    gc.collect()
    torch.cuda.empty_cache()
    return nlp
