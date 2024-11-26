import streamlit as st

st.title('📃 Theory underlying PumpingTestAnalysis')

st.subheader(':orange-background[The Theis, Neuman, and Hantush Jacob solution]', divider="orange")

st.markdown("""
            ### Introduction
            This interactive app allows to investigate transient flow to a well with the Theis and Neuman solution. Applications involve the pumping test evaluation in confined and unconfined, transient setups. The computation is based on an Spreadsheet from Prof. Rudolf Liedl.
            
            ### General situation
            We consider a homogeneous and isotropic aquifer. The aquifer can be confined and unconfined. If a well is pumping water out of the aquifer, radial flow towards the well is induced. To calculate the hydraulic situation, the following simplified flow equation can be used. This equation accounts for 1D radial transient flow towards a fully penetrating well within a confined or unconfined aquifer without further sinks and sources:
"""
)
st.latex(r'''\frac{\partial^2 h}{\partial r^2}+\frac{1}{r}\frac{\partial h}{\partial r}=\frac{S}{T}\frac{\partial h}{\partial t}''')
st.markdown("""
            ### Mathematical model and solution
            Charles V. Theis presented a solution for this by deriving
"""
)
st.latex(r'''s(r,t)=\frac{Q}{4\pi T}W(u)''')
st.markdown("""
            with the well function
"""
)
st.latex(r'''W(u) = \int_{u }^{+\infty} \frac{e^{-\tilde u}}{\tilde u}d\tilde u''')
st.markdown("""
            and the dimensionless variable
"""
)
st.latex(r'''u = \frac{Sr^2}{4Tt}''')
st.markdown("""
            This equations are not easy to solve. Historically, values for the well function were provided by tables or as so called type-curve. The type-curve matching with experimental data for pumping test analysis can be considered as one of the basic hydrogeological methods. However, modern computer provide an easier and more convinient way to solve the 1D radial flow equation based on the Theis approach. Subsequently, the Theis equation is solved with Python routines.
"""
)            


columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    st.write()
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/02_📈_▶️ Transient_Flow to a Well.py")
