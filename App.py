import streamlit as st
import time
from datetime import date, timedelta

# --- App Configuration ---
st.set_page_config(
    page_title="Your Personal Fitness Coach",
    page_icon="✨",
    layout="wide"
)

# --- Custom Styling (CSS) ---
st.markdown("""
<style>
    /* Main background and font */
    .stApp {
        background-color: #000000; /* Set background to black */
        font-family: 'Poppins', sans-serif;
        color: #FFFFFF; /* Set default text to white */
    }
    
    /* Title style */
    h1 {
        color: #FF6F00; /* A vibrant orange for the main title */
        font-weight: 700;
    }

    /* Subheader style */
    h2, h3 {
        color: #00BCD4; /* A lighter, vibrant teal for headers on dark background */
    }

    /* Custom styled boxes for recommendations */
    .custom-box {
        background-color: #272727; /* Dark grey for a subtle contrast */
        border-left: 10px solid #FFC107; /* A cheerful yellow accent */
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .custom-box p {
        font-size: 1.1rem; /* Slightly larger font size for readability */
        color: #FFFFFF; /* Changed to white */
    }
    .custom-box ul {
        font-size: 1.1rem;
        color: #FFFFFF; /* Changed to white */
    }
    .custom-box h4 {
        color: #FFC107; /* Match the yellow accent for sub-titles inside boxes */
    }

    /* Button style */
    .stButton>button {
        background-color: #FF6F00;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        font-size: 1.2rem;
        font-weight: bold;
        border: none;
    }
</style>
""", unsafe_allow_html=True)


# --- State Management ---
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "name": "", "weight": 0.0, "height": 0.0, "diet": "Vegetarian",
        "living_situation": "With Family", "gender": "Female",
        "age": 0, "waist": 0
    }
if 'metrics' not in st.session_state:
    st.session_state.metrics = {}


# --- Helper Functions for Health Calculations ---
def calculate_bmi(w, h): return round(w / ((h / 100) ** 2), 1) if h > 0 else 0
def classify_bmi(bmi):
    if bmi < 18.5: return "Underweight"
    if 18.5 <= bmi <= 24.9: return "Healthy Weight"
    if 25.0 <= bmi <= 29.9: return "Overweight"
    return "Obese"

# --- Advanced Metric Functions ---
def calculate_bsa(w, h): return round(0.007184 * (w ** 0.425) * (h ** 0.725), 2) if w > 0 and h > 0 else 0
def calculate_pi(w, h): return round(w / ((h/100) ** 3), 1) if h > 0 else 0
def calculate_bmr(w, h, age, gender):
    if w <= 0 or h <= 0 or age <= 0: return 0
    if gender == "Male": return round(10 * w + 6.25 * h - 5 * age + 5)
    return round(10 * w + 6.25 * h - 5 * age - 161)
def calculate_ibw(h, gender):
    h_inches = h * 0.393701
    if h_inches <= 60: return 0
    if gender == "Male": return round(52 + 1.9 * (h_inches - 60))
    return round(49 + 1.7 * (h_inches - 60))
def calculate_whtr(waist, h): return round(waist / h, 2) if waist > 0 and h > 0 else 0


