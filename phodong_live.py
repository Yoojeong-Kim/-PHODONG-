import streamlit as st
import time
import io

class CameraManager:
    """카메라 촬영 및 캡처된 이미지 관리를 담당하는 클래스"""
    
    @staticmethod
    def init_state():
        if "camera_captures" not in st.session_state:
            st.session_state.camera_captures = []

    @staticmethod
    def render_camera_ui():
        """카메라 UI를 그리고, 최종적으로 선택된 이미지 리스트(BytesIO)를 반환하거나 None을 반환"""
        CameraManager.init_state()
        
        st.markdown("### 📸 실시간 촬영 모드")
        st.info("카메라로 찰칵! 찍으면 아래에 사진이 모여요.")

        c1, c2 = st.columns([1, 1], gap="medium")
        
        # [왼쪽] 카메라 입력창
        with c1:
            # key를 고정하면 리셋이 안 되므로, 캡처 시마다 key를 다르게 줄 수도 있으나
            # 여기서는 심플하게 고정하고 state로 관리
            cam_image = st.camera_input("여기를 눌러 사진을 찍으세요", label_visibility="collapsed")
            
            if cam_image:
                bytes_data = cam_image.getvalue()
                # 중복 방지 (가장 최근 사진과 비교)
                if not st.session_state.camera_captures or st.session_state.camera_captures[-1] != bytes_data:
                    st.session_state.camera_captures.append(bytes_data)
                    st.toast(f"📸 찰칵! ({len(st.session_state.camera_captures)}장 저장됨)")
                    time.sleep(0.5) 
                    st.rerun()

        # [오른쪽] 찍은 사진 갤러리 & 완료 버튼
        with c2:
            st.markdown(f"**🖼️ 모은 조각들 ({len(st.session_state.camera_captures)}장)**")
            
            if st.session_state.camera_captures:
                # 갤러리 뷰 (3열 그리드)
                cols = st.columns(3)
                for idx, img_bytes in enumerate(st.session_state.camera_captures):
                    with cols[idx % 3]:
                        st.image(img_bytes, use_container_width=True)
                
                st.markdown("---")
                
                # 액션 버튼들
                col_act1, col_act2 = st.columns(2)
                with col_act1:
                    if st.button("🗑️ 모두 비우기", use_container_width=True):
                        st.session_state.camera_captures = []
                        st.rerun()
                with col_act2:
                    # [최종 완료 시] 찍은 사진들을 BytesIO 리스트로 변환하여 반환
                    if st.button("✨ 이걸로 이야기 만들기", type="primary", use_container_width=True):
                        return [io.BytesIO(b) for b in st.session_state.camera_captures]
            else:
                st.markdown("""
                <div style="padding:20px; border:2px dashed #DDD; border-radius:10px; text-align:center; color:#AAA;">
                    아직 찍은 사진이 없어요.<br>왼쪽에서 사진을 찍어보세요!
                </div>
                """, unsafe_allow_html=True)
        
        return None