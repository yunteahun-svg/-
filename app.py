import streamlit as st
import cv2
import easyocr
from gtts import gTTS
import numpy as np

# 앱 제목 및 시각장애인 접근성 안내
st.title("👁️ 시각장애인용 식품 정보 음성 안내 앱")
st.write("카메라로 식품의 유통기한이나 성분표를 찍어 업로드하면 인공지능이 읽어줍니다.")

# 1. 스마트폰 카메라 촬영 및 파일 업로드 버튼 생성
uploaded_file = st.file_uploader("식품 사진을 찍거나 올려주세요", type=["jpg", "jpeg", "png"], capture="camera")

if uploaded_file is not None:
    # 업로드된 이미지를 화면에 띄우기
    st.image(uploaded_file, caption='업로드된 사진', use_column_width=True)
    
    with st.spinner('인공지능이 글자를 읽는 중입니다...'):
        # 2. 이미지를 변환하여 EasyOCR에 전달
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        
        # 인공지능 모델 로드 및 텍스트 추출
        reader = easyocr.Reader(['ko', 'en'])
        result = reader.readtext(image, detail=0)
        text = " ".join(result)
        
    # 3. 인식 결과 화면 표시
    st.subheader("=== 📝 인공지능 인식 결과 ===")
    if text.strip():
        st.write(text)
        
        # 4. gTTS를 활용한 음성 변환 (오디오 파일 생성)
        tts = gTTS(text=text, lang='ko')
        tts.save('result.mp3')
        
        # 5. 스마트폰에서 소리가 바로 재생되는 오디오 플레이어 탑재
        st.audio('result.mp3', format='audio/mp3', start_time=0)
    else:
        st.warning("글씨를 찾지 못했습니다. 사진을 더 밝고 선명하게 다시 찍어보세요!")