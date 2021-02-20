'''
Summary
Library of Audio and Video Processing Functions made by ME
'''

# Imports
import numpy as np
import os
from cv2 import VideoWriter, imread, VideoWriter_fourcc
import cv2
from os.path import isfile, join
from scipy.io import wavfile
import pygame
import os
import pickle
from tqdm import tqdm
import time
import wave as w
import struct
import winsound

# Media Conversion
#FS
def convert_frames_to_video(pathIn, pathOut, fps=25.0, image_prefix=""):
	#DS
    # Converts list of frames into a video
    #DE
    #IS
    import os
    import cv2
    #IE

    frame_array = []
    files = [f for f in os.listdir(pathIn) if os.path.isfile(join(pathIn, f))]
 
    print(files)
    
    for i in range(len(files)):
        filename = pathIn + files[i]
        # Read each image file
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        print(filename)
        # Inserting the frames into an image array
        frame_array.append(img)
 
    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
 
    for i in range(len(frame_array)):
        # Writing to a image array
        out.write(frame_array[i])
    out.release()
#FE

# Video Display
#FS
def DisplayVideo(videoPath=0, quitChar='X'):
	#DS
    # Display video stream in a window
    #DE
    #IS
    import cv2
    #IE

    cap = cv2.VideoCapture(videoPath)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord(quitChar):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
#FE

#FS
def GetWebcamVideo(Filter=None, quitChar='q'):
	#DS
    # Get Webcam Video Stream
    #DE
    #IS
    import cv2
    #IE

    return cv2.VideoCapture(0)
#FE

# Piano Player
#FS
def speedx(snd_array, factor):
	#DS
    # Speeds up / slows down a sound, by some factor
    #DE
    #IS
    import numpy as np
    #IE

    indices = np.round(np.arange(0, len(snd_array), factor))
    indices = indices[indices < len(snd_array)].astype(int)
    return snd_array[indices]
#FE

#FS
def stretch(snd_array, factor, window_size, h):
	#DS
    # Stretches/shortens a sound, by some factor
    #DE
    #IS
    import numpy as np
    #IE

    phase = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros(int(len(snd_array) / factor + window_size))

    for i in np.arange(0, len(snd_array) - (window_size + h), h*factor):
        i = int(i)
        # Two potentially overlapping subarrays
        a1 = snd_array[i: i + window_size]
        a2 = snd_array[i + h: i + window_size + h]

        # The spectra of these arrays
        s1 = np.fft.fft(hanning_window * a1)
        s2 = np.fft.fft(hanning_window * a2)

        # Rephase all frequencies
        phase = (phase + np.angle(s2/s1)) % 2*np.pi

        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
        i2 = int(i/factor)
        result[i2: i2 + window_size] += hanning_window*a2_rephased.real

    # normalize (16bit)
    result = ((2**(16-4)) * result/result.max())

    return result.astype('int16')
#FE

#FS
def pitchshift(snd_array, n, window_size=2**13, h=2**11):
	#DS
    # Changes the pitch of a sound by ``n`` semitones
    #DE
    #IS
    #IE

    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    return speedx(stretched[window_size:], factor)
#FE

#FS
def GenerateKeySoundDict(sound_file_path, KeyConfig_file_path, TransposedSounds_file_path, SaveSounds=True):
	#DS
    # Generate Dictionary of key sounds
    #DE
    #IS
    import wavfile
    import pickle
    #IE

    # Get Reference Audio File
    fps, sound = wavfile.read(sound_file_path)

    # Create Key Sounds from reference file
    tones = range(-25, 25)
    print('Started Creating Key Sounds')
    transposed_sounds = []
    for tone in tqdm(tones):
        transposed_sounds.append(pitchshift(sound, tone))
    print('Finished Creating Key Sounds')

    if SaveSounds:
        pickle.dump(transposed_sounds, open(TransposedSounds_file_path, 'wb'))

    # Init Key Configs
    keys = open(KeyConfig_file_path, 'r+').read().split('\n')
    sounds = map(pygame.sndarray.make_sound, transposed_sounds)
    
    return keys, sounds, fps
