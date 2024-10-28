import streamlit as st

Start = st.Page(
    "pages/Start/start.py", title="Welcome", icon=":material/dashboard:", default=True
)
    
welcome = st.Page("pages/Start/welcome.py", title="Welcome", icon=":material/bug_report:")
content = st.Page("pages/Start/content.py", title="Content", icon=":material/bug_report:")

Section1 = st.Page(
    "pages/Topic_1/section1.py", title="Topic 1", icon=":material/dashboard:", default=True
)

topic1proxy   = st.Page("pages/Topic_1/section1proxy.py",   title="Topic1 Proxy",   icon=":material/bug_report:")

Section2 = st.Page(
    "pages/Topic_2/section2.py", title="Section 2", icon=":material/dashboard:", default=True
)

topic2WB1   = st.Page("pages/Topic_2/GWF_1D_unconf_analytic_BC_EX_DE.py",   title="Workbook hydraulische und physikalische Randbedingungen",   icon=":material/bug_report:")

Section3 = st.Page(
    "pages/Topic_3/section3.py", title="Section 3", icon=":material/dashboard:", default=True
)

topic3proxy   = st.Page("pages/Topic_3/section3proxy.py",   title="Topic3 Proxy",   icon=":material/bug_report:")

Section4 = st.Page(
    "pages/Topic_4/section4.py", title="Section 4", icon=":material/dashboard:", default=True
)

topic4proxy   = st.Page("pages/Topic_4/section4proxy.py",   title="Topic4 Proxy",   icon=":material/bug_report:")

Section5 = st.Page(
    "pages/Topic_5/section5.py", title="Section 5", icon=":material/dashboard:", default=True
)

topic5proxy   = st.Page("pages/Topic_5/section5proxy.py",   title="Topic5 Proxy",   icon=":material/bug_report:")

Section6 = st.Page(
    "pages/Topic_6/section6.py", title="Section 6", icon=":material/dashboard:", default=True
)

topic6proxy   = st.Page("pages/Topic_6/section6proxy.py",   title="Topic6 Proxy",   icon=":material/bug_report:")


pg = st.navigation(
        {
            "Start": [welcome,content],
            "Section1": [topic1proxy],
            "Section2": [topic2WB1],
            "Section3": [topic3proxy],
            "Section4": [topic4proxy],
            "Section5": [topic5proxy],
            "Section6": [topic6proxy],
        }
    )

pg.run()