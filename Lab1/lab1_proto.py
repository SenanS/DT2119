import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.signal
from lab1_tools import *


# DT2119, Lab1 Feature Extraction

# Function given by the exercise ----------------------------------

def mspec(samples, winlen=400, winshift=200, preempcoeff=0.97, nfft=512, samplingrate=20000):
    """Computes Mel Filterbank features.

    Args:
        samples: array of speech samples with shape (N,)
        winlen: lenght of the analysis window
        winshift: number of samples to shift the analysis window at every time step
        preempcoeff: pre-emphasis coefficient
        nfft: length of the Fast Fourier Transform (power of 2, >= winlen)
        samplingrate: sampling rate of the original signal

    Returns:
        N x nfilters array with mel filterbank features (see trfbank for nfilters)
    """
    """
    frames = enframe(samples, winlen, winshift)
    preemph = preemp(frames, preempcoeff)
    windowed = windowing(preemph)
    spec = powerSpectrum(windowed, nfft)
    return logMelSpectrum(spec, samplingrate)
    """
    return None


def mfcc(samples, winlen=400, winshift=200, preempcoeff=0.97, nfft=512, nceps=13, samplingrate=20000, liftercoeff=22):
    """Computes Mel Frequency Cepstrum Coefficients.

    Args:
        samples: array of speech samples with shape (N,)
        winlen: lenght of the analysis window
        winshift: number of samples to shift the analysis window at every time step
        preempcoeff: pre-emphasis coefficient
        nfft: length of the Fast Fourier Transform (power of 2, >= winlen)
        nceps: number of cepstrum coefficients to compute
        samplingrate: sampling rate of the original signal
        liftercoeff: liftering coefficient used to equalise scale of MFCCs

    Returns:
        N x nceps array with lifetered MFCC coefficients
    """
    """
    mspecs = mspec(samples, winlen, winshift, preempcoeff, nfft, samplingrate)
    ceps = cepstrum(mspecs, nceps)
    return lifter(ceps, liftercoeff)
    """
    return None


# Functions to be implemented ----------------------------------

def enframe(samples, winlen, winshift):
    """
    Slices the input samples into overlapping windows.

    Args:
        winlen: window length in samples.
        winshift: shift of consecutive windows in samples
    Returns:
        numpy array [N x winlen], where N is the number of windows that fit
        in the input signal
    """
    frames = samples[0:winlen].reshape((1, winlen))

    for i in range(winlen-winshift, samples.shape[0] - winlen, winlen-winshift):
        frames = np.vstack((frames, samples[i:i+winlen].reshape((1, winlen))))
    return frames


def compare(frames1, frames2):
    for i in range(frames1.shape[0]):
        for j in range(frames1.shape[1]):
            if frames1[i][j] != frames2[i][j]:
                print("Not the same!")
                return
    
    print("Same!")


def preemp(input, p=0.97):
    """
    Pre-emphasis filter.

    Args:
        input: array of speech frames [N x M] where N is the number of frames and
               M the samples per frame
        p: preemhasis factor (defaults to the value specified in the exercise)

    Output:
        output: array of pre-emphasised speech samples
    Note (you can use the function lfilter from scipy.signal)
    """
    # optional axis value in lfilter?
    return scipy.signal.lfilter([1, -p], [1], input)


def windowing(input):
    """
    Applies hamming window to the input frames.

    Args:
        input: array of speech samples [N x M] where N is the number of frames and
               M the samples per frame
    Output:
        array of windowed speech samples [N x M]
    Note (you can use the function hamming from scipy.signal, include the sym=0 option
    if you want to get the same results as in the example)
    """
    hamming_window = scipy.signal.hamming(input.shape[1], sym=0)

    return input * hamming_window


def powerSpectrum(input, nfft):
    """
    Calculates the power spectrum of the input signal, that is the square of the modulus of the FFT

    Args:
        input: array of speech samples [N x M] where N is the number of frames and
               M the samples per frame
        nfft: length of the FFT
    Output:
        array of power spectra [N x nfft]
    Note: you can use the function fft from scipy.fftpack
    """
    # discrete fourier transform using scipy: 
    fft = scipy.fftpack.fft(input, nfft)
    # square: 
    return np.square(np.abs(fft))