#FE

#FS
def LoadKeySounds(TransposedSounds_file_path, KeyConfig_file_path):
	#DS
    # Load Key sounds from file
    #DE
    #IS
    import pygame
    import wavfile
    import pickle
    #IE

    # Init Key Configs
    keys = open(KeyConfig_file_path, 'r+').read().split('\n')
    sounds = map(pygame.sndarray.make_sound, pickle.load(open(TransposedSounds_file_path, 'rb')))
    return keys, sounds
#FE

# Piano Audio Generator
#FS
def ParsePianoSequenceFile(filepath):
	#DS
    # Parse Piano Sequence File to get playable sequence of sounds
    #DE
    #IS
    #IE

    MainSeq = []
    SubSeqs = {}

    beepfile = open(filepath, 'r')
    CurSubSeqName = None
    for line in beepfile.readlines():
        line = line.strip()
        if line.startswith('//'):
            continue
        elif '{' in line:
            CurSubSeqName = line[:(line.index('{'))].strip()
            SubSeqs[CurSubSeqName] = []
        elif '}' in line:
            CurSubSeqName = None
        elif '.' in line:
            if CurSubSeqName == None:
                MainSeq.append(['S', line[(line.index('.')+1):].strip(), ''])
            else:
                SubSeqs[CurSubSeqName].append(['S', line[(line.index('.')+1):].strip(), ''])
        elif '-' in line:
            if CurSubSeqName == None:
                MainSeq.append(['D', line[(line.index('-')+1):].strip(), ''])
            else:
                SubSeqs[CurSubSeqName].append(['D', line[(line.index('-')+1):].strip(), ''])
        else:
            splitline = line.split(' ')
            freq = splitline[0].strip()
            dur = splitline[1].strip()
            asynccheck = str(False)
            if len(splitline) > 2:
                asynccheck = str(splitline[2].strip() == 'a')
            if CurSubSeqName == None:
                MainSeq.append(['M', freq, dur, asynccheck])
            else:
                SubSeqs[CurSubSeqName].append(['M', freq, dur, asynccheck])
    return MainSeq, SubSeqs
#FE

#FS
def GetFullMainSeq(MainSeq, SubSeqs):
	#DS
    # Get full sequence of sounds to play from sequence with repeated subsequences
    #DE
    #IS
    #IE

    SubSeqsFull = {}
    FullMainSeq = []

    for s in MainSeq:
        if s[0] == 'M':
            FullMainSeq.append([s[1], s[2], s[3]])
        elif s[0] == 'S':
            if s[1] not in SubSeqsFull.keys():
                SubSeqsFull[s[1]] = []
                SubSeqsFull[s[1]] = GetFullMainSeq(SubSeqs[s[1]], SubSeqs)
            FullMainSeq.extend(SubSeqsFull[s[1]])
        elif s[0] == 'D':
            FullMainSeq.append([s[1], s[2], s[3]])
    return FullMainSeq
#FE

