[data, fs] = audioread('input.wav');  % Replace with your audio filename

%% Plot the waveform in the time domain
figure(1);
subplot(2,1,1);
t = (0:length(data)-1) / fs; % Time vector
plot(t, data);
xlabel('Seconds');
ylabel('Amplitude');
title('Time Domain');

%% Plot the waveform in the frequency domain
subplot(2,1,2);
l = length(data);
NFFT = 2^nextpow2(l);
f = fs/2*linspace(0,1,NFFT/2+1);
xf = abs(fft(data, NFFT));
plot(f, xf(1:NFFT/2+1))
xlabel('Frequency (Hz)');
ylabel('Magnitude');
title('Single-sided Spectrum');

%% Compute and Plot Periodogram Power Spectral Density
figure(2);
subplot(2,1,1);
[psdestx, Fxx] = periodogram(data, rectwin(length(data)), length(data), fs);
plot(Fxx, 10*log10(psdestx));
xlabel('Frequency (Hz)');
ylabel('Power/Frequency (dB/Hz)');
title('Periodogram Power Spectral Density Estimate');
grid on;

%% Compute and Display Welch s PSD
subplot(2,1,2);
h = spectrum.welch; % create welch spectrum object
d = psd(h, data,'Fs', fs);
plot(d);
xlabel('Frequency (Hz)');
ylabel('Power Spectral Density (dB/Hz)');
title('Welch Power Spectral Density Estimate');
grid on;