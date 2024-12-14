# ERP AI Agent Assignment

## Repository Overview
This repository contains the codebase for an **AI Agent for Money Requests**, enabling users to submit project funding requests and manage records using text or voice inputs. It integrates technologies like Whisper, spaCy, and SQLite within a user-friendly Gradio interface.

## Step-by-Step Guide

### 1. Clone the Repository
Start by cloning the repository to your local machine:

```bash
git clone https://github.com/MohsinRazaKhanSipra/ERP_AI_Agent_Assignment.git
cd ERP_AI_Agent_Assignment
```

### 2. Set Up a Virtual Environment
To manage the dependencies, it is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

### 3. Install Dependencies
Install the required Python libraries by running the following command:

```bash
pip install -r requirements.txt
```

### 4. Download the Pre-trained Whisper Model
This repository uses OpenAI's Whisper model for speech-to-text conversion. The model will be automatically downloaded when running the app. Ensure you have sufficient disk space and an active internet connection for the download.


### 5. Place the Fine-Tuned spaCy Model
If you already have a fine-tuned spaCy model:

Place the model directory (e.g., fine_tuned_model/) in the project folder.
Ensure the code references the correct model path.
If you don't have a fine-tuned model, please refer to the Training spaCy Model section in the documentation to create and fine-tune the model.


### 6. Run the Application
Run the following command to launch the Gradio interface:

```bash
python app.py
```
This will start the application. Once it is running, a local URL will be displayed (e.g., http://127.0.0.1:7860). Open the URL in your browser to interact with the application.


### 7. Test the Application
You can test the application by:

Submitting requests using the text input field or microphone for voice input.
Viewing database records by clicking on the "View Records" button.



### 8. Customize or Extend
You can customize or extend the application as follows:

Modify the training_data in the script to add more examples for entity recognition.
Update the database schema in add_request_to_db() if necessary.
Enhance the user interface using Gradio components for a better user experience.



## Key Files and Directories
- `app.py`: Main application file that contains all functionalities.
- `requirements.txt`: Contains a list of required Python packages.
- `fine_tuned_model/`: Directory for the fine-tuned spaCy model.
- `erp.db`: SQLite database file (created automatically when the application is run for the first time).
- `ERP_Agent_AI_Assignment.ipynb`: This jupyter notebook contains detail steps related to the assignment

