import cupy
import torch
print(cupy.cuda.runtime.getDeviceProperties(0)['name'])
print(cupy.cuda.runtime.getDeviceCount())
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
print(f"PyTorch GPU: {torch.cuda.get_device_name(torch.cuda.current_device())}")
print(f"CuPy GPU: {cupy.cuda.runtime.getDeviceProperties(0)['name']}")

print(" ")
print(f"PyTorch GPU disponible: {torch.cuda.is_available()}")
print(f"Nombre de la GPU en PyTorch: {torch.cuda.get_device_name(0)}")
print(f"Nombre de la GPU en CuPy: {cupy.cuda.runtime.getDeviceProperties(0)['name']}")