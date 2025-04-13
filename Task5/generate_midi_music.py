from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo

midi = MidiFile()

bpm = 128 # Set the BPM for the song

# Set tempo BPM
tempo = bpm2tempo(bpm)
tempo_track = MidiTrack()
tempo_track.append(MetaMessage('set_tempo', tempo=tempo))
midi.tracks.append(tempo_track)

# Total beats calculation: number of beats = time / (60 seconds / bpm)

input_record_length = 225 # seconds (3:45 minutes)
num_beats = int(input_record_length * bpm / 60) - 3 # Calculate number of beats needed for the song to last 3:45 min at 100 BPM

# Piano Track (Channel 0)
piano = MidiTrack()
piano.append(Message('program_change', program=0, channel=0))  # Acoustic Piano
piano_melody = [
    60, 64, 67, 64,   # C major arpeggio pattern
    60, 63, 67, 63,   # C7 outline
    65, 69, 72, 69,   # F major figure
    59, 62, 67, 62,   # G7 outline
    
    57, 61, 65, 61,   # F/A arpeggio 
    55, 59, 62, 59,   # G7/B pattern
    60, 64, 67, 72,   # C6 rising figure
    57, 54, 57, 60    # D7 to C resolution
]

# Single note playback (much simpler)
for i in range(num_beats):
    note = piano_melody[i % len(piano_melody)]
    piano.append(Message('note_on', note=note, velocity=75, time=0, channel=0))
    piano.append(Message('note_off', note=note, velocity=75, time=480, channel=0))
midi.tracks.append(piano)

# Sax Track (Channel 1)
saxophone = MidiTrack()
saxophone.append(Message('program_change', program=65, channel=1))
saxophone_melody = [
    72, 74, 76, 72,   # Playful opening motif
    72, 69, 71, 72,   # Bouncy response
    74, 76, 79, 77,   # Rising excitement
    76, 72, 69, 67,   # Playful descent
    
    69, 72, 76, 77,   # Rising line
    76, 74, 72, 71,   # Swinging phrase
    72, 74, 76, 72,   # Callback to opening
    71, 69, 67, 64    # Playful ending
]
for i in range(num_beats):
    note = saxophone_melody[i % len(saxophone_melody)]
    saxophone.append(Message('note_on', note=note, velocity=90, time=0, channel=1))
    saxophone.append(Message('note_off', note=note, velocity=90, time=480, channel=1))  # 1 beat
midi.tracks.append(saxophone)

# Save MIDI file
midi.save("music.mid")