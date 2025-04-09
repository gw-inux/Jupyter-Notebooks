import streamlit as st

Start = st.Page(
    "pages/Start/start.py", title="Welcome", icon=":material/dashboard:", default=True
)
    
welcome = st.Page("pages/Start/welcome.py", title="Welcome", icon=":material/bug_report:")
content = st.Page("pages/Start/content.py", title="Content", icon=":material/bug_report:")

Section1 = st.Page(
    "pages/Section_1/section1.py", title="Section 1", icon=":material/dashboard:", default=True
)

bucket_steady_homo   = st.Page("pages/Section_1/bucket_steady_homo.py",   title="Bucket with heads in steady state - homogene",   icon=":material/bug_report:")
bucket_steady_hetero = st.Page("pages/Section_1/bucket_steady_hetero.py", title="Bucket with heads in steady state - heterogene", icon=":material/bug_report:")

Section2 = st.Page(
    "pages/Section_2/section2.py", title="Section 2", icon=":material/dashboard:", default=True
)

bucket_transient_a = st.Page("pages/Section_2/bucket_transient_a.py", title="Bucket with heads in transient - A", icon=":material/bug_report:")
bucket_transient_b = st.Page("pages/Section_2/bucket_transient_b.py", title="Bucket with heads in transient - B", icon=":material/bug_report:")

Section3 = st.Page(
    "pages/Section_3/section3.py", title="Section 3", icon=":material/dashboard:", default=True
)

section3proxy = st.Page("pages/Section_3/section3proxy.py", title="Section 3 topic", icon=":material/bug_report:")

Section4 = st.Page(
    "pages/Section_4/section4.py", title="Section 4", icon=":material/dashboard:", default=True
)

Transport_1D_A = st.Page("pages/Section_4/Transport_1D_A.py", title="Transport 1D A", icon=":material/bug_report:")
Transport_1D_AD = st.Page("pages/Section_4/Transport_1D_AD.py", title="Transport 1D AD", icon=":material/bug_report:")
Transport_1D_ADR = st.Page("pages/Section_4/Transport_1D_ADR.py", title="Transport 1D ADR", icon=":material/bug_report:")
Transport_1D_ADRD = st.Page("pages/Section_4/Transport_1D_ADRD.py", title="Transport 1D ADRD", icon=":material/bug_report:")

Section5 = st.Page(
    "pages/Section_5/section5.py", title="Section 5", icon=":material/dashboard:", default=True
)

section5proxy = st.Page("pages/Section_5/section5proxy.py", title="Section 5 topic", icon=":material/bug_report:")

Section6 = st.Page(
    "pages/Section_6/section6.py", title="Section 6", icon=":material/dashboard:", default=True
)

section6proxy = st.Page("pages/Section_6/section6proxy.py", title="Section 6 topic", icon=":material/bug_report:")

Section7 = st.Page(
    "pages/Section_7/section7.py", title="Section 7", icon=":material/dashboard:", default=True
)

section7proxy = st.Page("pages/Section_7/section7proxy.py", title="Section 7 topic", icon=":material/bug_report:")

Section8 = st.Page(
    "pages/Section_8/section8.py", title="Section 8", icon=":material/dashboard:", default=True
)

section8proxy = st.Page("pages/Section_8/section8proxy.py", title="Section 8 topic", icon=":material/bug_report:")

Section9 = st.Page(
    "pages/Section_9/section9.py", title="Section 9", icon=":material/dashboard:", default=True
)

section9proxy = st.Page("pages/Section_9/section9proxy.py", title="Section 9 topic", icon=":material/bug_report:")

Section10 = st.Page(
    "pages/Section_10/section10.py", title="Section 10", icon=":material/dashboard:", default=True
)

section10proxy = st.Page("pages/Section_10/section10proxy.py", title="Section 10 topic", icon=":material/bug_report:")

pg = st.navigation(
        {
            "Start": [welcome,content],
            "Section1": [bucket_steady_homo, bucket_steady_hetero],
            "Section2": [bucket_transient_a, bucket_transient_b],
            "Section3": [section3proxy],
            "Section4": [Transport_1D_A,Transport_1D_AD,Transport_1D_ADR,Transport_1D_ADRD],
            "Section5": [section5proxy],
            "Section6": [section6proxy],
            "Section7": [section7proxy],
            "Section8": [section8proxy],
            "Section9": [section9proxy],
            "Section10": [section10proxy],
        }
    )

pg.run()