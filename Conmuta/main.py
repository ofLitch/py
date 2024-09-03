import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np

# Función que lee el audio
def readAudioFile(path):
    x, fs = sf.read(path)
    return x, fs

# A/D
def AtD(x, fs, bits = 16):
    maxLevel = 2**(bits-1); # 32.768 máximo valor
    maxX = np.max(np.abs(x))
    normX = x/maxX
    samplesDigital = np.round( normX * (maxLevel/maxX) )
    return samplesDigital

# D/A
def DtA (x, fs, bits = 16):
    maxLevel = 2**(bits-1)  # 32.768 máximo valor para 16 bits
    normX = x / maxLevel  # Desescalar
    reconstructedX = normX  # La señal ya normalizada
    return reconstructedX

def DtB(x, bits=16):
    binarySamples = []
    for sample in x:
        newB = [np.binary_repr(int(sample[0]), width=bits), np.binary_repr(int(sample[1]), width=bits)]
        binarySamples.append(newB)
    return binarySamples

def BtD(x):
    digitalSamples = []
    for binary in x:
        digitalSamples = [[int(binary[0]) ], [int(binary[1]) ]]
    return digitalSamples

ruta = 'LD.mp3'

x, fs = readAudioFile(ruta)
# A/d
xDigital = AtD(x,fs)

# DtB
xBinary = DtB(xDigital)

# BtD
xReconstructed = BtD(xBinary)


# D/A
xAnalog = DtA(xDigital, fs)

sf.write('LD_reconstructed.wav', xAnalog, fs)