# --- Content Generation Functions ---
def get_diet_recommendations(category, diet_type, living_situation, name):
    title = f"<h3>🥗 Hey {name}, I hope you're having a great day! Let's talk food.</h3>"
    image_url = "https://placehold.co/800x300/272727/FFFFFF?text=Healthy+Indian+Thali"
    content = f"<img src='{image_url}' style='border-radius: 10px; margin-bottom: 20px; width: 100%;'>"
    
    base_info = f"""
    <div class="custom-box">
    <p>Based on your <b>{category}</b> status, here are some simple, balanced meal ideas that fit your <b>{diet_type}</b> preference. Think of this as a friendly guide, not a strict rulebook. The goal is to build a healthy relationship with food!</p>
    <h4>🌟 Golden Rules of Mindful Eating:</h4>
    <ul>
        <li><b>Stay Hydrated:</b> Aim for 2-3 litres of water daily. It's the simplest and most effective habit!</li>
        <li><b>Portion Smarts:</b> Use a smaller plate. When eating a thali, fill half your plate with vegetables/salad, a quarter with dal/protein, and a quarter with rice/roti.</li>
        <li><b>Eat Slowly:</b> Savor each bite. It takes 20 minutes for your brain to register fullness.</li>
        <li><b>Smart Snacking:</b> For mid-meal hunger, grab a fruit, a handful of chana, or a bowl of dahi.</li>
    </ul>
    </div>
    """
    
    specific_advice = ""
    if category in ["Overweight", "Obese"]:
        specific_advice = """
        <h4>🎯 Your Focus: Nutrient-Dense Foods</h4>
        <p>We want foods that are high in nutrients but moderate in calories.</p>
        """
        if diet_type == "Vegetarian":
            specific_advice += "<ul><li><b>Breakfast:</b> Oats upma, moong dal chilla, or poha with lots of veggies.</li><li><b>Lunch:</b> 2 multigrain rotis, a large bowl of dal, sabzi, and a big salad.</li><li><b>Dinner:</b> Keep it light! Vegetable khichdi, paneer bhurji, or a large bowl of lentil soup (dal).</li></ul>"
        elif diet_type == "Eggetarian":
            specific_advice += "<ul><li><b>Breakfast:</b> 2 boiled eggs or a simple egg bhurji with less oil.</li><li><b>Lunch:</b> Add boiled eggs to your veg thali for a protein boost.</li><li><b>Dinner:</b> A simple egg curry with 1-2 rotis.</li></ul>"
        else:  # Non-Vegetarian
            specific_advice += "<ul><li><b>Breakfast:</b> Egg bhurji or 2 boiled eggs.</li><li><b>Lunch:</b> 100g grilled chicken/fish with a large salad and a small portion of brown rice or one roti.</li><li><b>Dinner:</b> Homestyle chicken/fish curry (thin gravy) with lots of veggies.</li></ul>"

    elif category == "Underweight":
        specific_advice = """
        <h4>🎯 Your Focus: Healthy & Sustainable Weight Gain</h4>
        <p>Our goal is to nourish your body with calorie-dense and nutrient-rich foods to build strength and stamina in a healthy way.</p>
        """
        if diet_type == "Vegetarian":
            specific_advice += """
            <ul>
                <li><b>Breakfast:</b> A bowl of dalia or oats cooked in milk with nuts and seeds. Or, 2 paneer-stuffed parathas with dahi.</li>
                <li><b>Lunch:</b> A full thali with 2 rotis (with ghee), a generous serving of rice, dal, sabzi, and a side of paneer or tofu curry.</li>
                <li><b>Dinner:</b> Khichdi made with extra ghee, or rajma/chana masala with rice. A glass of warm milk before bed is a great addition.</li>
                <li><b>Snacks:</b> Peanut butter with apple slices, a handful of almonds/walnuts, or a banana shake.</li>
            </ul>
            """
        elif diet_type == "Eggetarian":
            specific_advice += """
            <ul>
                <li><b>Breakfast:</b> A 3-egg omelette with cheese and vegetables, served with 2 slices of whole wheat toast.</li>
                <li><b>Lunch:</b> Add 2-3 boiled eggs to your standard vegetarian thali for an easy protein and calorie boost.</li>
                <li><b>Dinner:</b> Egg curry with rice or roti, along with a hearty sabzi.</li>
            </ul>
            """
        else:  # Non-Vegetarian
            specific_advice += """
            <ul>
                <li><b>Breakfast:</b> 3-egg omelette or scrambled eggs with chicken sausages.</li>
                <li><b>Lunch:</b> A generous portion of chicken or fish curry with rice, dal, and sabzi. Don't skip the carbs!</li>
                <li><b>Dinner:</b> Grilled chicken/fish (150g) with roasted sweet potatoes and vegetables.</li>
            </ul>
            """
    
    else: # Healthy Weight
        specific_advice = "<h4>🎯 Your Focus: Maintenance & Vitality</h4><p>You're doing great! Let's focus on maintaining this balance with variety and whole foods.</p><ul><li>Ensure a good mix of protein (dal, paneer, eggs, chicken), complex carbs (roti, brown rice), and colorful vegetables.</li></ul>"

    living_advice = ""
    if living_situation == "I cook for myself":
        living_advice = "<h4>💡 Tip for You:</h4><p>One-pot meals are your best friend! Think vegetable pulao, dal khichdi, or a quick paneer/chicken stir-fry. Easy, quick, and nutritious.</p>"
    elif living_situation == "I live in a PG/Hostel":
        living_advice = "<h4>💡 Making Smart Choices in the Mess:</h4><p>You can still eat healthy!<ul><li>Always take the salad if it's available.</li><li>Ask for an extra serving of dal and sabzi instead of a second helping of rice or puri.</li><li>Avoid fried items like pakoras or papad when you can.</li><li>Drink a glass of water before your meal to control your appetite.</li></ul></p>"
    else: # I live with family
        living_advice = "<h4>💡 Eating with Family:</h4><p>No need for a separate meal! Just adjust your portions. Take a larger serving of sabzi and dal, and a smaller one of rice or roti. You're still sharing the meal and love, just in a way that serves your goals.</p>"

    return f"{title}{content}{base_info}<div class='custom-box'>{specific_advice}{living_advice}</div>"


