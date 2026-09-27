import streamlit as st
import cv2
import numpy as np


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Image Transformation Studio",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main page */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    /* Main heading */
    .main-title {
        font-size: 38px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 4px;
    }

    .subtitle {
        text-align: center;
        font-size: 16px;
        margin-bottom: 25px;
        opacity: 0.75;
    }

    /* Section headings */
    .section-title {
        font-size: 21px;
        font-weight: 650;
        margin-top: 8px;
        margin-bottom: 12px;
    }

    /* Preview labels */
    .preview-label {
        font-size: 17px;
        font-weight: 650;
        margin-bottom: 8px;
    }

    /* Status box */
    .status-box {
        padding: 12px 15px;
        border-radius: 8px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-top: 15px;
        margin-bottom: 15px;
    }

    /* Upload area */
    [data-testid="stFileUploader"] {
        margin-bottom: 10px;
    }

    /* Buttons */
    .stButton button,
    .stDownloadButton button {
        border-radius: 7px;
        font-weight: 600;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.2);
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">🖼️ Image Transformation Studio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive geometric image transformations powered by OpenCV'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "tx" not in st.session_state:
    st.session_state.tx = 0

if "ty" not in st.session_state:
    st.session_state.ty = 0

if "angle" not in st.session_state:
    st.session_state.angle = 0

if "scale" not in st.session_state:
    st.session_state.scale = 1.0

if "flip_horizontal" not in st.session_state:
    st.session_state.flip_horizontal = False

if "flip_vertical" not in st.session_state:
    st.session_state.flip_vertical = False


# ============================================================
# RESET FUNCTION
# ============================================================

def reset_transformations():

    st.session_state.tx = 0
    st.session_state.ty = 0
    st.session_state.angle = 0
    st.session_state.scale = 1.0

    st.session_state.flip_horizontal = False
    st.session_state.flip_vertical = False


# ============================================================
# IMAGE UPLOAD
# ============================================================

