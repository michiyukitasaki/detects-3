from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import json

subscription_key = "730d3e76c1d041f1a29db31e9cd4cb0c"
endpoint = "https://michi-20210930.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


def get_tags(filepath):
    local_image = open(filepath, "rb")
    tags_result = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
    return tags_name


def detect_objects(filepath):
    local_image = open(filepath, "rb")
    detect_objects_results = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_objects_results.objects
    return objects

import streamlit as st
from PIL import ImageDraw
from PIL import ImageFont

st.title('パンの測長アプリ')

st.sidebar.title('**注意事項**')
st.sidebar.write('15cmの距離で撮影しましたか？')
st.sidebar.write('画像に検査物は1つですか？')

uploaded_file = st.file_uploader('Choose an image...', type=['jpg','png'])
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_path = f'img/{uploaded_file.name}'
    img.save(img_path)
    objects = detect_objects(img_path)

    #描画
    draw = ImageDraw.Draw(img)
    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h
        caption = object.object_property
        caption1 = str(w - x)
        caption2 = str(h - y)

        font = ImageFont.truetype(font='./GenEiNombre.ttf', size=100)
        text_w, text_h = draw.textsize(caption, font=font)
        draw.rectangle([(x,y), (x+w, y+h)], fill=None, outline='red', width=50)
        # draw.rectangle([(x, y), (x + text_w, y + text_h)], fill='red')
        # draw.rectangle([(x, y + text_h), (x + text_w, y + 2*(text_h))], fill='red')
        # draw.text((x, y),caption1, fill='white', font=font)
        # draw.text((x, y + text_h), caption2, fill='white', font=font)

    st.image(img)

    tags_name = get_tags(img_path)
    tags_name = ', '.join(tags_name)
    caption3 = f'X：{caption1}mm, Y：{caption2}mm'


    st.markdown('**パンのサイズ**')
    # st.markdown(f'{tags_name}')
    st.markdown(caption3)