def logMelSpectrum(input, samplingrate):
    """
    Calculates the log output of a Mel filterbank when the input is the power spectrum

    Args:
        input: array of power spectrum coefficients [N x nfft] where N is the number of frames and
               nfft the length of each spectrum
        samplingrate: sampling rate of the original signal (used to calculate the filterbank shapes)
    Output:
        array of Mel filterbank log outputs [N x nmelfilters] where nmelfilters is the number
        of filters in the filterbank
    Note: use the trfbank function provided in lab1_tools.py to calculate the filterbank shapes and
          nmelfilters
    """
    #tranposed filter bank
    filter_bank = trfbank(samplingrate, input.shape[1]).T
    #Getting the log of the dot product of the input and filter bank
    return np.log(np.dot(input, filter_bank))

def cepstrum(input, nceps):
    """
    Calulates Cepstral coefficients from mel spectrum applying Discrete Cosine Transform

    Args:
        input: array of log outputs of Mel scale filterbank [N x nmelfilters] where N is the
               number of frames and nmelfilters the length of the filterbank
        nceps: number of output cepstral coefficients
    Output:
        array of Cepstral coefficients [N x nceps]
    Note: you can use the function dct from scipy.fftpack.realtransforms
    """
    # "Return the Discrete Cosine Transform of arbitrary type sequence x." :
    dct = scipy.fftpack.realtransforms.dct(input)
    # Get the correct number of output cepstra coefficients:
    return dct[:, 0:nceps]


def dtw(x, y, dist):
    """Dynamic Time Warping.

    Args:
        x, y: arrays of size NxD and MxD respectively, where D is the dimensionality
              and N, M are the respective lenghts of the sequences
        dist: distance function (can be used in the code as dist(x[i], y[j]))

    Outputs:
        d: global distance between the sequences (scalar) normalized to len(x)+len(y)
        LD: local distance between frames from x and y (NxM matrix)
        AD: accumulated distance between frames of x and y (NxM matrix)
        path: best path through AD

    Note that you only need to define the first output for this exercise.
    """

if __name__ == "__main__":
    # data = np.load('/home/cornelis/KTH/speech_recog/lab1/lab1_data.npz', allow_pickle=True)['data']
    # example = np.load('/home/cornelis/KTH/speech_recog/lab1/lab1_example.npz', allow_pickle=True)['example'].item()
    example = np.load('lab1_example.npz', allow_pickle=True)['example'].item()

    # Frames:
    print("Sampling rate: " + str(example['samplingrate']))
    # 20000 * 0.02 = 400
    # 20000 * 0.01 = 200
    frames_test = enframe(example['samples'], 400, 200)

    # Testing if correct:
    print("enframe")
    compare(frames_test, example['frames'])
    plt.pcolormesh(frames_test.T)
    plt.show()
    plt.pcolormesh(example['frames'].T)
    plt.show()

    # Preemph:
    preemp_test = preemp(frames_test)

    # Testing if correct:
    print("Preemph")
    compare(preemp_test, example['preemph'])
    plt.pcolormesh(preemp_test.T)
    plt.show()
    plt.pcolormesh(example['preemph'].T)
    plt.show()

    # Hamming Window:
    hamming_test = windowing(preemp_test)

    # Testing if correct:
    print("Hamming")
    compare(hamming_test, example['windowed'])
    plt.pcolormesh(hamming_test.T)
    plt.show()
    plt.pcolormesh(example['windowed'].T)
    plt.show()

    # Power spectrum:
    spec_test = powerSpectrum(hamming_test, 512)
    
    # Testing if correct:
    print("Power Spectrum")
    compare(spec_test, example['spec'])
    plt.pcolormesh(spec_test.T)
    plt.show()
    plt.pcolormesh(example['spec'].T)
    plt.show()

    # Mel-filterbank:
    mel_test = logMelSpectrum(spec_test, example['samplingrate'])

    # Testing if correct:
    print("Log Mel Spectrum")
    compare(mel_test, example['mspec'])
    plt.pcolormesh(mel_test.T)
    plt.show()
    plt.pcolormesh(example['mspec'].T)
    plt.show()

    # Cepstrals:
    cepstrals_test = cepstrum(mel_test, 13)

    # Testing if correct:
    print("Cepstrals")
    compare(cepstrals_test, example['mfcc'])
    plt.pcolormesh(cepstrals_test.T)
    plt.show()
    plt.pcolormesh(example['mfcc'].T)
    plt.show()
