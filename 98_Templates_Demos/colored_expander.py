import streamlit as st

# Fixed CSS with proper selectors and removed conflicting rules
st.markdown("""
<style>
/* Remove any conflicting nth-child rules that might override container styles */

/* Green expanders for exercises */
.exercise-style > div > div > details > summary {
    background-color: #c8e6c9 !important;
    border: 2px solid #4CAF50 !important;
    color: #2e7d32 !important;
    font-weight: bold;
    border-radius: 8px 8px 0 0 !important;
    padding: 12px !important;
}

.exercise-style > div > div > details > summary:hover {
    background-color: #a5d6a7 !important;
}

.exercise-style > div > div > details[open] > summary {
    border-radius: 8px 8px 0 0 !important;
}

.exercise-style > div > div > details > div {
    background-color: #e8f5e8 !important;
    border: 2px solid #4CAF50 !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 10px !important;
    margin-top: 0 !important;
}

/* Blue expanders for explanations */
.explanation-style > div > div > details > summary {
    background-color: #bbdefb !important;
    border: 2px solid #2196F3 !important;
    color: #1565c0 !important;
    font-weight: bold;
    border-radius: 8px 8px 0 0 !important;
    padding: 12px !important;
}

.explanation-style > div > div > details > summary:hover {
    background-color: #90caf9 !important;
}

.explanation-style > div > div > details[open] > summary {
    border-radius: 8px 8px 0 0 !important;
}

.explanation-style > div > div > details > div {
    background-color: #e3f2fd !important;
    border: 2px solid #2196F3 !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 10px !important;
    margin-top: 0 !important;
}

/* Red expanders for warnings */
.warning-style > div > div > details > summary {
    background-color: #ffcdd2 !important;
    border: 2px solid #f44336 !important;
    color: #c62828 !important;
    font-weight: bold;
    border-radius: 8px 8px 0 0 !important;
    padding: 12px !important;
}

.warning-style > div > div > details > summary:hover {
    background-color: #ef9a9a !important;
}

.warning-style > div > div > details[open] > summary {
    border-radius: 8px 8px 0 0 !important;
}

.warning-style > div > div > details > div {
    background-color: #ffebee !important;
    border: 2px solid #f44336 !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 10px !important;
    margin-top: 0 !important;
}

/* Purple expanders for tips */
.tip-style > div > div > details > summary {
    background-color: #e1bee7 !important;
    border: 2px solid #9c27b0 !important;
    color: #6a1b9a !important;
    font-weight: bold;
    border-radius: 8px 8px 0 0 !important;
    padding: 12px !important;
}

.tip-style > div > div > details > summary:hover {
    background-color: #ce93d8 !important;
}

.tip-style > div > div > details[open] > summary {
    border-radius: 8px 8px 0 0 !important;
}

.tip-style > div > div > details > div {
    background-color: #f3e5f5 !important;
    border: 2px solid #9c27b0 !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 10px !important;
    margin-top: 0 !important;
}

/* REMOVED THE PROBLEMATIC nth-child SELECTORS THAT WERE CAUSING CONFLICTS */
</style>
""", unsafe_allow_html=True)

st.title("🎨 Fixed Streamlit Colored Expanders")
st.write("This version should show different colors for each expander type.")

# Helper function for easier use
def create_colored_expander(title, style_class):
    """Helper function to create colored expanders"""
    container = st.container()
    with container:
        st.markdown(f'<div class="{style_class}">', unsafe_allow_html=True)
        expander = st.expander(title)
        st.markdown('</div>', unsafe_allow_html=True)
        return expander

st.header("🧪 Testing Different Colors")

# Test each color to verify they work
st.subheader("Green Exercise Expander:")
with st.container():
    st.markdown('<div class="exercise-style">', unsafe_allow_html=True)
    with st.expander("🏃 Exercise: Python Basics (Should be GREEN)"):
        st.write("This expander should have a **green** background.")
        st.success("If you see green styling, this method is working!")
        st.code("print('Hello, Green World!')")
    st.markdown('</div>', unsafe_allow_html=True)

st.subheader("Blue Explanation Expander:")
with st.container():
    st.markdown('<div class="explanation-style">', unsafe_allow_html=True)
    with st.expander("📚 Explanation: Functions (Should be BLUE)"):
        st.write("This expander should have a **blue** background.")
        st.info("If you see blue styling, this method is working!")
        st.code("def hello(): return 'Hello, Blue World!'")
    st.markdown('</div>', unsafe_allow_html=True)

