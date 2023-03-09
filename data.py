from googleapiclient.discovery import build
#import pandas as pd
import cv2
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
import requests
from sklearn.manifold import MDS

def get_data(API_KEY, number_of_videos, region="GB"):
  youtube = build("youtube", "v3", developerKey=API_KEY)
  nextPageToken = None
  video_data=[]
  quotient_batch = number_of_videos//50
  remainder_batch = number_of_videos%50 
  for i in range(quotient_batch):
      params = {
          "part": "snippet,contentDetails,statistics",
          "chart": "mostPopular",
          "regionCode": region,
          "maxResults": 50,
          "pageToken":nextPageToken
      }
      results = youtube.videos().list(**params).execute()
      #video_titles = [item["snippet"]["title"] for item in results["items"]]
      nextPageToken= results.get("nextPageToken")
      video_data = video_data + [(item["snippet"]["title"],
                                  item["snippet"]["thumbnails"]["default"]["url"],
                                  item["snippet"]["channelTitle"],
                                  item["statistics"]["viewCount"]) for item in results["items"]]
      youtube.close()
  for i in range(1):
    params = {
        "part": "snippet,contentDetails,statistics",
        "chart": "mostPopular",
        "regionCode": region,
        "maxResults": remainder_batch,
        "pageToken":nextPageToken
    }
    results = youtube.videos().list(**params).execute()
    #video_titles = [item["snippet"]["title"] for item in results["items"]]
    nextPageToken= results.get("nextPageToken")
    video_data = video_data + [(item["snippet"]["title"], item["snippet"]["thumbnails"]["default"]["url"], item["snippet"]["channelTitle"], item["statistics"]["viewCount"]) for item in results["items"]]
    youtube.close()
    return video_data
  


def parse_variables(video_data):
    urls = []
    titles = []
    channels = []
    views = []
    for i,j,k,l in video_data:
        titles.append(i)
        urls.append(j)
        channels.append(k)
        views.append(int(l))
    return urls, titles, channels, views

def download_image(url, file_name):
    response = requests.get(url)
    open(file_name, "wb").write(response.content)

def folder_thumbnails(urls):
    for i, url in enumerate(urls):
        download_image(url, f"thumbnails/image_{i}.jpg")

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (64, 64))
    image = image.astype("float32") / 255.0
    return image

def extract_features(images):
    model = ResNet50(weights="imagenet", include_top=False, input_shape=(64, 64, 3))
    features = model.predict(preprocess_input(images))
    features = features.reshape((features.shape[0], -1))
    return features

