#include <stdio.h>
#include "libtta.h"

FILE *input_wav_file;
FILE *output_tta_file;

// Callback functions
TTAint32 read_callback(TTA_io_callback *io, TTAuint8 *buffer, TTAuint32 size) {
    return fread(buffer, 1, size, input_wav_file);
}

TTAint32 write_callback(TTA_io_callback *io, TTAuint8 *buffer, TTAuint32 size) {
    return fwrite(buffer, 1, size, output_tta_file);
}

TTAint64 seek_callback(TTA_io_callback *io, TTAint64 offset) {
    if (fseek(output_tta_file, offset, SEEK_SET) < 0)
        return -1;
    return offset;
}

int main() {
    // Open input WAV file & output TTA file
    input_wav_file = fopen("input.wav", "rb");
    output_tta_file = fopen("output.tta", "wb");
    
    if (!input_wav_file || !output_tta_file) {
        printf("Failed to open files\n");
        return 1;
    }

    // Skip RIFF header
    fseek(input_wav_file, 12, SEEK_SET);
    
    // Information from WAV header
    uint32_t sample_rate = 0, data_bytes = 0;
    uint16_t audio_format = 0, num_channels = 0, bit_depth = 0;
    
    // Skip subchunk ID and size (8 bytes)
    fseek(input_wav_file, 8, SEEK_CUR);
    
    // Read format data
    fread(&audio_format, 1, 2, input_wav_file);
    fread(&num_channels, 1, 2, input_wav_file);
    fread(&sample_rate, 1, 4, input_wav_file);
                
    fseek(input_wav_file, 6, SEEK_CUR); // Skip byte rate and block align
                
    fread(&bit_depth, 1, 2, input_wav_file);
    
    // Skip subchunk ID
    fseek(input_wav_file, 4, SEEK_CUR);
    // Read data size
    fread(&data_bytes, 1, 4, input_wav_file);
    
    // Set up I/O callbacks
    TTA_io_callback tta_io;
    tta_io.read = read_callback;
    tta_io.write = write_callback;
    tta_io.seek = seek_callback;
    
    // Initialize encoder
    tta_encoder_new(&tta_io);
    
    // Prepare TTA info
    TTA_info info;
    info.format = TTA_FORMAT_SIMPLE;
    info.nch = num_channels;
    info.bps = bit_depth;
    info.sps = sample_rate;
    info.samples = data_bytes / ((bit_depth / 8) * num_channels);    
    // Initialize encoder with audio info
    tta_encoder_init_set_info(&info, 0);
    
    // Encode the WAV file
    const int BUFFER_SIZE = 8192; //8KB
    TTAuint8 buffer[BUFFER_SIZE];
    int bytes_read;
    
    while ((bytes_read = fread(buffer, 1, BUFFER_SIZE, input_wav_file)) > 0) {
        tta_encoder_process_stream(buffer, bytes_read, NULL);
    }
    
    // Finalize the encoding
    tta_encoder_finalize();
    
    // Clean up
    tta_encoder_done();
    fclose(input_wav_file);
    fclose(output_tta_file);
    
    printf("\nCompressed 'input.wav' to 'output.tta'\n");
    return 0;
}