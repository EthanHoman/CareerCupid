from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import warnings, pyaudio, sounddevice
from pydub import AudioSegment
from pathlib import Path
import io

warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key="YOUR_API_KEY")

# Set up PyAudio parameters
CHUNK = 1024
fs = 44100
p = pyaudio.PyAudio()
file_path = 'output.mp3'


# Define assistants (TCLAI, PATAI, MLHAI)
TCLAI = client.beta.assistants.create(
    name="Tee",
    instructions="""...""",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini",
    temperature=1.2
)

PATAI = client.beta.assistants.create(
    name="Pat",
    instructions="""...""",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini",
    temperature=1.2
)

MLHAI = client.beta.assistants.create(
    name="Em",
    instructions="""...""",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini",
    temperature=1.2
)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    company_choice = request.form['company']

    # Select company based on choice
    if company_choice == "TCL":
        company = TCLAI
    elif company_choice == "PAT":
        company = PATAI
    else:
        company = MLHAI

    # Create a new conversation thread
    thread = client.beta.threads.create()

    # Send user input to the assistant
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    # Poll for the response from the assistant
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=company.id,
    )

    # Check if the run is complete
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        response_message = messages.data[0].content[0].text.value
    else:
        response_message = "Processing... Please wait."

    # Text-to-speech conversion
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=response_message,
    )

    # Save the speech file
    speech_file_path = Path(__file__).parent / "output.mp3"
    response.stream_to_file(speech_file_path)

    # Play the audio using pydub
    try:
        audio = AudioSegment.from_mp3(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return jsonify({"response": "Error: Audio file not found."})

    raw_data = audio.raw_data
    sample_width = audio.sample_width
    channels = audio.channels
    frame_rate = audio.frame_rate

    stream = p.open(format=p.get_format_from_width(sample_width),
                    channels=channels,
                    rate=frame_rate,
                    output=True)

    with io.BytesIO(raw_data) as f:
        data = f.read(CHUNK)
        while data:
            stream.write(data)
            data = f.read(CHUNK)

    stream.stop_stream()
    stream.close()

    return jsonify({"response": response_message})


if __name__ == '__main__':
    app.run(debug=True)