st.markdown(
    '<div class="section-title">📤 Upload Image</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose an image to transform",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)


# ============================================================
# MAIN APPLICATION
# ============================================================

if uploaded_file is not None:

    # ========================================================
    # READ IMAGE
    # ========================================================

    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )

    image_rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )


    # ========================================================
    # SIDEBAR CONTROLS
    # ========================================================

    with st.sidebar:

        st.markdown("## 🎛️ Controls")
        st.caption("Adjust the transformation parameters")

        st.divider()


        # ----------------------------------------------------
        # TRANSLATION
        # ----------------------------------------------------

        st.markdown("### ↔️ Translation")

        tx = st.slider(
            "Horizontal (X)",
            min_value=-300,
            max_value=300,
            step=10,
            key="tx"
        )

        ty = st.slider(
            "Vertical (Y)",
            min_value=-300,
            max_value=300,
            step=10,
            key="ty"
        )


        st.divider()


        # ----------------------------------------------------
        # ROTATION
        # ----------------------------------------------------

        st.markdown("### 🔄 Rotation")

        angle = st.slider(
            "Angle",
            min_value=-180,
            max_value=180,
            step=1,
            key="angle"
        )


        st.divider()


        # ----------------------------------------------------
        # SCALING
        # ----------------------------------------------------

        st.markdown("### 🔍 Scaling")

        scale = st.slider(
            "Scale Factor",
            min_value=0.1,
            max_value=3.0,
            step=0.1,
            key="scale"
        )


        st.divider()


        # ----------------------------------------------------
        # FLIP
        # ----------------------------------------------------

        st.markdown("### 🪞 Flip")

        flip_col1, flip_col2 = st.columns(2)

        with flip_col1:

            if st.button(
                "↔️ Flip H",
                use_container_width=True
            ):

                st.session_state.flip_horizontal = (
                    not st.session_state.flip_horizontal
                )

        with flip_col2:

            if st.button(
                "↕️ Flip V",
                use_container_width=True
            ):

                st.session_state.flip_vertical = (
                    not st.session_state.flip_vertical
                )


        st.divider()


        # ----------------------------------------------------
        # RESET
        # ----------------------------------------------------

        st.button(
            "🔄 Reset All",
            on_click=reset_transformations,
            use_container_width=True
        )


        st.divider()


        # ----------------------------------------------------
        # CURRENT VALUES
        # ----------------------------------------------------

        st.markdown("### 📊 Current Values")

        st.write(f"**X:** {tx}px")
        st.write(f"**Y:** {ty}px")
        st.write(f"**Rotation:** {angle}°")
        st.write(f"**Scale:** {scale}×")

        flip_status = []

        if st.session_state.flip_horizontal:
            flip_status.append("Horizontal")

        if st.session_state.flip_vertical:
            flip_status.append("Vertical")

        if flip_status:
            st.write(
                "**Flip:** " + ", ".join(flip_status)
            )
        else:
            st.write("**Flip:** None")


    # ========================================================
    # APPLY TRANSFORMATIONS
    # ========================================================

    transformed_image = image.copy()


    # --------------------------------------------------------
    # FLIP
    # --------------------------------------------------------

    if st.session_state.flip_horizontal:

        transformed_image = cv2.flip(
            transformed_image,
            1
        )

    if st.session_state.flip_vertical:

        transformed_image = cv2.flip(
            transformed_image,
            0
        )


    # --------------------------------------------------------
    # TRANSLATION
    # --------------------------------------------------------

    height, width = transformed_image.shape[:2]

    translation_matrix = np.float32([
        [1, 0, tx],
        [0, 1, ty]
    ])

    transformed_image = cv2.warpAffine(
        transformed_image,
        translation_matrix,
        (width, height)
    )


    # --------------------------------------------------------
    # ROTATION + SCALING
    # --------------------------------------------------------

    center = (
        width // 2,
        height // 2
    )

    rotation_matrix = cv2.getRotationMatrix2D(
        center,
        angle,
        scale
    )

    transformed_image = cv2.warpAffine(
        transformed_image,
        rotation_matrix,
        (width, height)
    )


    # ========================================================
    # CONVERT TO RGB
    # ========================================================

    transformed_image_rgb = cv2.cvtColor(
        transformed_image,
        cv2.COLOR_BGR2RGB
    )


    # ========================================================
    # TRANSFORMATION STATUS
    # ========================================================

    st.markdown(
        '<div class="status-box">'
        '🔹 <b>Live Preview</b> — Changes are applied instantly'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # IMAGE PREVIEW
    # ========================================================

    st.markdown(
        '<div class="section-title">🖼️ Preview</div>',
        unsafe_allow_html=True
    )

    original_col, transformed_col = st.columns(2)


    # --------------------------------------------------------
    # ORIGINAL
    # --------------------------------------------------------

    with original_col:

        st.markdown(
            '<div class="preview-label">Original Image</div>',
            unsafe_allow_html=True
        )

        st.image(
            image_rgb,
            use_container_width=True
        )


    # --------------------------------------------------------
    # TRANSFORMED
    # --------------------------------------------------------

    with transformed_col:

        st.markdown(
            '<div class="preview-label">Transformed Image</div>',
            unsafe_allow_html=True
        )

        st.image(
            transformed_image_rgb,
            use_container_width=True
        )


    # ========================================================
    # IMAGE INFORMATION
    # ========================================================

    info1, info2, info3 = st.columns(3)

    info1.metric(
        "Image Width",
        f"{width}px"
    )

    info2.metric(
        "Image Height",
        f"{height}px"
    )

    info3.metric(
        "Scale",
        f"{scale}×"
    )


    # ========================================================
    # DOWNLOAD
    # ========================================================

    st.markdown(
        '<div class="section-title">💾 Export</div>',
        unsafe_allow_html=True
    )

    success, encoded_image = cv2.imencode(
        ".png",
        transformed_image
    )

    if success:

        st.download_button(
            label="💾 Download Transformed Image",
            data=encoded_image.tobytes(),
            file_name="transformed_image.png",
            mime="image/png",
            use_container_width=True
        )


else:

    # ========================================================
    # EMPTY STATE
    # ========================================================

    st.info(
        "👆 Upload an image above to start transforming it."
    )

    st.markdown(
        """
        ### ✨ Available Transformations

        | Transformation | Function |
        |---|---|
        | ↔️ Translation | Move the image horizontally or vertically |
        | 🔄 Rotation | Rotate the image from -180° to +180° |
        | 🔍 Scaling | Resize from 0.1× to 3.0× |
        | 🪞 Flip | Flip horizontally or vertically |
        """
    )