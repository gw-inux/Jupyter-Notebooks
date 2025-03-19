# -*- coding: utf-8 -*-
import streamlit as st
from fpdf import FPDF

# App title
st.title("How to Prepare a Delicious Pizza")

# Introduction
st.write("Follow these simple steps to make a homemade pizza from scratch!")

# Pizza selection
st.header("Choose Your Pizza Type")
pizza_choice = st.radio(
    "Which pizza do you want to make?",
    ("Margherita", "Capricciosa", "Vegetariana", "Quattro Formaggi", "Hawaii")
)

# Ingredients based on selection
if pizza_choice == "Margherita":
    ingredients = [
        "2 1/2 cups all-purpose flour",
        "1 packet (2 1/4 tsp) instant yeast",
        "1 tsp salt",
        "1 cup warm water",
        "1 tbsp olive oil",
        "1/2 cup tomato sauce",
        "1 1/2 cups shredded mozzarella cheese",
        "Fresh basil leaves"
    ]
    image_url = "https://upload.wikimedia.org/wikipedia/commons/d/d3/Supreme_pizza.jpg"

elif pizza_choice == "Capricciosa":
    ingredients = [
        "2 1/2 cups all-purpose flour",
        "1 packet (2 1/4 tsp) instant yeast",
        "1 tsp salt",
        "1 cup warm water",
        "1 tbsp olive oil",
        "1/2 cup tomato sauce",
        "1 1/2 cups shredded mozzarella cheese",
        "Artichokes",
        "Ham",
        "Mushrooms",
        "Black olives"
    ]
    image_url = "https://upload.wikimedia.org/wikipedia/commons/d/d3/Supreme_pizza.jpg"

elif pizza_choice == "Vegetariana":
    ingredients = [
        "2 1/2 cups all-purpose flour",
        "1 packet (2 1/4 tsp) instant yeast",
        "1 tsp salt",
        "1 cup warm water",
        "1 tbsp olive oil",
        "1/2 cup tomato sauce",
        "1 1/2 cups shredded mozzarella cheese",
        "Bell peppers",
        "Zucchini",
        "Eggplant",
        "Cherry tomatoes",
        "Red onions"
    ]
    image_url = "https://upload.wikimedia.org/wikipedia/commons/d/d3/Supreme_pizza.jpg"

elif pizza_choice == "Quattro Formaggi":
    ingredients = [
        "2 1/2 cups all-purpose flour",
        "1 packet (2 1/4 tsp) instant yeast",
        "1 tsp salt",
        "1 cup warm water",
        "1 tbsp olive oil",
        "1/2 cup tomato sauce",
        "1 1/2 cups shredded mozzarella cheese",
        "Gorgonzola",
        "Parmesan",
        "Fontina"
    ]
    image_url = "https://upload.wikimedia.org/wikipedia/commons/d/d3/Supreme_pizza.jpg"

elif pizza_choice == "Hawaii":
    st.markdown("### :red[**Warning**:]")
    st.markdown("### 🚨 **You are about to enter forbidden territory!** 🚨")
    st.markdown("🔥 **Pineapple on pizza... truly a path of no return.** 🔥👹")

    confirm = st.checkbox("I accept my fate and will proceed 🍍🔥")
    
    if confirm:
        ingredients = [
            "2 1/2 cups all-purpose flour",
            "1 packet (2 1/4 tsp) instant yeast",
            "1 tsp salt",
            "1 cup warm water",
            "1 tbsp olive oil",
            "1/2 cup tomato sauce",
            "1 1/2 cups shredded mozzarella cheese",
            "Ham",
            ":red[NO NO NO] Pineapple :red-background[DONT EVEN THINK ABOUT IT!!!]"
        ]
        # 🔥 Special "Hawaii from Hell" image
        image_url = "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzNtYjM1c24xNmFsYXg5OXUxZ2p2Z2NkZW5keGRjanc5bmc4dzZ3MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QjnNaD7viJrWALeWA9/giphy.gif" 
    else:
        st.stop()

st.header("Ingredients")
st.write("\n".join([f"- {item}" for item in ingredients]))

# Steps to prepare pizza
st.header("Steps to Prepare Pizza")

steps = [
    "1. **Prepare the dough**: Mix flour, yeast, salt, warm water, and olive oil. Knead until smooth.",
    "2. **Let the dough rise**: Cover and let it rest for about an hour until it doubles in size.",
    "3. **Preheat the oven**: Set it to 475 F (245 C).",
    "4. **Roll out the dough**: Flatten the dough on a floured surface and shape it into a round pizza base.",
    "5. **Add toppings**: Spread tomato sauce, sprinkle cheese, and add your selected toppings.",
    "6. **Bake the pizza**: Place it in the oven and bake for 12-15 minutes until golden brown.",
    "7. **Enjoy!** Slice and serve your homemade pizza. 🍕"
]

for step in steps:
    st.write(step)

# Add an image (special for Hawaii 🍍🔥)
st.image(image_url, caption="Your chosen pizza!")

# Function to generate PDF
def generate_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, f"Grocery List for {pizza_choice} Pizza", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for item in ingredients:
        pdf.cell(0, 10, f"- {item}", ln=True)
    return pdf.output(dest="S").encode("utf-8")

# Button to download PDF
st.header("Download Grocery List")
pdf_data = generate_pdf()
st.download_button(label="Click to Download", data=pdf_data, file_name=f"{pizza_choice.lower()}_grocery_list.pdf", mime="application/pdf")

st.write("Hope you enjoy making your homemade pizza! 🍕")
