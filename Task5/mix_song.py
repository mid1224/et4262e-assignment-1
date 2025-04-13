from pydub import AudioSegment

# Load the beat and lyrics
music = AudioSegment.from_wav("music.wav")
lyrics = AudioSegment.from_wav("input.wav")

# Make sure both are the same length (or adjust as needed)
min_length = min(len(music), len(lyrics))
music = music[:min_length]
lyrics = lyrics[:min_length]

# Mix them together (overlay)
mixed = music.overlay(lyrics)

# Export to a new file
mixed.export("song_mix.wav", format="wav")