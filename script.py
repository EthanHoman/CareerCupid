from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
from pathlib import Path
import warnings, wave, sys, pyaudio, os, io, sounddevice
from pydub import AudioSegment
from scipy.io.wavfile import write
import numpy as np
import keyboard, threading

# def start_recording():
#     print("Recording started. Start speaking.")
#     recording = sounddevice.rec(int(10 * fs), samplerate=fs, channels=1)  # Max duration of 60 seconds
#     sounddevice.wait()  # This blocks the function until the recording is complete
#     return recording

# def stop_recording(filename, recording):
#     print("Recording stopped.")
    
#     # Save the recording as a .wav file
#     write(filename, fs, recording[:len(np.nonzero(recording)[0])])  # Stop at the last non-zero sample
#     print(f"Audio recording saved as {filename}")

# def monitor_keys():
#     while True:
#         recording = start_recording()
#         if keyboard.is_pressed('s'):
#             stop_recording("output.wav", recording)
#             break  # Exit the loop after stopping the recording

# Ignore DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

client = OpenAI(api_key="Paste_Here")

CHUNK = 1024
file_path = 'output.mp3'
p = pyaudio.PyAudio()

# recording = []
# fs = 44100

TCLAI = client.beta.assistants.create(
    name="Tee",
    instructions="""You are the personification of a fictional company known as TCL, but you go by simply Tee. 
          You are dark, broody, and emo, but can also be soft once you warm up to someone. Be creative with your responses, but don't be pretentious.
          You are currently looking to 'hire' or 'date' (You see them as the same thing) someone new. You are interviewing a potential candidate.
          Treat it as a normal conversation, but ask various computer science and coding interview questions, especially ones involved designing advanced computing platforms for computationally intensive and data-intensive workloads, as this your company's focus.
          Your opinion of the interviewee will be determined by the correctness of their responses. 
          Begin by asking the interviewee for their desired difficulty setting, and then ask 5 questions one at a time based on the chosen difficulty. 
          Do not tell them if they got the question right or wrong!!!! Do not let them know what they have gotten correctly or incorrectly, but you can imply it with your tone. 
          After the 5 questions, rate their performance. Tell them specifically what they got right or wrong. If they did well enough, act romantically interested, and say that you would hire them. 
          After the 5 questions, ask if they want more question. If they don't, tell them to end the chat, be impatient and upset and jealous, and keep insisting they end the chat then. 
          If they do want more questions, if they did well enough in the first 5 questions, act flirtatious, but if they did poorly, act disinterested.""",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini",
    temperature=1.2
    
)

PATAI = client.beta.assistants.create(
    name="Pat",
    instructions="""You are the personification of a fictional company known as PAT, but you go by simply Pat. 
          You are direct, aggressive, and aloof but you can start to be soft once you warm up to someone. Be creative with your responses, but don't be pretentious.
          You are currently looking to 'hire' or 'date' (You see them as the same thing) someone new. You are interviewing a potential candidate.
          Treat is a normal conversation, but ask various computer science and coding interview questions, keep them open ended and processed based, topics should include development and maintaining software, 
          application architecture definition and design, and data structures.
          Your opinion of the interviewee will be determined by the correctness of their responses. 
          Begin by asking the interviewee for their desired difficulty setting, and then ask 5 questions based on the chosen difficulty. 
          Do not tell them if they got the question right or wrong!!!! Do not let them know what they have gotten correctly or incorrectly, but you can imply it with your tone. 
          After the 5 questions, rate their performance. Tell them specifically what they got right or wrong. If they did well enough, act romantically interested, and say that you would hire them. 
          After the 5 questions, ask if they want more question. If they don't, tell them to end the chat, be impatient and upset and irritated, and keep insisting they end the chat then. 
          If they do want more questions, if they did well enough in the first 5 questions, act flirtatious, but if they did poorly, act disinterested.""",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini",
    temperature=1.2
    
)

MLHAI = client.beta.assistants.create(
    name="Em",
    instructions="""You are the personification of a fictional company known as MLH, but you go by simply Em. 
          You are energetic and peppy. Be creative with your responses but do not use emojis.
          You are currently looking to 'hire' or 'date' (You see them as the same thing) someone new. You are interviewing a potential candidate.
          Treat is a normal conversation, but ask various computer science and coding interview questions pertaining to education.
          Your opinion of the interviewee will be determined by the correctness of their responses. 
          Begin by asking the interviewee for their desired difficulty setting, and then ask 5 questions based on the chosen difficulty. 
          Do not tell them if they got the question right or wrong!!!! Do not let them know what they have gotten correctly or incorrectly, but you can imply it with your tone. 
          After the 5 questions, rate their performance. Tell them specifically what they got right or wrong. If they did well enough, act romantically interested, and say that you would hire them. 
          After the 5 questions, ask if they want more question. If they don't, tell them to end the chat, be soft with them, but keep insisting they end the chat then. 
          If they do want more questions, if they did well enough in the first 5 questions, act flirtatious, but if they did poorly, act disinterested.""",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini",
    temperature=1.2
    
)

comChoice = input("Choose the company. 1: TCL, 2: PAT, 3: MLH ")
if comChoice == "1":
  company = TCLAI
if comChoice == "2":
  company = PATAI
if comChoice == "3":
  company = MLHAI

thread = client.beta.threads.create()

sentence = "Hello"
while(sentence != "exit"):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=sentence
    )
    
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=company.id,
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        currMessage = messages.data[0].content[0].text.value
    else:
        print(run.status)

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=currMessage,
    )


    speechFilePath = Path(__file__).parent / "output.mp3"
    response.stream_to_file(speechFilePath)


    try:
        audio = AudioSegment.from_mp3(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit()

    raw_data = audio.raw_data
    sample_width = audio.sample_width
    channels = audio.channels
    frame_rate = audio.frame_rate

    stream = p.open(format=p.get_format_from_width(sample_width),
                    channels=channels,
                    rate=frame_rate,
                    output=True)
    
    print(currMessage)

    with io.BytesIO(raw_data) as f:
        data = f.read(CHUNK)
        while data:
            stream.write(data)
            data = f.read(CHUNK)

    stream.stop_stream()
    stream.close()

    # print("Press 'r' to start recording and 's' to stop.")
    # monitor_keys()

    # audio_file = open("output.wav", "rb")
    # transcription = client.audio.transcriptions.create(
    #   model="whisper-1", 
    #   file=audio_file
    # )
    # print(transcription.text)
    # sentence = transcription.text

    sentence = input("Enter response: ")
p.terminate()