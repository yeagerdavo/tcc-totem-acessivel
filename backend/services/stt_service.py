import whisper
import subprocess
import os

# modelo muito mais rápido
model = whisper.load_model("tiny")


def transcrever_audio(caminho_audio):

    caminho_convertido = "audio_convertido.wav"

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", caminho_audio,
        "-ar", "16000",
        "-ac", "1",
        caminho_convertido
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
    )

    print("Áudio convertido:", os.path.exists(caminho_convertido))

    result = model.transcribe(
        caminho_convertido,
        language="pt",
        fp16=False
    )

    texto = result["text"].strip()

    print("Texto:", texto)

    return texto