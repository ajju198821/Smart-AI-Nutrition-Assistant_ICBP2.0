# Smart AI Nutrition Assistant

The **Smart AI Nutrition Assistant** is an innovative web application designed to empower users with personalized health and nutrition solutions. Built using Streamlit, it leverages Groq's Large Language Model (LLM) and Hugging Face's vision models to provide tailored diet plans, workout routines, and food image analysis.

## Features

- **Personalized Nutrition Plans**: Generate 7-day meal plans based on user inputs such as age, weight, health goals, dietary preferences, and cultural context.
- **Goal-Oriented Workout Plans**: Create customized weekly exercise routines aligned with fitness goals and available equipment.
- **Food Image Analysis**: Analyze uploaded food images to estimate calories, identify ingredients, and provide health suggestions.
- **Interactive AI Chatbot**: Engage with an AI nutritionist or fitness coach for real-time advice and follow-up questions.
- **Culturally Relevant Recipes**: Incorporate local and culturally appropriate meal and snack options.
- **Responsive UI**: Streamlit-based interface with dynamic backgrounds and user-friendly navigation.

## Prerequisites

- **Python**: Version 3.8 or higher
- **Groq API Key**: Obtain from [xAI](https://x.ai/api)
- **Image Files**: Background images (`welcomepage.jpg`, `personal.avif`, `workout2.webp`) for UI styling
- **Internet Connection**: Required for API calls to Groq and Hugging Face

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/smart-ai-nutrition-assistant.git
   cd smart-ai-nutrition-assistant
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the project root:
     ```bash
     touch .env
     ```
   - Add your Groq API key:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```

5. **Add Background Images**:
   - Place `welcomepage.jpg`, `1n1n1.avif`, and `workout2.webp` in the project root directory.
   - Note: Replace with your own images or update the code to use different file paths if needed.

6. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Access the App**:
   - Open your browser and navigate to `http://localhost:8501` after running the app.
   
2. **Navigate Pages**:
   - **Welcome**: Overview of the app's capabilities.
   - **Nutrition Plan**: Input personal details and preferences to generate a 7-day diet plan.
   - **Workout Plan**: Specify fitness goals and equipment to receive a weekly exercise routine.
   - **Food Image Analyzer**: Upload food images to analyze calories and ingredients.

3. **Interact with the Chatbot**:
   - Use the chat interface on each page to ask follow-up questions about nutrition, workouts, or food analysis.

## File Structure

```
smart-ai-nutrition-assistant/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not tracked)
├── welcomepage.jpg         # Background image for Welcome page
├── 1n1n1.avif             # Background image for Nutrition Plan page
├── workout2.webp          # Background image for Workout Plan page
├── README.md              # Project documentation
└── .gitignore             # Git ignore file
```

## Technologies Used

- **Frontend**: Streamlit for interactive web UI
- **Backend**: Python with LangChain for LLM integration, Transformers for vision model
- **AI Models**:
  - **LLM**: Groq's LLaMA3-8B-8192 via ChatGroq
  - **Vision Model**: Salesforce BLIP (blip-image-captioning-base) from Hugging Face
- **APIs**: Groq API, Hugging Face API
- **Libraries**: PIL (Pillow), base64, python-dotenv
- **Styling**: Custom CSS for background images and UI enhancements

## Requirements File

Create a `requirements.txt` with the following content:

```
streamlit
langchain-groq
python-dotenv
transformers
pillow
torch
```

Install with:
```bash
pip install -r requirements.txt
```

## Troubleshooting

- **API Key Issues**: Ensure `GROQ_API_KEY` is correctly set in `.env`.
- **Missing Images**: Verify that `welcomepage.jpg`, `1n1n1.avif`, and `workout2.webp` exist in the project root. If not, replace with valid image files or modify `set_background` function.
- **Model Loading Errors**: Check internet connectivity and ensure sufficient memory for loading BLIP models.
- **Streamlit Errors**: Confirm Python version (3.8+) and update Streamlit if needed (`pip install --upgrade streamlit`).

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## Acknowledgments

- **xAI**: For providing the Groq API and LLaMA3 model.
- **Hugging Face**: For the BLIP vision model.
- **Streamlit**: For the intuitive web framework.

---

*Built with ❤️ by Abdul Aziz Md*

*Last Updated: May 17, 2025*
