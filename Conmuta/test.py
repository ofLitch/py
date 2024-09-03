import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def readAudioFile(path):
    samples, fs = sf.read(path)  # Leer archivo de audio
    print(f"Frecuencia de muestreo: {fs}")
    print(f"Longitud de los datos: {len(samples)}")
    print(samples)

# Ejecutar función con el archivo de audio
readAudioFile('LD.mp3')
