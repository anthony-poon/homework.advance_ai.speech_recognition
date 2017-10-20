% EXAMPLE Simple demo of the MFCC function usage.
%
%   This script is a step by step walk-through of computation of the
%   mel frequency cepstral coefficients (MFCCs) from a speech signal
%   using the MFCC routine.
%
%   See also MFCC, COMPARE.

%   Author: Kamil Wojcicki, September 2011


    % Clean-up MATLAB's environment
    clear all; close all; clc;  

    
    % Define variables
    Tw = 25;                % analysis frame duration (ms)
    Ts = 10;                % analysis frame shift (ms)
    alpha = 0.97;           % preemphasis coefficient
    M = 20;                 % number of filterbank channels 
    C = 12;                 % number of cepstral coefficients
    L = 22;                 % cepstral sine lifter parameter
    LF = 300;               % lower frequency limit (Hz)
    HF = 3700;              % upper frequency limit (Hz)
    wav_file_array = [
      "s0A",
      "s0B",
      "s1A",
      "s1B",
      "s3A",
      "s3B",
      "s4A",
      "s4B",
      "s5A",
      "s5B",
      "s8A",
      "s8B"
    ];  % input audio filename

for i = 1:length(wav_file_array)
    wav_file = strcat('..\wav\truncated\',wav_file_array(i,:),'.wav');
    % Read speech samples, sampling rate and precision from file
    [ speech, fs, nbits ] = wavread( wav_file );


    % Feature extraction (feature vectors as columns)
    [ MFCCs, FBEs, frames ] = ...
                    mfcc( speech, fs, Tw, Ts, alpha, @hamming, [LF HF], M, C+1, L );


    % Generate data needed for plotting 
    [ Nw, NF ] = size( frames );                % frame length and number of frames
    time_frames = [0:NF-1]*Ts*0.001+0.5*Nw/fs;  % time vector (s) for frames 
    time = [ 0:length(speech)-1 ]/fs;           % time vector (s) for signal samples 
    logFBEs = 20*log10( FBEs );                 % compute log FBEs for plotting
    logFBEs_floor = max(logFBEs(:))-50;         % get logFBE floor 50 dB below max
    logFBEs( logFBEs<logFBEs_floor ) = logFBEs_floor; % limit logFBE dynamic range
    save(strcat('..\extracted_mfcc\',wav_file_array(i,:),'_mfcc.txt'), 'MFCCs','-ascii');
end
% EOF
