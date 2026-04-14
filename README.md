# Prerequisites

## Before running the application, ensure you have **Python 3.10** or higher installed. You will need to install the following dependencies:
```bash
pip install gradio openai
```

# Configuration (Environment Variables)
The program retrieves API keys from your system's environment variables for security. You must set the following keys before launching the app:

**On Windows (PowerShell):**

```powershell
$env:DASHSCOPE_API_KEY="your_aliyun_api_key_here"
$env:ZHIPU_API_KEY="your_zhipu_api_key_here"
```


# File Structure
* AI_ui.py: The main application script.

* files/: Directory where exported dialogue JSON files are stored.

* README.md: Setup and usage instructions.


# How to Run
Assume that the file is under "path/to/hci_hw_2", and the file name is AI_ui.py.

1. Navigate to the project directory
```bash
cd path/to/hci_hw_2
```

2. Run the Python script
```bash
python AI_ui.py
```

3. Open your browser and go to the local URL provided in the terminal (usually http://127.0.0.1:7860).


# Key Features
**Model Switching:** Seamlessly toggle between Alibaba's Qwen and Zhipu's GLM-4 models to compare performance.

**Parameter Tuning:** Adjust the Sampling Temperature via a slider to control the creativity vs. determinism of the AI responses.

**Role-Play Mode:** Initialized with a specific prompt (e.g., AI Interviewer) to demonstrate specialized LLM behavior.

**Dialogue Export:** Save your conversation history as a structured JSON file in the files/ folder for further analysis.

**Responsive UI:** A clean, functional layout designed for optimal Human-Computer Interaction (HCI).

# Tips for the Evaluator
* To test the Role-Play feature, simply start typing in the input box. The AI is pre-configured to act as an interviewer.

* The Reset button clears the current conversation state and restarts the interaction.

* If the UI fails to load, please ensure no other service is occupying port 7860.