#FS
def PlayPianoSequence(Seq, KeySoundDict, fade_ms=50):
	#DS
    # Play Piano Sequence in a window once
    #DE
    #IS
    import time
    import wavfile
    import pygame
    #IE

    print("Started Audio Sequence")
    for s in Seq:
        if s[1] != '':
            print("Playing key", s[0], " for", s[1], "ms async:", s[2])
            if s[2] == 'False':
                KeySoundDict[s[0]].play(fade_ms=fade_ms)
                time.sleep(float(s[1])/1000)
            else:
                KeySoundDict[s[0]].play(fade_ms=fade_ms)
        else:
            print("Delaying for", float(s[0]), "ms")
            time.sleep(float(s[0])/1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
    print("Ended Audio Sequence")
#FE

#FS
def LoopPianoSequence(Seq, KeySoundDict):
	#DS
    # Play Piano Sequence in a window looped infinitely
    #DE
    #IS
    #IE

    while True:
        PlayPianoSequence(Seq, KeySoundDict)
#FE

#FS
def CreatePianoSounds(RefSound_file_path, KeyConfig_file_path, TransposedSounds_file_path='', SaveSounds=False):
	#DS
    # Create new piano sounds dictionary from Reference sound
    #DE
    #IS
    import wavfile
    import pygame
    import pickle
    #IE

    # Get Reference Audio File
    fps, sound = wavfile.read(RefSound_file_path)

    # Create Key Sounds from reference file
    tones = range(-25, 25)
    print('Started Creating Key Sounds')
    transposed_sounds = []
    for tone in tqdm(tones):
        transposed_sounds.append(pitchshift(sound, tone))
    print('Finished Creating Key Sounds')

    # Save Sounds
    if SaveSounds:
        pickle.dump(transposed_sounds, open(TransposedSounds_file_path, 'wb'))

    # Init Pygame
    pygame.mixer.init(fps, -16, 1, 2048)
    screen = pygame.display.set_mode((150, 150))

    # Init Key Configs
    keys = open(KeyConfig_file_path, 'r+').read().split('\n')
    sounds = map(pygame.sndarray.make_sound, transposed_sounds)
    keysound_dict = dict(zip(keys, sounds))
    return keysound_dict
#FE

# Audio Processing
# Create WAV Files
#FS
def CreateWAVFile(filepath, nchannels, sampwidth, framerate, nframes, comptype, compname):
	#DS
    # Create new WAV File from sound
    #DE
    #IS
    import wavfile
    #IE

    #open(filepath, 'w+')
    fw = OpenWAV(filepath, 'w')
    # (nchannels, sampwidth, framerate, nframes, comptype, compname)
    params = (nchannels, sampwidth, framerate, nframes, comptype, compname)
    fw.setparams(params)
#FE

# Open WAV Files
#FS
def OpenWAV(filepath, mode):
	#DS
    # Open WAV File from path for writing or reading
    #DE
    #IS
    import os
    #IE

    if not os.path.exists(filepath):
        open(filepath, 'w+')
    if mode in ['r', 'rb', 'Read', 'read']:
        return w.open(filepath, 'rb')
    if mode in ['w', 'wb', 'Write', 'write']:
        return w.open(filepath, 'wb')
#FE

#FS
def WriteBytesToWAV(filepath, data, datasize, nchannels=2, sampwidth=3, framerate=48000, comptype='NONE', compname='not compressed'):
	#DS
    # Write Bytes to WAV File
    #DE
    #IS
    import os
    import wavfile
    #IE

    if not os.path.exists(filepath):
        CreateWAVFile(filepath, nchannels, sampwidth, framerate, datasize, comptype, compname)
        fw = OpenWAV(filepath, 'w')
        for sample in data:
            fw.writeframes(struct.pack('h', int( sample * 32767.0 )))
        #fw.writeframes(data)
        fw.close()
    else:
        fr = OpenWAV(filepath, 'r')
        fw = OpenWAV(filepath, 'w')
        fw.setnframes(fr.getnframes() + datasize)
        fw.writeframes(data)
        fr.close()
        fw.close()
#FE

#FS
def save_wav(file_name, audio):
	#DS
    # Save audio as WAV file
    #DE
    #IS
    import os
    import wavfile
    import wave as w
    #IE

    # Open up a wav file
    wav_file = w.open(file_name,"w")

    # wav params
    nchannels = 1

    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    sample_rate = 48000
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the 
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    for sample in audio:
        print("Sample:", type(sample), sample)
        wav_file.writeframes(sample)
    wav_file.close()
#FE

# Beep Sequencer
#FS
def GenerateFreq(freq, duration): 
	#DS
    # Generate and play a particular frequency for some duration using beep
    #DE
    #IS
    import winsound
    #IE

    winsound.Beep(freq, duration)
#FE

#FS
def PlaySound(sound):
	#DS
    # Play sound using winsound library
    #DE
    #IS
    import winsound
    #IE

    winsound.PlaySound(sound)
#FE

# File Parser Code
#FS
def ParseBeepSequenceFile(filepath):
	#DS
    # Parse Beep Sequence file to get playable sequence of sounds
    #DE
    #IS
    #IE

    MainSeq = []
    SubSeqs = {}

    beepfile = open(filepath, 'r')
    CurSubSeqName = None
    for line in beepfile.readlines():
        line = line.strip()
        if line.startswith('//'):
            continue
        elif '{' in line:
            CurSubSeqName = line[:(line.index('{'))].strip()
            SubSeqs[CurSubSeqName] = []
        elif '}' in line:
            CurSubSeqName = None
        elif '.' in line:
            if CurSubSeqName == None:
                MainSeq.append(['S', line[(line.index('.')+1):].strip(), ''])
            else:
                SubSeqs[CurSubSeqName].append(['S', line[(line.index('.')+1):].strip(), ''])
        elif '-' in line:
            if CurSubSeqName == None:
                MainSeq.append(['D', line[(line.index('-')+1):].strip(), ''])
            else:
                SubSeqs[CurSubSeqName].append(['D', line[(line.index('-')+1):].strip(), ''])
        else:
            freq = line.split(' ')[0].strip()
            dur = line.split(' ')[1].strip()
            if CurSubSeqName == None:
                MainSeq.append(['M', freq, dur])
            else:
                SubSeqs[CurSubSeqName].append(['M', freq, dur])
    return MainSeq, SubSeqs
#FE

#FS
def PlayBeepSequence(Seq):
	#DS
    # Play Beep Sequence once
    #DE
    #IS
    import winsound
    import time
    #IE

    print("Started Audio Sequence")
    for s in Seq:
        if s[1] != '':
            print("Playing", s[0], "Hz for", s[1], "ms")
            winsound.Beep(int(s[0]), int(s[1]))
            #GenerateFreq(int(s[0]), int(s[1]))
        else:
            print("Delaying for", float(s[0]), "ms")
            time.sleep(float(s[0])/1000)
    print("Ended Audio Sequence")
#FE

#FS
def LoopBeepSequence(Seq):
	#DS
    # Play Beep Sequence looped infinitely
    #DE
    #IS
    import winsound
    import time
    #IE

    while True:
        PlayBeepSequence(Seq)
#FE

#FS
def PianoKeyFreqMap():
	#DS
    # Mapper for piano keys to frequencies
    #DE
    #IS
    #IE

    KeysFreq = {}
    Keys = ['C6', 'C6#', 'D6', 'D6#', 'E6', 'F6', 'F6#', 'G6', 'G6#', 'A6', 'A6#', 'B6', 
    'C7', 'C7#', 'D7', 'D7#', 'E7', 'F7', 'F7#', 'G7', 'G7#', 'A7', 'A7#', 'B7', 'C8']
    KeyNos = range(64, 88 + 1, 1)
    for key, keyno in zip(Keys, KeyNos):
        KeysFreq[key] = [GetKeyFreq(keyno)]
    return Keys, KeysFreq
#FE

#FS   
def GetKeyFreq(KeyNo):
	#DS
    # Get standard frequency associated with a key
    #DE
    #IS
    #IE

    return 2 ** ((KeyNo - 49) / 12) * 440
#FE

#FS
def PlayPianoSounds():
	#DS
    # Plays all piano sounds once
    #DE
    #IS
    #IE

    duration = 1000
    Keys, KeyFreqs = PianoKeyFreqMap()
    for key in Keys:
        for freq in KeyFreqs[key]:
            print(key, freq)
            if freq >= 37 and freq <= 32767:
                GenerateFreq(int(round(freq)), duration)
#FE