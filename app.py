# Internal Modules
from config.api_keys import openai_api_key
from gpt.zsl import classify_case
# External Modules
import streamlit as st
import pandas as pd
import openai
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정 (Windows)
font_path = 'C:/Windows/Fonts/malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# Function to display column preview
def display_column_preview(df, column):
    return df[column].head()

# Function to perform zero-shot classification using OpenAI
def zero_shot_classification(df, column, classes, model_name, openai_api_key):
    # openai.api_key = openai_api_key
    results = []
    for text in df[column]:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model=model_name,
            messages=f"다음 텍스트를 다음 중 하나로 분류하세요: \n\n- {'\n- '.join(classes)}.\n\nText: {text}\nClass:",
            max_tokens=16,
            n=1,
            stop=None,
            temperature=0
        )
        results.append(response.choices[0].text.strip())
    return results

# Streamlit app
st.title("Zero-shot Classification App")

# API Key input
# openai_api_key = st.text_input("Enter your OpenAI API key", type="password")

if openai_api_key:
    # File upload
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write("File Uploaded Successfully!")

        # Display column names
        st.write("Select a column for classification:")
        column = st.selectbox("Columns", df.columns)

        # Display column preview
        if column:
            st.write(f"Preview of column: {column}")
            st.write(display_column_preview(df, column))

            # Input for class labels
            classes = st.text_area("Enter class labels separated by commas or bullet points")

            if classes:
                classes_list = [x.strip() for x in classes.replace('- ', ',').split(",") if x.strip()]
                st.write("Class Labels: ", classes_list)

                # Select GPT model
                model_name = st.selectbox("Select a GPT model", ["babbage-002", "davinci-002", "gpt-3.5-turbo", "gpt-3.5-turbo-0125", "gpt-4", "gpt-4-0613", "gpt-4-turbo", "gpt-4o"])

                if st.button("Perform Classification"):
                    with st.spinner('Performing classification...'):
                        progress_bar = st.progress(0)
                        total_steps = len(df)
                        # Perform zero-shot classification
                        # df["재해개요"] = classify_case(df[column])  # zero_shot_classification(df, column, classes_list, model_name, openai_api_key)
                        results = []

                        for i in range(total_steps):
                            case_description = df.loc[i, column]
                            classified_case = classify_case(case_description)
                            results.append(classified_case)
                            progress_bar.progress((i + 1) / total_steps)

                        # 새로운 컬럼에 결과 저장
                        df["작업공종"] = results
                        del progress_bar
                    st.write("Classification Completed!")
                    st.write(df.head())

                    # Display pie chart
                    st.write("Classification Results:")
                    chart_data = df["작업공종"].value_counts()
                    st.write(chart_data)
                    fig, ax = plt.subplots()
                    chart_data.plot.pie(autopct="%1.1f%%", ax=ax)
                    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                    st.pyplot(fig)

                    # Download button
                    def to_excel(df):
                        output = BytesIO()
                        writer = pd.ExcelWriter(output, engine='xlsxwriter')
                        df.to_excel(writer, index=False, sheet_name='Sheet1')
                        writer.close()  # save() 대신 close() 사용
                        processed_data = output.getvalue()
                        return processed_data

                    df_xlsx = to_excel(df)

                    st.download_button(label='Download Excel file with classification',
                                       data=df_xlsx,
                                       file_name='classified_data.xlsx')