def get_workout_recommendations(category, name):
    title = f"<h3>🏃‍♀️ {name}, Let's Get Moving and Feel Amazing!</h3>"
    image_url = "https://placehold.co/800x300/272727/FFFFFF?text=Start+Your+Fitness+Journey"
    content = f"<img src='{image_url}' style='border-radius: 10px; margin-bottom: 20px; width: 100%;'>"
    
    workout_plan = ""
    if category in ["Overweight", "Obese"]:
        workout_plan = """
        <h4>Your Goal: Build Consistency & Joyful Movement</h4>
        <ul>
            <li><b>Week 1: The Foundation.</b> Let's begin with a 30-minute brisk walk every day. Put on some music, listen to a podcast, and enjoy this time for yourself!</li>
            <li><b>Week 2: Building Stamina.</b> Increase your walk to 45 minutes. Focus on your breathing. You're building a powerful habit!</li>
            <li><b>Week 3: Adding Strength.</b> After your walk, let's add 2 sets of 10 simple squats and 10 wall push-ups. This will start building muscle, which boosts metabolism.</li>
            <li><b>Beyond:</b> We'll slowly increase the duration and add more fun exercises. The goal is to find movement you love!</li>
        </ul>
        """
    else:
        workout_plan = """
        <h4>Your Goal: Maintain Fitness & Build Strength</h4>
        <ul>
            <li><b>Your Routine:</b> Aim for 3-5 days of activity per week. A mix of cardio (walking, jogging, cycling) and strength training (yoga, bodyweight exercises) is ideal.</li>
            <li><b>Try Something New:</b> Explore online dance workouts, try Surya Namaskar for flexibility, or find a sport you enjoy. Keeping it fun is the key to consistency.</li>
        </ul>
        """
    return f"{title}{content}<div class='custom-box'>{workout_plan}</div>"

def get_habit_and_confidence_tips(name):
    title = f"<h3>💡 Hey {name}, Let's Build Habits for a Confident You!</h3>"
    content = f"""
    <h4>Small Steps, Giant Leaps</h4>
    <ul>
        <li><b>The 80/20 Rule:</b> Eat healthy 80% of the time, and allow yourself treats 20% of the time. This isn't about restriction; it's about balance.</li>
        <li><b>Listen to Your Body:</b> Eat when you're hungry, stop when you're satisfied (not stuffed). Your body is incredibly smart!</li>
        <li><b>Healthy Swaps:</b> Switch to whole wheat roti, use jaggery instead of sugar, and opt for baked/roasted snacks over fried ones.</li>
    </ul>
    <h4>💖 Building Unshakable Confidence:</h4>
    <ul>
        <li><b>Celebrate Non-Scale Victories:</b> Did your clothes fit better? Did you have more energy? Did you walk further than last week? Celebrate these wins! They matter more than the number on the scale.</li>
        <li><b>Positive Self-Talk:</b> Speak to yourself like you would a dear friend. Instead of "I have to work out," try "I get to move my body and feel strong."</li>
        <li><b>You Are More Than a Number:</b> Your weight does not define your worth. This journey is about health, strength, and feeling good in your own skin. You are already amazing, and you've got this!</li>
    </ul>
    """
    return f"{title}<div class='custom-box'>{content}</div>"
    
