"""test sound module"""

from speech_recognition import AudioData

# smarti imports
from smarti.logic import sound


def test_convert_audio_bytes(input_folder):
    """test convert audio bytes"""
    with open(f"{input_folder}/hello_world.ogg", "rb") as file:
        audio_bytes = file.read()
    audio_data = sound.convert_audio_bytes(audio_bytes)
    assert isinstance(audio_data, AudioData)


def test_recognize_audio(mocker, input_folder):
    """test recognize audio"""
    mocker.patch(
        "speech_recognition.Recognizer.recognize_google", return_value="hello world"
    )
    with open(f"{input_folder}/hello_world.ogg", "rb") as file:
        audio_bytes = file.read()
    audio_data = sound.convert_audio_bytes(audio_bytes)
    text = sound.recognize_audio(audio_data)
    assert text == "hello world"