st.subheader("Red Warning Expander:")
with st.container():
    st.markdown('<div class="warning-style">', unsafe_allow_html=True)
    with st.expander("⚠️ Warning: Important Info (Should be RED)"):
        st.write("This expander should have a **red** background.")
        st.error("If you see red styling, this method is working!")
        st.code("# Be careful with this code!")
    st.markdown('</div>', unsafe_allow_html=True)

st.subheader("Purple Tip Expander:")
with st.container():
    st.markdown('<div class="tip-style">', unsafe_allow_html=True)
    with st.expander("💜 Tip: Pro Advice (Should be PURPLE)"):
        st.write("This expander should have a **purple** background.")
        st.write("🔮 If you see purple styling, this method is working!")
        st.code("# Pro tip: Use descriptive variable names")
    st.markdown('</div>', unsafe_allow_html=True)

st.header("🔧 Using Helper Function")
st.write("Here's the same functionality using the helper function:")

# Using helper function
with create_colored_expander("🔬 Helper Function - Exercise", "exercise-style"):
    st.write("This uses the helper function and should be **GREEN**.")
    st.write("The helper function makes it easier to create colored expanders.")

with create_colored_expander("💡 Helper Function - Explanation", "explanation-style"):
    st.write("This uses the helper function and should be **BLUE**.")
    st.write("Helper functions reduce code duplication.")

with create_colored_expander("🚨 Helper Function - Warning", "warning-style"):
    st.write("This uses the helper function and should be **RED**.")
    st.warning("Always test your styling changes!")

with create_colored_expander("✨ Helper Function - Tip", "tip-style"):
    st.write("This uses the helper function and should be **PURPLE**.")
    st.write("Consistent styling improves user experience.")

st.header("🔄 Alternative: Inline HTML Method")
st.write("If the CSS method still doesn't work, use this inline HTML approach:")

# Inline HTML method (most reliable)
st.markdown("""
<details style="
    background-color: #e8f5e8; 
    border: 2px solid #4CAF50; 
    border-radius: 8px; 
    padding: 0;
    margin: 10px 0;
">
<summary style="
    background-color: #c8e6c9; 
    padding: 12px; 
    cursor: pointer; 
    border-radius: 8px 8px 0 0;
    color: #2e7d32;
    font-weight: bold;
">
🌟 Inline HTML - Always Works (GREEN)
</summary>
<div style="padding: 15px; background-color: #e8f5e8;">
<p><strong>This is a manually styled expander using pure HTML!</strong></p>
<p>This approach works regardless of Streamlit version because it uses inline styles.</p>
<p>✅ This should always show as GREEN regardless of CSS issues.</p>
</div>
</details>
""", unsafe_allow_html=True)

st.markdown("""
<details style="
    background-color: #e3f2fd; 
    border: 2px solid #2196F3; 
    border-radius: 8px; 
    padding: 0;
    margin: 10px 0;
">
<summary style="
    background-color: #bbdefb; 
    padding: 12px; 
    cursor: pointer; 
    border-radius: 8px 8px 0 0;
    color: #1565c0;
    font-weight: bold;
">
🔵 Inline HTML - Always Works (BLUE)
</summary>
<div style="padding: 15px; background-color: #e3f2fd;">
<p><strong>This blue expander uses inline HTML styling!</strong></p>
<p>Inline styles have the highest CSS priority and can't be overridden.</p>
<p>✅ This should always show as BLUE regardless of CSS conflicts.</p>
</div>
</details>
""", unsafe_allow_html=True)

st.header("🔍 Troubleshooting")

st.write("**If expanders are still all blue:**")

st.markdown("""
1. **Check Browser Cache**: 
   - Try refreshing the page (Ctrl+F5 or Cmd+Shift+R)
   - Clear browser cache

2. **Inspect CSS**: 
   - Press F12 to open developer tools
   - Look at the expander elements
   - Check if the CSS classes are being applied

3. **Streamlit Version**: 
   - Different Streamlit versions might have different HTML structures
   - Try updating Streamlit: `pip install streamlit --upgrade`

4. **Use Inline HTML**: 
   - If CSS doesn't work, use the inline HTML method above
   - It's more reliable across different versions
""")

st.code(f"Current Streamlit version: {st.__version__}")

st.success("""
**Expected Results:**
- 🟢 Green expanders for exercises
- 🔵 Blue expanders for explanations  
- 🔴 Red expanders for warnings
- 🟣 Purple expanders for tips
- 🌟 Inline HTML examples should always work
""")