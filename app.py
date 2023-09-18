import streamlit as st
import os
import io
import tempfile

from PIL import Image
from googletrans import Translator

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

from langs import langs

##### Streamlit Configurations #####
st.set_page_config(
    page_title='too lazy to write alt',
    page_icon='🦥',
    layout='centered',
    menu_items={
        'About': '''
         [![general-english-image-caption-blip-2-6_7B](https://clarifai.com/api/salesforce/blip/models/general-english-image-caption-blip-2-6_7B/badge)](https://clarifai.com/salesforce/blip/models/general-english-image-caption-blip-2-6_7B) [![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/claromes/toolazytowritealt?include_prereleases)](https://github.com/claromes/toolazytowritealt/releases) [![License](https://img.shields.io/github/license/claromes/toolazytowritealt)](https://github.com/claromes/toolazytowritealt/blob/main/LICENSE)

        # 🦥

        *alt text for lazy people*

        generate and translate alt text using vision-language pre-trained and large language model

        features:

        - mobile-friendly
        - multiple images via upload or URL
        - translation into multiple languages
        - copy to clipboard

        -------
        ''',
        'Report a bug': 'https://github.com/claromes/toolazytowritealt/issues'
    }
)

##### Clarifai Variables #####
PAT = st.secrets.PAT

USER_ID='salesforce'
APP_ID='blip'
MODEL_ID = 'general-english-image-caption-blip-2-6_7B'
MODEL_VERSION_ID = 'd5ce30a4f98646deb899a19ff4becaad'

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

##### Functions #####
##### ##### Translation ##### #####
def translate(text):
    translator = Translator()
    translate = translator.translate((text), src='en', dest=code)
    return translate.text

##### ##### Alt Text Interface ##### #####
def show_result(image, alt):
    col1, col2 = st.columns(2)

    with col1:
        st.image(image)

    with col2:
        st.caption('english alt')
        st.code(alt.capitalize(), language='text')

        if not code =='nothanks':
            st.caption(f'{alt_lang.lower()} alt')
            st.code(translate(alt).capitalize(), language='text')

##### Streamlit Sytle Variables #####
file_uploader_font_size = '''
<style>
    .css-13f0ups  {
        font-size: 12px;
    }
</style>
'''

st.markdown(file_uploader_font_size, unsafe_allow_html=True)

##### Options Interface #####
st.title('too lazy to write alt', anchor=False)
st.caption('generate and translate alt text using VLP and LLM')

st.columns(1)

uploaded_files = st.file_uploader('upload images', type=['PNG', 'JPG', 'JFIF', 'TIFF', 'BMP', 'WEBP'], accept_multiple_files=True, help='''
                                                                                                                                        - up to 128 images
                                                                                                                                        - we do not store your images
                                                                                                                                        ''')

url = st.text_input('paste an image URL')

alt_lang = st.selectbox(
    'alt text language other than english',
    (lang[0] for lang in langs)
)

for lang in langs:
    if alt_lang == lang[0]:
        code = lang[1]

_, col2, _ = st.columns([2, 8, 2])

with col2:
    st.columns(1)
    button = st.button("generate alt because I'm too lazy", type='primary', use_container_width=True)

st.divider()

##### Predictions #####
##### Docs: https://docs.clarifai.com/api-guide/predict/images
if button:
    try:
        with st.spinner('generating...'):
            ##### ##### Predict via Bytes ##### #####
            if uploaded_files:
                temp_dir = tempfile.TemporaryDirectory()

                for i, image in enumerate(uploaded_files):
                    bytes_data = image.read()

                    image_io = Image.open(io.BytesIO(bytes_data))

                    temp_image_path = os.path.join(temp_dir.name, image.name)
                    image_io.save(temp_image_path)

                    IMAGE_FILE_LOCATION = temp_image_path

                    with open(IMAGE_FILE_LOCATION, 'rb') as f:
                        file_bytes = f.read()

                    response = stub.PostModelOutputs(
                        service_pb2.PostModelOutputsRequest(
                            user_app_id=userDataObject,
                            model_id=MODEL_ID,
                            version_id=MODEL_VERSION_ID,
                            inputs=[
                                resources_pb2.Input(
                                    data=resources_pb2.Data(
                                        image=resources_pb2.Image(
                                            base64=file_bytes
                                        )
                                    )
                                )
                            ]
                        ),
                        metadata=metadata
                    )

                    if response.status.code != status_code_pb2.SUCCESS:
                        st.error(f'Post model outputs failed, status: ' + response.status.description)

                    alt = response.outputs[0].data.text.raw

                    show_result(temp_image_path, alt)

            ##### ##### Predict via URL ##### #####
            if url:
                response = stub.PostModelOutputs(
                    service_pb2.PostModelOutputsRequest(
                        user_app_id=userDataObject,
                        model_id=MODEL_ID,
                        version_id=MODEL_VERSION_ID,
                        inputs=[
                            resources_pb2.Input(
                                data=resources_pb2.Data(
                                    image=resources_pb2.Image(
                                        url=url
                                    )
                                )
                            )
                        ]
                    ),
                    metadata=metadata
                )

                alt = response.outputs[0].data.text.raw

                show_result(url, alt)

            st.columns(1)
            st.caption('**Limitations**: The BLIP-2 image captioning model inherits language model limitations like offensive language and bias. Performance issues can arise from inaccurate knowledge, outdated information, and data quality. [Read more](https://github.com/claromes/toolazytowritealt#language-model).')
    except Exception as e:
        st.error(f'An error has occurred: {e}')
