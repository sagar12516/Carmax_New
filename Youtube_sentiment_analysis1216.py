from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import time
import json
import boto3
from pyspark_carmax import streaming
import numpy as np
import pandas as pd
import streamlit as st
from urllib.parse import urljoin
from Yt_st_final import preprocessing



class YT():

    def main(self,url):

        placeholder = st.empty()

        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        # chromedriver_path="/Users/venkatsagar/Documents/Python books/webdriver/chrome_driver"
        chromedriver_path = "/Users/venkatsagar/Applications/Anaconda/anaconda3/lib/python3.11/site-packages (1.4.1)/phantomjs"
        service = Service(service=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # st.set_page_config(
        #         page_title="YT Sentiment Analysis",
        #         page_icon="✅",
        #         layout="wide",
        #     )
        # st.title("YT Sentiment Analysis")

        base_url = "https://www.youtube.com/watch?v=1xMG7SfKe8A&ab_channel=TSports"
        driver.get(url)
        time.sleep(5)
        listings = driver.find_element(by=By.ID,value="secondary")
        listings = listings.find_element(by=By.ID, value="secondary-inner")
        listings = listings.find_element(by=By.CSS_SELECTOR,value="div[id='chat-container']")
        listings = listings.find_element(by=By.TAG_NAME,value="ytd-live-chat-frame")
        iframe = WebDriverWait(listings, 10000).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"iframe[id='chatframe']")))
        # iframe = listings.find_element(by=By.CSS_SELECTOR,value="iframe[id='chatframe']")
        print("iframe ",iframe)
        # driver.switch_to.frame(iframe)
        src = iframe.get_attribute("src")
        print("src is here ",src)
        url = "https://www.youtube.com/"+src.split("/")[-1]




        # driver.close()
        print("url is here ",url)
        time.sleep(5)
        driver.get(url)
        time.sleep(5)

        listings = WebDriverWait(driver, 10000).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"div[id='contents']")))

        contents_list = listings.find_element(by=By.CSS_SELECTOR,value="div[id='contents']")
        comment_list = contents_list.find_elements(by=By.CSS_SELECTOR,
                                          value="yt-live-chat-text-message-renderer[class='style-scope yt-live-chat-item-list-renderer']")

        ct_cm_lt = len(comment_list) #55
        print(ct_cm_lt)
        for i in range(len(comment_list)):
            comment = comment_list[i].find_element(by=By.CSS_SELECTOR, value="span[id='message']")
            print(comment.text)

        # To retrieve recent comment store use len(listings) and if the listings increases then print last indexed value
        # Ex : while len(listings) > listings: then print(comment)

        # def scrpe_cmnts(contents_list):
        #     comment_list = contents_list.find_elements(by=By.CSS_SELECTOR,
        #                                       value="yt-live-chat-text-message-renderer[class='style-scope yt-live-chat-item-list-renderer']")
        #     return comment_list

        while True:
            comment_list = contents_list.find_elements(by=By.CSS_SELECTOR,
                                                      value="yt-live-chat-text-message-renderer[class='style-scope yt-live-chat-item-list-renderer']")
            if len(comment_list) > ct_cm_lt:
                idx_cmnts_len = len(comment_list) - ct_cm_lt  #5
                # print("comment lst ", len(comment_list), "old cmnt lst ", ct_cm_lt)
                cm_lst = comment_list[-idx_cmnts_len:]
                for i in cm_lst:
                    message = i.find_element(by=By.CSS_SELECTOR, value="span[id='message']")
                    comment = message.text
                    preprocessing(self,st,comment,placeholder)
                    ct_cm_lt += 1
            time.sleep(2)






        # while True:
        #     comment_list = listings.find_elements(by=By.CSS_SELECTOR,
        #                                       value="yt-live-chat-text-message-renderer[class='style-scope yt-live-chat-item-list-renderer']")
        #
        #     cm_lst = comment_list.find_element(by=By.CSS_SELECTOR, value="span[id='message']")
        #
        #     if len(cm_lst) > ct_cm_lt:
        #         print(cm_lst[-1].text)
        #         ct_cm_lt = len(cm_lst)


        # print("Comments here ",listings.text)
        # listings = listings.find_element(by=By.ID, value="chat-container")
        # listings = listings.find_element(by=By.CSS_SELECTOR,value="ytd-live-chat-frame[id='chat']")
        # print("Listings here ",listings.text)
        # src = listings.get_attribute("src")
        # print("src here ",src)
        # time.sleep(10)
        # driver.switch_to.frame(listings.find_element(by=By.TAG_NAME,value="iframe"))
        # time.sleep(10)
        # listings = driver.find_element(by=By.XPATH,value="/html/body")
        # time.sleep(10)
        # driver.switch_to.frame(listings.find_element(by=By.TAG_NAME,value="yt-live-chat-app"))
        # listings = listings.find_element(by=By.CSS_SELECTOR,value="div[id='contents']")
        # listings = listings.find_element(by=By.CSS_SELECTOR,value="iron-pages[id='content-pages']")


        # src = driver.find_element(By.TAG_NAME, "iframe").get_attribute("src")
        # print("src is ",src)
        # print("here ",listings)
        # print(listings.text)
        # print("len of listings ",len(listings))
        # elems = listings.find_elements(By.XPATH,value="//*[@id='message']")
        # print(elems)
        # print(len(elems))
        # print(listings[0])
        # for i in listings:
        #     content =  i.find_element(by=By.ID,value='content')
        #     message = content.find_element(by=By.ID,value='message')
        #     text = message.text
        #     print(text)
        #     # st.write(text)
        #


if __name__ == '__main__':
    st.set_page_config(
        page_title="Youtube Sentiment Analysis",
        page_icon="✅",
        layout="wide",
    )

    with st.form("myform"):
        url = st.text_input("Paste URL")
        submitted = st.form_submit_button("Submit")

    if submitted:
        YT().main(url)