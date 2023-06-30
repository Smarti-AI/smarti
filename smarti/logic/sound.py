"""handle sound operations"""
import io
import logging
import sys

import pydub
import soundfile as sf
import speech_recognition as sr

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler(sys.stdout))

# language for speech to text recognition
# pylint: disable=W0511
# TODO: detect this automatically based on the user's language
LANGUAGE = "iw-IL"


# run speech recognition on the audio data
def recognize_audio(audio_bytes):
    """run speech recognition on the audio data"""
    recognizer = sr.Recognizer()
    audio_text = recognizer.recognize_google(audio_bytes, language=LANGUAGE)
    return audio_text


# convert ogg audio bytes to audio data which speechrecognition library can process
def convert_audio_bytes(audio_bytes):
    """convert ogg audio bytes to audio data which speechrecognition library can process"""
    ogg_audio = pydub.AudioSegment.from_ogg(io.BytesIO(audio_bytes))
    ogg_audio = ogg_audio.set_sample_width(4)
    wav_bytes = ogg_audio.export(format="wav").read()
    audio_data, sample_rate = sf.read(io.BytesIO(wav_bytes), dtype="int32")
    sample_width = audio_data.dtype.itemsize
    log.info("audio sample_rate:{%s}, sample_width:{%s}", sample_rate, sample_width)
    audio = sr.AudioData(audio_data, sample_rate, sample_width)
    return audio
