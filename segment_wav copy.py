import re
import json
import requests
from pydub import AudioSegment


def split_audio(file_path, segment_length_ms):
    audio = AudioSegment.from_file(file_path)
    audio_length_ms = len(audio)
    segments = []

    for i in range(0, audio_length_ms, segment_length_ms):
        start_time = i
        end_time = i + segment_length_ms
        segment = audio[start_time:end_time]
        segments.append(segment)

    return segments


def transcribe_audio_wit(file_path, access_token):
    url = "https://api.wit.ai/speech"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "audio/wav"
    }

    with open(file_path, "rb") as audio_file:
        response = requests.post(url, headers=headers, data=audio_file)

    if response.status_code == 200:
        try:
            raw_response = response.text
            json_objects = [json.loads(m.group()) for m in re.finditer(
                r'\{(?:[^{}]|(?R))*\}', raw_response)]

            combined_text = ""
            for json_data in json_objects:
                if "text" in json_data and json_data["text"]:
                    combined_text += json_data["text"] + " "

            return combined_text.strip() if combined_text else None
        except Exception as e:
            print(f"Erreur lors de l'analyse de la réponse JSON: {e}")
            print(f"Réponse brute: {response.text}")
            return None
    else:
        print(f"Erreur lors de la requête à Wit.ai: {response.status_code}")
        print(response.text)
        return None


def transcribe_segments(segments, access_token):
    transcriptions = []

    for i, segment in enumerate(segments):
        segment_file_path = f"segment_{i}.wav"
        segment.export(segment_file_path, format="wav")
        transcription = transcribe_audio_wit(segment_file_path, access_token)
        transcriptions.append(transcription)

    return transcriptions


# Remplacez par le chemin de votre fichier audio
file_path = "converted_audio.wav"
# Remplacez par votre token d'accès Wit.ai
access_token = "ZOFJ46NWKHBXVAFX4IT5TEL5BNQUENAK"

segment_length_ms = 20 * 1000  # 10 secondes
segments = split_audio(file_path, segment_length_ms)
transcriptions = transcribe_segments(segments, access_token)

for i, transcription in enumerate(transcriptions):
    print(f"Segment {i + 1}: {transcription}")
