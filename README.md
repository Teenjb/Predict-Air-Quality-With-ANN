# Predict Air Quality Index (AQI) using Machine Learning

## Introduction
Air Quality Index (AQI) is a measure used to communicate how polluted the air currently is or how polluted it is forecast to become. Public health risks increase as the AQI rises. Different countries have their own air quality indices, corresponding to different national air quality standards. The AQI can be used to communicate to the public how polluted the air currently is or how polluted it is forecast to become. The AQI can be used to describe the quality of the air at any given time. The AQI is divided into categories that correspond to different levels of health concern. Each category corresponds to a different level of health concern. The six levels of health concern and what they mean are:

- 0-50: Good
- 51-100: Moderate
- 101-150: Unhealthy for Sensitive Groups
- 151-200: Unhealthy
- 201-300: Very Unhealthy
- 301-500: Hazardous
- 500+: Beyond the AQI

## Problem Statement
The AQI currently is calculated using the concentration of pollutants in the air. The technology use laser to measure the pollutants. The data is collected from the sensors and then the AQI is calculated. The problem with this approach is that the sensors are expensive and the data is not available for all the locations. The goal of this project is to predict the AQI using the cameras. The cameras are cheap and can be installed at all the locations. The data collected from the cameras can be used to predict the AQI. The data collected from the cameras is in the form of images. The images are of the sky. The goal of this project is to predict the AQI using the images of the sky.

## Dataset
The dataset is collected from the cameras. The dataset contains the images of the sky and the AQI. The dataset is divided into two parts: training and testing. The training dataset contains 1000 images and the testing dataset contains 100 images. The images are of the sky and the AQI is the target variable. The images are in the form of numpy arrays. The images are of the size 256x256. The AQI is the target variable. The AQI is a continuous variable. The AQI is divided into categories that correspond to different levels of health concern. The six levels of health concern and what they mean are:

## Approach
This project will use several machine learning ANNs to predict the AQI. The algorithms that will be used are:
- ResNet
- VGGNet
- AlexNet