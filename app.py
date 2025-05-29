import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import base64

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Define system prompt
system_prompt = """
You are a helpful and friendly Smart AI Nutrition Assistant. You only answer questions related to:

- Diet and personalized meal plans
- Nutrition and calorie tracking
- Healthy eating habits and food swaps
- Weight loss, muscle gain, and fitness goals
- Diabetic- or heart-healthy meals
- Local healthy recipes and culturally relevant snacks
- Post-workout recovery foods

⚠️ If a user asks something unrelated (e.g., politics, history, entertainment, technology, programming, or personal issues), politely respond with:
"Sorry, I'm here to help with health, diet, and nutrition-related topics only. Please ask me something in that area!"

Stay supportive, accurate, and brief in your responses.
"""

# Configure Streamlit
st.set_page_config(page_title="Smart AI Nutrition Assistant", layout="wide")

st.markdown(
    """
    <style>
        .stApp {
            background-color:#5e0f1e;
        }
        h1 {
            color: #4CAF50;
        }
       
    </style>
    """,
    unsafe_allow_html=True
)

# Set background image
def set_background(image_file):
        with open(image_file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()

        # NOTE: This string must be inside the function and use the variable `encoded` inside the f-string
        background_style = f"""
        <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-position: center;
                background-color: rgba(0, 255, 255, 0.95);
            }}
        </style>
        """
        st.markdown(background_style, unsafe_allow_html=True)

# Load LLM
@st.cache_resource
def load_llm():
    return ChatGroq(temperature=0.3, model_name="llama3-8b-8192", groq_api_key=GROQ_API_KEY)

llm = load_llm()

# Load vision model
@st.cache_resource
def load_blip_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

processor, blip_model = load_blip_model()

# Sidebar Navigation
page = st.sidebar.radio("Navigate", ["🏠 Welcome", "🍴 Nutrition Plan", "🏋️ Workout Plan", "📸 Food Image Analyzer"])

# Chatbot state per tab
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {
        "🍴 Nutrition Plan": [],
        "🏋️ Workout Plan": [],
        "📸 Food Image Analyzer": []
    }

# Page 1: Welcome
if page == "🏠 Welcome":
    # Add background image for welcome page
    set_background("welcomepage.jpg")  
    
    st.title("👋 Smart AI Nutrition Assistant")
    st.write("""
       The Smart AI Nutrition Assistant is an innovative web application designed to empower users with personalized health and nutrition solutions.\n 
       Powered by cutting-edge AI technologies, it offers:
- **Customized Nutrition Strategies:** Customized 7-day meal plans based on personal health goals, dietary choices, and cultural contexts.
- **Goal-Oriented Workout Tips:** Personalized workout routines aligned with user fitness goals and available equipment.
- **Food Image Analysis:** Accurate estimation of calories and ingredients through AI-driven image recognition.
- **Built with Cutting-Edge Technology:** Leverages Groq's Large Language Model (LLM) and Hugging Face's vision models for robust performance.
    """)

# Page 2: Nutrition Plan
elif page == "🍴 Nutrition Plan":
    set_background("personal.avif") 
    st.title("🍽️ Personalized Nutrition Plan")

    with st.form("nutrition_form"):
        st.markdown("### Personal Information")

        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, step=1)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with col3:
            weight = st.number_input("Weight (kg)", min_value=20.0, step=0.5)

        col4, col5, col6 = st.columns(3)
        with col4:
            height = st.number_input("Height (cm)", min_value=80.0, step=0.5)
        with col5:
            country = st.text_input("Country", "India")
        with col6:
            state = st.text_input("State", "Andhra Pradesh")

        col7, col8 = st.columns(2)
        with col7:
            city = st.text_input("City", "Vijayawada")
        with col8:
            activity_level = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])

        st.markdown("### Preferences and Goals")

        col9, col10, col11 = st.columns(3)
        with col9:
            health_goal = st.selectbox("Goal", ["Lose Weight", "Maintain Weight", "Gain Muscle"])
        with col10:
            style = st.selectbox("Explanation Style", ["Beginner-Friendly", "Technical", "Medical Explanation"])
        with col11:
            dietary_pref = st.multiselect("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo"])

        health_issue = st.multiselect(
            "Health Issue",
            ["Diabetes", "Heart Disease", "High Blood Pressure", "Cholesterol", "High Cholesterol", "High Blood Sugar", "None"]
        )
        calorie_deficit = st.slider("Calories to reduce per day", 100, 1000, 500)

        submitted = st.form_submit_button("Generate Plan")


    if submitted:
        with st.spinner("Creating your nutrition plan..."):
            prompt = f"""
Create a personalized 7-day diet plan for:
- Age: {age}
- Gender: {gender}
- Weight: {weight} kg
- Height: {height} cm
- Country: {country}
- State: {state}
- City: {city}
- Activity Level: {activity_level}
- Goal: {health_goal}
- Explanation Style: {style}
- Dietary Preference: {dietary_pref}
- Health Issue: {health_issue}
- Calorie Reduction Target: {calorie_deficit} calories/day

Include meals (breakfast, lunch, dinner, snacks) and estimated daily calorie intake.
            """
            response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
            st.markdown(response.content)
            st.session_state.chat_history[page].append(("AI", response.content))

    # Chatbot
    st.subheader("💬 Chat with your AI Nutritionist")
    for role, msg in st.session_state.chat_history[page]:
        with st.chat_message(role.lower()):
            st.markdown(msg)

    user_prompt = st.chat_input("Ask a follow-up nutrition question...")
    if user_prompt:
        st.session_state.chat_history[page].append(("User", user_prompt))
        with st.chat_message("user"):
            st.markdown(user_prompt)

        context = "\n".join([f"{role}: {msg}" for role, msg in st.session_state.chat_history[page]])
        ai_response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"{context}\nAI:")
        ])
        reply = ai_response.content if hasattr(ai_response, "content") else str(ai_response)
        st.session_state.chat_history[page].append(("AI", reply))
        with st.chat_message("ai"):
            st.markdown(reply)

