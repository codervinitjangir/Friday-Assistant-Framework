
import torch
import sys

print(f"Python: {sys.version}")
try:
    print(f"Torch: {torch.__version__}")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU Name: {torch.cuda.get_device_name(0)}")
    else:
        print("No GPU detected by PyTorch.")
except ImportError:
    print("PyTorch not installed.")

try:
    from faster_whisper import WhisperModel
    print("faster_whisper module found.")
except ImportError:
    print("faster_whisper not installed.")