def get_gender_specific_tips(gender, name):
    title = f"<h3>🌟 Personalized Insights Just for You, {name}</h3>"
    content = ""
    if gender == "Female":
        content = """<h4>Health Focus for Women:</h4><ul><li><b>Iron & Calcium are Key:</b> Ensure your diet is rich in iron (spinach, lentils, beans) and calcium (dairy, ragi, sesame seeds) for bone health and energy levels.</li><li><b>Hormonal Harmony:</b> Regular exercise and a balanced diet can significantly help with managing PMS and maintaining hormonal balance.</li><li><b>Stress & Weight:</b> For many women, stress can lead to weight gain, especially around the midsection. Our stress management tips are extra important for you!</li></ul>"""
    elif gender == "Male":
        content = """<h4>Health Focus for Men:</h4><ul><li><b>Protein for Muscle:</b> To build and maintain muscle mass, ensure adequate protein intake from sources like dal, paneer, eggs, or lean meats with every meal.</li><li><b>Heart Health:</b> Focus on a diet low in unhealthy fats and high in fiber (vegetables, whole grains) to keep your heart strong.</li><li><b>Mind the Belly:</b> For many men, excess weight tends to accumulate around the abdomen. Consistent cardio and a clean diet are the best tools to manage this.</li></ul>"""
    else:
        content = """<h4>A Holistic Approach to Your Health:</h4><ul><li><b>Listen to Your Body:</b> Your body gives you unique signals. Pay attention to your energy levels, sleep quality, and mood. These are your best indicators of health.</li><li><b>Balanced Nutrition is Universal:</b> A diet rich in a variety of whole foods—vegetables, proteins, healthy fats, and complex carbs—is the foundation of good health for everyone.</li><li><b>Consistency is Your Power:</b> Building a routine that you can stick with is more important than any single diet or workout.</li></ul>"""
    return f"{title}<div class='custom-box'>{content}</div>"

def get_stress_management_tips(name):
    title = f"<h3>🧘‍♀️ {name}, Let's Talk About Stress & Wellness</h3>"
    image_url = "https://placehold.co/800x300/272727/FFFFFF?text=Find+Your+Calm"
    content = f"<img src='{image_url}' style='border-radius: 10px; margin-bottom: 20px; width: 100%;'>"
    tips = """<p>Stress is a normal part of life, but managing it is crucial for your health. High stress can lead to poor food choices and impact your goals.</p><h4>Simple Techniques to Find Your Calm:</h4><ul><li><b>5-Minute Breathing:</b> When feeling overwhelmed, sit quietly and focus on your breath. Inhale for 4 seconds, hold for 4, and exhale for 6. Repeat for 5 minutes.</li><li><b>Digital Detox:</b> Try to set aside 30 minutes every day where you put your phone away. Go for a walk, listen to music, or just sit with your thoughts.</li><li><b>Schedule 'Me-Time':</b> Just like a meeting, block out time in your calendar for a hobby or activity you love. It's non-negotiable!</li><li><b>Get Quality Sleep:</b> Aim for 7-8 hours of sleep. A well-rested mind is a less-stressed mind.</li></ul>"""
    return f"{title}{content}<div class='custom-box'>{tips}</div>"
    
def get_20_day_plan(name, category, weight):
    today = date.today()
    end_date = today + timedelta(days=20)
    target_weight = weight
    if category == "Overweight": target_weight -= 1.5
    elif category == "Obese": target_weight -= 2.0
    elif category == "Underweight": target_weight += 1.0
        
    title = f"<h3>🎯 Your 20-Day Kickstart Plan, {name}!</h3>"
    chart_url = f"https://placehold.co/800x200/272727/00BCD4?text=Your+Journey:+Day+1+to+Day+20"
    content = f"<img src='{chart_url}' style='border-radius: 10px; margin-bottom: 20px; width: 100%;'>"

    plan_details = f"""
    <p>Today is <b>{today.strftime('%B %d, %Y')}</b>. Let's start a 20-day challenge to build momentum! Consistency is more powerful than intensity. Your projected target is to reach <b>{target_weight:.1f} kg</b> by <b>{end_date.strftime('%B %d, %Y')}</b>.</p>
    <h4>Your Daily Mini-Goals:</h4>
    <ul>
        <li><b>Movement:</b> Complete your recommended walk or activity.</li>
        <li><b>Hydration:</b> Drink at least 8 glasses of water.</li>
        <li><b>Mindful Meal:</b> For at least one meal, eat slowly without distractions.</li>
        <li><b>Reflection:</b> Before bed, think of one healthy choice you made today that made you feel good.</li>
    </ul>
    <p>That's it! Small, achievable steps. You can absolutely do this. Let's check in after 20 days and see the amazing progress you've made!</p>
    """
    return f"{title}{content}<div class='custom-box'>{plan_details}</div>"