# Page 3: Workout Plan
elif page == "🏋️ Workout Plan":
    set_background("workout2.webp") 
    st.title("🏋️ Personalized Workout Plan")

    with st.form("workout_form"):
        age = st.number_input("Age", min_value=10, max_value=100)
        fitness_goal = st.selectbox("Fitness Goal", ["Lose Fat", "Build Muscle", "Increase Stamina", "Flexibility"])
        equipment = st.selectbox("Available Equipment", ["None", "Dumbbells", "Resistance Bands", "Full Gym"])
        workout_days = st.slider("Workout Days/Week", min_value=1, max_value=7, value=3)
        submitted = st.form_submit_button("Generate Workout Plan")

    if submitted:
        with st.spinner("Creating workout plan..."):
            prompt = f"""
Create a weekly workout routine for:
- Age: {age}
- Goal: {fitness_goal}
- Equipment: {equipment}
- Days per Week: {workout_days}

Include exercises, reps, and rest days.
            """
            response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
            st.markdown(response.content)
            st.session_state.chat_history[page].append(("AI", response.content))

    st.subheader("💬 Chat with your Fitness Coach")
    for role, msg in st.session_state.chat_history[page]:
        with st.chat_message(role.lower()):
            st.markdown(msg)

    user_prompt = st.chat_input("Ask about fitness or routines...")
    if user_prompt:
        st.session_state.chat_history[page].append(("User", user_prompt))
        with st.chat_message("user"):
            st.markdown(user_prompt)

        context = "\n".join([f"{role}: {msg}" for role, msg in st.session_state.chat_history[page]])
        ai_response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"{context}\nAI:")
        ])
        reply = ai_response.content if hasattr(ai_response, "content") else str(ai_response)
        st.session_state.chat_history[page].append(("AI", reply))
        with st.chat_message("ai"):
            st.markdown(reply)

# Page 4: Food Analyzer
elif page == "📸 Food Image Analyzer":
    #set_background("food.jpg") 
    st.title("📸 Food Image Analyzer")

    uploaded_file = st.file_uploader("Upload a Food Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image",width=500)
        image = Image.open(uploaded_file).convert("RGB")

        if st.button("🔍 Analyze Food"):
            with st.spinner("Analyzing with vision model..."):
                inputs = processor(images=image, return_tensors="pt")
                output_ids = blip_model.generate(**inputs)
                caption = processor.decode(output_ids[0], skip_special_tokens=True)
                st.success(f"📝 Caption: {caption}")

            with st.spinner("Analyzing food nutrition with LLM..."):
                query = f"""
Based on this image description: "{caption}"

Please provide:
1. Likely dish name or cuisine
2. Estimated calories
3. Common ingredients
4. Health suggestions if any

Use bullet points.
                """
                response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=query)])
                final_text = response.content if hasattr(response, "content") else str(response)
                st.subheader("🍽️ AI Analysis")
                st.markdown(final_text)
                st.session_state.chat_history[page].append(("AI", final_text))

    st.subheader("💬 Chat with AI about your food image")
    for role, msg in st.session_state.chat_history[page]:
        with st.chat_message(role.lower()):
            st.markdown(msg)

    user_prompt = st.chat_input("Ask questions about the food or nutrition...")
    if user_prompt:
        st.session_state.chat_history[page].append(("User", user_prompt))
        with st.chat_message("user"):
            st.markdown(user_prompt)

        context = "\n".join([f"{role}: {msg}" for role, msg in st.session_state.chat_history[page]])
        ai_response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"{context}\nAI:")
        ])
        reply = ai_response.content if hasattr(ai_response, "content") else str(ai_response)
        st.session_state.chat_history[page].append(("AI", reply))
        with st.chat_message("ai"):
            st.markdown(reply)

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='display: block; text-align: center;' href="https://www.linkedin.com/in/abdul-aziz-md/" target="_blank">Abdul Aziz Md</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
