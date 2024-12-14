import gradio as gr
import whisper
import spacy
import sqlite3

# Load Whisper model for speech-to-text
stt_model = whisper.load_model("base")

# Load spaCy for entity extraction
nlp = spacy.load("fine_tuned_model")

# Global variables to store request data
project_name = ""
amount = ""
reason = ""


# Speech-to-text function
def speech_to_text(audio):
    result = stt_model.transcribe(audio.name)
    print(result["text"])
    return result["text"]


# Extract entities using spaCy
def extract_entities(text):
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        entities[ent.label_] = ent.text
    return entities


# Add request to database
def add_request_to_db(project_name, amount, reason):
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS money_requests (project_name TEXT, amount REAL, reason TEXT)")
    cursor.execute("INSERT INTO money_requests (project_name, amount, reason) VALUES (?, ?, ?)",
                   (project_name, amount, reason))
    conn.commit()
    conn.close()


# Retrieve records from the database
def view_database_records():
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS money_requests (project_name TEXT, amount REAL, reason TEXT)")
    records = cursor.execute("SELECT * FROM money_requests").fetchall()
    conn.close()
    if not records:
        return "No records found."
    return records


# Process text/audio requests
def process_request(text_input):
    global project_name, amount, reason
    
    if not project_name or not amount or not reason:
        # If required data isn't available, extract entities
        entities = extract_entities(text_input)
        project_name = entities.get('PROJECT', '')
        amount = entities.get('MONEY', '')
        reason = entities.get('REASON', '')

        if not project_name or not amount or not reason:
            missing_fields = []
            if not project_name:
                missing_fields.append("project name")
            if not amount:
                missing_fields.append("amount")
            if not reason:
                missing_fields.append("reason")
            return f"Missing fields: {', '.join(missing_fields)}. Please provide the missing information."

        return f"You are going to add a request for project: {project_name}, request amount: {amount}, reason: {reason}. Are you sure you want to proceed? Yes/No"
    
    # Confirmation Step
    if "yes" in text_input.lower() or "okay" in text_input.lower() or "confirm" in text_input.lower():
        add_request_to_db(project_name, amount, reason)
        project_name_temp=project_name
        amount_temp=amount
        reason_temp=reason
        project_name, amount, reason = "", "", ""  # Reset the global variables after the request is added
        return f"Your request for project '{project_name_temp}' with amount {amount_temp} for {reason_temp} has been submitted successfully."
        
    else:
        project_name, amount, reason = "", "", ""  # Reset the global variables if canceled
        return "Request has been canceled."


# Gradio Interface for handling chatbot and database interactions
def chatbot_interface(text_input, audio_input=None):
    if audio_input:
        text_input = speech_to_text(audio_input)
    
    # Process the request and confirmation flow
    return process_request(text_input)


# Gradio Interface for viewing database records
def database_view_interface():
    return view_database_records()


# Create the Gradio Interface
iface = gr.Blocks()

with iface:
    gr.Markdown("# AI Agent for Money Requests")
    gr.Markdown("Use text or voice commands to request money for a project or view existing records.")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Submit Request")
            text_input = gr.Textbox(label="Enter your text request:", placeholder="Type your message here...")
            audio_input = gr.Audio(label="Or use voice input:", sources="microphone")
            submit_button = gr.Button("Submit Request")
            
        
        with gr.Column():
            gr.Markdown("### AI Agent Response")
            response_output = gr.Textbox(label="Response:")
            gr.Markdown("### View Database Records")
            view_records_button = gr.Button("View Records")
            records_output = gr.Textbox(label="Database Records:")

    # Bind functions
    submit_button.click(fn=chatbot_interface, inputs=[text_input, audio_input], outputs=response_output)
    view_records_button.click(fn=database_view_interface, outputs=records_output)

# Launch the Interface
iface.launch()
