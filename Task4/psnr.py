import numpy as np
from scipy.io import wavfile

def calculate_psnr(original_file, compressed_file):
    sr1, data1 = wavfile.read(original_file)
    sr2, data2 = wavfile.read(compressed_file)
    
    min_len = min(len(data1), len(data2))
    data1 = data1[:min_len].astype(np.float64)
    data2 = data2[:min_len].astype(np.float64)
    
    # Calculate MSE
    mse = np.mean((data1 - data2) ** 2)
    
    if mse == 0:
        return float('inf')
    
    # For 16-bit audio
    max_value = 32767.0
    
    # Apply PSNR formula
    psnr = 20 * np.log10(max_value) - 10 * np.log10(mse)
    
    return psnr

print(f'TTA PSNR: {calculate_psnr("input.wav", "tta_decoded.wav"):.2f} dB')
print(f'MP3 PSNR: {calculate_psnr("input.wav", "mp3_decoded.wav"):.2f} dB')