# Internal Modules
from config.api_keys import openai_api_key
from gpt.zsl import classify_case
# External Modules
import streamlit as st
import pandas as pd
import openai
import shutil
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import streamlit.components.v1 as components  # components 임포트

# 원본 폰트 파일 경로
source_font_regular = r".\static\fonts\HANBATANG.TTF"
source_font_bold = r".\static\fonts\HANBATANGB.TTF"

# matplotlib 폰트 디렉토리 경로
matplotlib_fonts_dir = matplotlib.matplotlib_fname().replace("matplotlibrc", "fonts")

# 대상 폰트 파일 경로
destination_font_regular = os.path.join(matplotlib_fonts_dir, "HANBATANG.TTF")
destination_font_bold = os.path.join(matplotlib_fonts_dir, "HANBATANGB.TTF")

# 폰트 파일이 존재하지 않으면 복사
if not os.path.exists(destination_font_regular):
    shutil.copy(source_font_regular, destination_font_regular)
    print(f"Copied {source_font_regular} to {destination_font_regular}")

if not os.path.exists(destination_font_bold):
    shutil.copy(source_font_bold, destination_font_bold)
    print(f"Copied {source_font_bold} to {destination_font_bold}")
# 한글 폰트 설정 (Windows)
font_path = r'./static/fonts/HANBATANG.TTF'
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)
# Streamlit UI
st.set_page_config(
    page_title='Excel Zero Shot Classification',
    page_icon='https://i.namu.wiki/i/NgVoid2KU7eIGUnYVeZKBcfdydT9zq9_l69cYGpP1LwOFKn4nnbHe_OhsE3MWPcDtt6jqST_9tUSjyuNw3lNzw.svg',
    initial_sidebar_state='collapsed'
)
# Sidebar
st.sidebar.header("작업 공종 예시")
with st.sidebar:
    # HTML and JavaScript for clipboard copying
    copy_text = """
    - 가설전기 작업
    - 비계 조립 및 해체 작업
    - 낙하물방지망 및 방호선반 작업
    - 타워크레인 설치 및 해체 작업
    - 건설용 리프트 설치 및 해체 작업
    - 굴착 및 발파 작업
    - 흙막이 지보공 작업
    - 거푸집동바리 작업
    - 철근 작업
    - 콘크리트 타설 작업
    - 작업발판 일체형 거푸집 작업
    - 철골 작업
    - PC 작업
    - 외부마감 작업
    - 내부마감 작업
    - 기계식주차장 설치 작업
    - 엘리베이터 설치 작업
    - 기계실 설비 작업
    - *지상높이가 31미터 이상인 건축물 참고
    - *깊이 10미터 이상인 굴착공사 참고
    - 가설작업
    - 가설도로 작업
    - 파일 작업
    - 구조물 작업
    - 거더작업(PSC I형거더)
    - FCM(Free Cantilever method)
    - ILM(Incremental Launching Method)
    - FSM(Full Staging Method)
    - PSM(Precast Segment Method)
    - 강교(Steel Box)
    - 주탑 및 케이블 설치작업(현수교, 사장교 및 Extradosed교)
    - 비계작업
    - 갱구부 또는 수직구 굴착작업
    - 플랜트 설치작업
    - 터널 발파작업
    - 버럭 처리작업
    - 숏크리트 작업
    - 강지보공 작업
    - 락볼트 작업
    - 터널 방수 및 철근배근 작업
    - 라이닝 콘크리트 작업
    - 기타 기계설비 설치작업
    - 가체절(가물막이) 작업
    - 배치플랜트 작업
    - 기초처리 작업
    - 본댐 기계설비 작업
    - 공도교 작업
    - 복공 설치 및 해체 작업
    """
    copy_button = f"""
    <button onclick="copyToClipboard()">Copy to Clipboard</button>
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText(`{copy_text}`);
        alert("Copied to clipboard");
    }}
    </script>
    """
    components.html(copy_button)
    st.write(copy_text)

# Function to display column preview
def display_column_preview(df, column):
    return df[column].head()

# Function to perform zero-shot classification using OpenAI
def zero_shot_classification(df, column, classes, model_name, openai_api_key):
    # openai.api_key = openai_api_key
    etr : str = '\n- '
    results = []
    for text in df[column]:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model=model_name,
            messages=f"다음 텍스트를 다음 중 하나로 분류하세요: \n\n- {etr.join(classes)}.\n\nText: {text}\nClass:",
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
