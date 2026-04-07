import streamlit as st
import requests

st.set_page_config(
    page_title="Data Analytics RAG",
    page_icon="📊",
    layout="centered",
)
st.title("Data Analytics RAG")
st.markdown("Upload a CSV or Excel file to analyze your data with the power of RAG!")

st.subheader("Upload Your File")

uploaded_file = st.file_uploader("Choose a CSV or Excel File",
                                 type = ["csv", "xlsx", "xls"])

if uploaded_file is not None:
    with st.spinner("Uploading the file and analysing your data..."): 
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        response =  requests.post("http://127.0.0.1:8000/upload", files=files)

        if response.status_code == 200:
            data = response.json()
            st.success(data["message"])

            info =  data["data_info"]
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Rows", info["rows"])
            with col2:
                st.metric("Total Columns", len(info["columns"]))    

                st.write("**Columns:**", ", ".join(info["columns"]))
                st.dataframe(info["preview"])
        else:
            st.error("Upload Failed. Make sure you FastApi is working") 

# Ask Question section

st.subheader("Ask a Question about your data")

question = st.text_input("Type your question here...",
placeholder = "what is the average sales, what is the number of columns in the dataset?"
)

if st.button("Ask AI"):
    if question == "":
        st.warning("Please type a question first!")
    else:
        with st.spinner("Thinking..."):
            response = requests.post("http://127.0.0.1:8000/ask", json={"question": question})

            if response.status_code == 200:
                data = response.json()
                st.success("Answer: ")
                st.write(data["answer"])
            else: 
                st.error("Failed to get an answer. Please upload a file first!")    