def get_india_snapshot():
    st.markdown("<h3>🇮🇳 India's Health Snapshot: You're Part of a National Movement!</h3>", unsafe_allow_html=True)
    
    # This block uses st.markdown for each part to ensure proper rendering.
    with st.container():
        st.markdown("""
        <div class="custom-box">
            <p>Your decision to focus on your health is incredibly important. You're joining millions of Indians working towards a healthier future. Here's a look at the bigger picture:</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-box">
            <h4>🤔 Do you know? The Definitions Matter!</h4>
            <ul>
                <li><b>What is Obesity?</b> According to the WHO, it's an abnormal or excessive fat accumulation that presents a risk to health. A BMI of 30+ is globally considered obese.</li>
                <li><b>The Indian Context:</b> For the Indian population, the classifications are adjusted. A person is considered <b>overweight</b> if their BMI is between <b>23.0 and 24.9</b>, and <b>obese</b> if their BMI is <b>25 or higher</b>.</li>
                <li><b>What is BMI?</b> Body Mass Index is a simple check for healthy weight. It's your weight (kg) divided by the square of your height (m). A healthy BMI range is generally <b>18.5 to 24.9</b>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="custom-box">
            <h4>📈 The Bigger Picture: National & Global Trends</h4>
        </div>
        """, unsafe_allow_html=True)


    # Key Statistics using Streamlit's metric component for a nice visual
    kpi_cols = st.columns(3)
    kpi_cols[0].metric(label="Overweight Women (NFHS-5)", value="24%")
    kpi_cols[1].metric(label="Overweight Men (NFHS-5)", value="23%")
    kpi_cols[2].metric(label="Overweight Children <5yrs", value="3.4%", delta="up from 2.1% in 2015-16")

    st.markdown("""
    <div class="custom-box" style="margin-top: 20px;">
        <ul>
            <li>Globally, adult obesity (BMI > 30) has more than doubled since 1990, rising from <b>7% to 16%</b>.</li>
            <li>In India (ages 15-49), <b>6.4% of women</b> and <b>4.0% of men</b> are classified as obese.</li>
        </ul>
        <p style="font-size: 0.9rem; text-align: right; margin-top: 15px;">
            Source: <a href="https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2107179" target="_blank" style="color: #00BCD4;">Press Information Bureau (Govt. of India)</a>
        </p>
    </div>
    <p style='margin-top: 20px;'><b>Your small, consistent steps contribute to changing these statistics for the better. Every walk, every healthy meal, every glass of water—it all counts!</b></p>
    """, unsafe_allow_html=True)


# --- The App UI ---
st.title("✨ Welcome to Your Personal Wellness Coach!")
st.image("https://placehold.co/1200x300/000000/FF6F00?text=Your+Health+Journey+Starts+Now", use_container_width=True)
st.markdown("<h3>I'm here to guide you on your journey to a healthier, more confident you. Let's do this together!</h3>", unsafe_allow_html=True)

# --- Step 0: Collect User Info ---
if st.session_state.step == 0:
    with st.form("user_info_form"):
        st.header("First, Tell Me a Bit About Yourself")
        name = st.text_input("What is your name?", placeholder="e.g., Priya Sharma")
        gender = st.selectbox("What is your gender?", ("Female", "Male", "Prefer not to say / Other"))
        
        # Basic Info
        weight = st.number_input("Weight (kg)", 30.0, 200.0, 65.0, 0.5)
        height = st.number_input("Height (in cm)", 100.0, 250.0, 165.0, 1.0)
        diet = st.selectbox("Dietary preference?", ("Vegetarian", "Eggetarian", "Non-Vegetarian"))
        living_situation = st.selectbox("How do you manage meals?", ("I live with family", "I cook for myself", "I live in a PG/Hostel"))
        
        # Optional Advanced Info
        with st.expander("Optional: Add more details for a deeper analysis"):
            age = st.number_input("Your Age", 0, 100, 25)
            waist = st.number_input("Waist Circumference (in cm)", 0, 200, 80)

        submitted = st.form_submit_button("Preview My Plan!")
        if submitted:
            if not name: st.error("Please enter your name.")
            else:
                st.session_state.user_data = {
                    "name": name, "weight": weight, "height": height, "diet": diet,
                    "living_situation": living_situation, "gender": gender,
                    "age": age, "waist": waist
                }
                st.session_state.step = 1
                st.rerun()

