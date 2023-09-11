import streamlit as st
import os
import io
import tempfile

from dotenv import load_dotenv
from PIL import Image
from googletrans import Translator

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

from langs import langs

load_dotenv()
PAT = os.getenv('PAT')

USER_ID='salesforce'
APP_ID='blip'
MODEL_ID = 'general-english-image-caption-blip-2'
MODEL_VERSION_ID = '71cb98f572694e28a99fa8fa86aaa825'

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

st.title('too lazy to write alt', anchor=False)
st.write('[![general-english-image-caption-blip-2](https://clarifai.com/api/salesforce/blip/models/general-english-image-caption-blip-2/badge)](https://clarifai.com/salesforce/blip/models/general-english-image-caption-blip-2)')

st.write('upload images')
images = st.file_uploader('upload images', help='we do not store your files', accept_multiple_files=True, label_visibility='collapsed')

st.write('alt language other than english')
col1, col2 = st.columns(2)

with col1:
    alt_lang = st.selectbox(
        'alt language other than english',
        (lang[0] for lang in langs),
        label_visibility='collapsed'
    )

for lang in langs:
    if alt_lang == lang[0]:
        code = lang[1]

with col2:
    button = st.button("generate alt because I'm too lazy", type='primary', use_container_width=True)

st.divider()

if images and button:
    def translate(text):
        translator = Translator()
        translate = translator.translate((text), src='en', dest=code)
        return translate.text

    temp_dir = tempfile.TemporaryDirectory()

    for i, image in enumerate(images):
        bytes_data = image.read()

        image_io = Image.open(io.BytesIO(bytes_data))

        temp_image_path = os.path.join(temp_dir.name, image.name)
        image_io.save(temp_image_path)

        IMAGE_URL = 'https://www.w3schools.com/html/pic_trulli.jpg'
        # IMAGE_URL = temp_image_path

        st.image(image, caption=f'{i+1}')

        response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,
                model_id=MODEL_ID,
                version_id=MODEL_VERSION_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            image=resources_pb2.Image(
                                url=IMAGE_URL
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )

        if response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            st.error(f'Post model outputs failed, status: ' + response.status.description)

        alt = response.outputs[0].data.text.raw

        st.caption('english alt')
        st.write(alt.capitalize())

        if not code =='en':
            st.caption(f'{alt_lang.lower()} alt')
            st.write(translate(alt))