# --- Step 1: Preview and Confirmation ---
elif st.session_state.step == 1:
    user = st.session_state.user_data
    w, h, age, gender, waist = user['weight'], user['height'], user['age'], user['gender'], user['waist']
    
    # Calculate all metrics
    bmi = calculate_bmi(w, h)
    bmi_category = classify_bmi(bmi)
    st.session_state.metrics = {
        'bmi': bmi, 'bmi_category': bmi_category,
        'bsa': calculate_bsa(w, h),
        'pi': calculate_pi(w, h),
        'bmr': calculate_bmr(w, h, age, gender),
        'ibw': calculate_ibw(h, gender),
        'whtr': calculate_whtr(waist, h)
    }
    metrics = st.session_state.metrics
    name = user['name'].split(" ")[0]

    with st.spinner(f'Analyzing your details, {name}...'): time.sleep(1)
    st.header(f"Alright {name}, Here's Your Personalized Health Snapshot!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Your BMI Analysis")
        st.metric("Body Mass Index (BMI)", metrics['bmi'])
        st.write(f"This places you in the **'{metrics['bmi_category']}'** category.")
    with col2:
        st.subheader("My Message to You")
        if metrics['bmi_category'] == "Healthy Weight": st.success(f"This is fantastic, {name}! You're in a great place. Let's help you feel strong and energized.")
        else: st.warning(f"Thank you for sharing, {name}. This is just a starting point for an amazing journey of self-care. I'm here with you!")

    # Display Advanced Metrics only if the required data was provided
    if user['age'] > 0 or user['waist'] > 0:
        st.subheader("Deeper Health Insights")
        adv_cols = st.columns(3)
        if metrics['bsa'] > 0: adv_cols[0].metric("Body Surface Area (BSA)", f"{metrics['bsa']} m²", help="An indicator of your metabolic mass.")
        if metrics['bmr'] > 0: adv_cols[1].metric("Basal Metabolic Rate (BMR)", f"{metrics['bmr']} kcal/day", help="Calories your body burns at rest. Useful for diet planning.")
        if metrics['ibw'] > 0: adv_cols[2].metric("Ideal Body Weight (IBW)", f"{metrics['ibw']} kg", help="An estimated healthy weight for your height.")
        if metrics['whtr'] > 0:
            adv_cols[0].metric("Waist-to-Height Ratio", metrics['whtr'], help="A ratio < 0.5 is ideal for heart health.")
            if metrics['whtr'] >= 0.5: st.warning("Your WHtR is slightly high. Focusing on core exercises and a balanced diet can help improve this.")
            else: st.success("Your WHtR is in a healthy range. Great job!")

    st.info("When you're ready, unlock your full, personalized action plan below.")
    if st.button("Unlock My Full Personalized Plan"):
        st.session_state.step = 2
        st.rerun()
    if st.button("Start Over", key="so_preview"):
        st.session_state.clear()
        st.rerun()

# --- Step 2: The Full Plan ---
elif st.session_state.step == 2:
    user = st.session_state.user_data
    metrics = st.session_state.metrics
    name = user['name'].split(" ")[0]
    
    st.header(f"Your Action Plan for a Healthier, More Confident You!")
    
    tabs = st.tabs(["🎯 Your 20-Day Goal", "🥗 Diet Plan", "🏃‍♀️ Workout Plan", "💡 Habits & Confidence", "🇮🇳 India Health Snapshot", "🌟 Personalized Insights", "🧘‍♀️ Stress & Wellness"])
    with tabs[0]: st.markdown(get_20_day_plan(name, metrics['bmi_category'], user['weight']), unsafe_allow_html=True)
    with tabs[1]: st.markdown(get_diet_recommendations(metrics['bmi_category'], user['diet'], user['living_situation'], name), unsafe_allow_html=True)
    with tabs[2]: st.markdown(get_workout_recommendations(metrics['bmi_category'], name), unsafe_allow_html=True)
    with tabs[3]: st.markdown(get_habit_and_confidence_tips(name), unsafe_allow_html=True)
    with tabs[4]: get_india_snapshot()
    with tabs[5]: st.markdown(get_gender_specific_tips(user['gender'], name), unsafe_allow_html=True)
    with tabs[6]: st.markdown(get_stress_management_tips(name), unsafe_allow_html=True)

    st.divider()
    st.subheader("🔔 Motivational Reminders")
    if st.toggle("Enable motivational notifications"):
        st.success("Awesome! I'll be your cheerleader. Imagine getting friendly nudges like these:")
        st.info(f"Hey {name}, have you had a glass of water yet? Stay hydrated! 💧")
        st.info(f"You're doing great, {name}! Just a quick reminder that you are strong and capable. Keep going! 💪")

    if st.button("Start Over"):
        st.session_state.clear()
        st.rerun()
