import time

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
import mysql.connector




class data_output():
    # carInfo = {"name": [], "price": [], "mileage": [], "vin": [], "link": [], "ratings": [],
    #                 "reviews": [], "pros": [],
    #                 "cons": []}
    carInfo = {}
    url = "https://www.carmax.com/cars/" #1
    close_btn  = "/html/body/div[6]/button" #2
    close_btn2 = "button[title='Close']" #3
    lists_var = "//*[@id='cars-listing']/div[2]" #4
    matches_ct = "//*[@id='number-of-matches']" #5
    cstm_srch_cls = "button[class='sc--close-accessible-button base-modal--close']" #6
    crnt_view = "span[class ='see-more--blue']" #7
    list2 = "scct--tile-shell" #8
    get_link = "scct--image-gallery__image-link" #9
    car_name = "h1[class = 'car-header-basic-car-info']" #10
    car_price = "span[id='default-price-display']" #11
    price_zero = "price-drop-header-display" #12
    car_mileage = "car-header-mileage" #13
    vin_num = "/html/body/main/section[1]/div[5]/div/button[2]/span[3]" #14
    cstm_srch_cls2 = "button[class='sc--close-accessible-button base-modal--close']" #15


    def __init__(self,driver,carBrand,fltr1,prceMlgeFltr,placeholder,model_yr_fltr):
        self.driver = driver
        self.carBrand = carBrand
        self.fltr1 = fltr1
        self.placeholder = placeholder
        self.prceMlgeFltr = prceMlgeFltr
        self.model_yr_fltr = model_yr_fltr


        # URL
        self.driver.get(f"{self.__class__.url}{self.carBrand}") #1
        time.sleep(2)

        try:
            close_btn = driver.find_element(by=By.XPATH, value={self._class__.close_btn})  #2
            close_btn.click()
        except:
            pass


        try:
            self.driver.find_element(by=By.CSS_SELECTOR, value=self.__class__.close_btn2).click() #3
        except:
            pass
        # totalMatches = driver.find_element(by=By.CSS_SELECTOR,value="span[class='see-more--blue']")
        print("Printing the listings")
        listing = self.driver.find_element(by=By.XPATH, value=self.__class__.lists_var) #4
        # print("After listings... ",listing)
        # listings = self.driver.find_elements(by=By.CSS_SELECTOR, value="article[class='scct--car-tile car-tile fluid']")

        listings = listing.find_elements(by=By.CLASS_NAME, value = 'scct--car-tile car-tile fluid scct--car-tile--compact')
        # totalMatches = self.driver.find_element(by=By.XPATH, value="//div[@class='number-of-matches']/span[1]").text
        totalMatches = self.driver.find_element(by=By.XPATH, value = self.__class__.matches_ct).text
        totalMatches = int(totalMatches.replace(",", ""))

        print("Total Matches ",totalMatches)

        # Before using the below code add ratings and reviews to the dataframe
        try:
            cstmSearchBtn = self.driver.find_element(by=By.CSS_SELECTOR,
                                                value=self.__class__.cstm_srch_cls) #6
            cstmSearchBtn.click()
            print("custom search clicked")
        except:
            pass

        currentView = self.driver.find_element(by=By.CSS_SELECTOR, value=self.__class__.crnt_view) #7

        print('current view ', currentView.text)

        # print('matches ', matches)
        # print('total matches ',totalMatches)





    def kinesis_streaming(self,incoming_data):
        AWS_ACCESS_KEY = ""
        AWS_SECRET_KEY = ""
        AWS_REGION_NAME = ""

        print(incoming_data)

        client = boto3.client(
            "kinesis",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION_NAME,
        )

        response = client.put_record(  # kinesis Data Streams only , use different parameters for Firehose
            StreamName='',
            Data=json.dumps(incoming_data),
            PartitionKey=''
        )
        print(response)




    def lengthChk(self):
        # print("LengthChk called.....")
        # print(self.__class__.carInfo)
        # print("Before checking length condition.....")
        # if len(self.__class__.carInfo['Name']) == 5:
        # self.kinesis_streaming(self.__class__.carInfo)
        # print("Length of the carInfo... ", len(self.__class__.carInfo["name"]))
        # self.__class__.carInfo = {"name": [], "price": [], "mileage": [], "vin": [], "link": [], "ratings": [],
        #            "reviews": [], "pros": [],
        #            "cons": []}

        streaming(self.__class__.carInfo, self.fltr1, self.prceMlgeFltr,st,self.placeholder,self.model_yr_fltr)
        # self.__class__.carInfo = {}



    def mysql_create(self):
        mydb = mysql.connector.connect(
            host="",
            user="",
            password="",
            database=""
        )
        mycursor = mydb.cursor()
        cols = list(data_output.carInfo.keys())  # ['link', 'name', 'price', 'mileage', 'vin']
        data_types = ['varchar(100)', 'varchar(100)', 'int', 'int', 'varchar(100)']

        create_state = "create table if not exists carmax.test_carmax( id int not null auto_increment primary key, "

        for i in range(len(cols)):
            if i == len(cols)-1:
                create_state = create_state + cols[i] + ' ' + data_types[i]
            else:
                create_state = create_state + cols[i] + ' ' + data_types[i] + ', '

        create_state = create_state + ')'
        print(create_state)
        mycursor.execute(create_state)
        mydb.commit()
        mycursor.close()
        mydb.close()



    def mysql_insert(self):
        mydb = mysql.connector.connect(
            host="",
            user="",
            password="",
            database=""
        )
        mycursor = mydb.cursor()
        cols = list(data_output.carInfo.keys())  # ['link', 'name', 'price', 'mileage', 'vin']
        vals = list(data_output.carInfo.values())
        insert_state = "insert into carmax.test_carmax("
        for i in range(len(cols)):
            if i == len(cols)-1 :
                insert_state = insert_state + cols[i] + ')'
                # values = f"values( {vals[i]} )"
            else:
                insert_state = insert_state + cols[i] + ', '
                # values = f"values({vals[i]} , "
        inserted_vals =  insert_state + f" values{tuple(vals)}"
        print(inserted_vals)
        mycursor.execute(inserted_vals)
        # mycursor.execute("select * from carmax.test_carmax")
        mydb.commit()
        mycursor.close()
        mydb.close()



    def CarData(self,listings, startPt, endPt):
        create_qry = 0
        # carInfo = {"Name": [], "Price": [], "Mileage": [], "Vin": [], "link": []}
        for i in range(startPt, endPt):
            time.sleep(1)
            listings = self.driver.find_elements(by=By.CLASS_NAME, value=self.__class__.list2) #8
            # print("len of list in for loop ", len(listings))

            # print("len of listings ", len(listings))
            # print("current index ", i)
            #         element = listings[i].find_elements(by=By.CLASS_NAME,value="scct--tile-shell")
            element = listings[i]

            link = element.find_element(by=By.CLASS_NAME, value=self.__class__.get_link).get_attribute('href') #9
            # print('link ', link)
            element.click()
            self.__class__.carInfo['link'] = link
            heading = WebDriverWait(self.driver, 1000000).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.__class__.car_name))) #10
            # heading = driver.find_element(by=By.CSS_SELECTOR,value="h1[class = 'car-header-basic-car-info']")
            self.__class__.carInfo['name'] = heading.text
            price = self.driver.find_element(by=By.CSS_SELECTOR, value=self.__class__.car_price) #11
            price = re.findall(r'\d+', price.text)
            price = ''.join(price)
            price = price.strip()
            #         print("price ",price)
            if len(price) == 0:
                price = self.driver.find_element(by=By.ID, value=self.__class__.price_zero) #12
                # price = re.findall(r'\d+', price.text)
                price = price.text.split("\n")[0]
                print("Price before join ",price)
                price = re.findall(r'\d+', price)
                price = ''.join(price)
                print("price is ",price)
                self.__class__.carInfo['price'] = int(price)
            else:
                self.__class__.carInfo['price'] = int(price)
            mileage = self.driver.find_element(by=By.CLASS_NAME, value=self.__class__.car_mileage) #13
            mileage_txt = mileage.text.split(" ")[0]
            mileage_txt = mileage_txt.replace("K", "000")
            self.__class__.carInfo['mileage'] = int(mileage_txt)
            VIN = self.driver.find_element(by=By.XPATH, value=self.__class__.vin_num) #14
            # print('VIn ',VIN.text)
            self.__class__.carInfo['vin'] = VIN.text
            try:
               

               
                self.lengthChk()  # Invoking length check function
                if create_qry == 0:
                    self.mysql_create()
                    create_qry += 1
                else:
                    pass
                self.mysql_insert()
                self.driver.back()
            except Exception as  e:
                # self.__class__.carInfo['reviews'] = [None]
                # self.__class__.carInfo['ratings'] = [None]
                # self.__class__.carInfo['pros'] = [None]
                # self.__class__.carInfo['cons'] = [None]

                self.lengthChk()  # Invoking length check function
                if create_qry == 0:
                    self.mysql_create()
                    create_qry += 1
                else:
                    pass
                self.mysql_insert()
                self.driver.back()
        try:
            cstmSearchBtn = self.driver.find_element(by=By.CSS_SELECTOR,
                                                value=self.__class__.cstm_cls2) #15
            cstmSearchBtn.click()
        except:
            pass









if __name__ == '__main__':

    see_more_btn =  "/html/body/main/div[1]/div/section/section[1]/div/div[3]/div/hzn-button" #1
    car_list_main = "scct--tile-shell" #2

    st.set_page_config(
        page_title="Carmax",
        page_icon="✅",
        layout="wide",
    )

    st.title("Real Time Data")
    placeholder = st.empty()

    with st.form("myform"):
        carBrand = st.text_input("Enter the Brand Name")
        fltr1 = st.radio("Select the filter ", ['Lowest', 'Highest'])
        # fltr2 = st.radio("Select the filter ", ['price','mileage'])
        prceMlgeFltr = st.radio("Select the options", ['price','mileage'])
        start_year, end_year = st.select_slider(
            "Select a range of color wavelength",
            options= list(map(lambda x : x,range(2000,2025))),
            value=(2000, 2024),
        )
        model_yr_fltr = [start_year,end_year]
        submitted = st.form_submit_button('Submit')

    if submitted:
        t1 = time.time()
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        # chromedriver_path="/Users/venkatsagar/Documents/Python books/webdriver/chrome_driver"
        chromedriver_path = "/Users/venkatsagar/Applications/Anaconda/anaconda3/lib/python3.11/site-packages (1.4.1)/phantomjs"
        service = Service(service=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)


        # carBrand = st.carBrand
        # fltr1 = st.fltr1

        objM = data_output(driver,carBrand,fltr1,prceMlgeFltr,placeholder,model_yr_fltr)

        startPt = 0
        b = 0
        totalCt = 0
        # data_output()
        while True:
        # for i in range(3):
            # print("Current StartPt", startPt)
            listings = driver.find_elements(by=By.CLASS_NAME, value=car_list_main) #2
            endPt = len(listings)  # 46
            totalCt = len(listings)  # 46
            # print("Total length of the current Listing", totalCt)
            # print("Start and End points", (startPt, endPt))
            objM.CarData(listings, startPt, endPt)  # sp = 22, ep=46
            # time.sleep(1)
            startPt = endPt  # sp = 46
            if totalCt in range(22,30):  # totalMatches: replace after testing
                # print("length column list ",len(data_output.carInfo.keys()))
                # dict_cols = list(data_output.carInfo.keys())
                #
                # mydb.commit()
                # mycursor.close()
                # mydb.close()
                # df = pd.DataFrame.from_dict(data_output.carInfo())
                # df.to_csv("carmax_final.csv",index=False)
                break
            seeMorebtn = WebDriverWait(driver, 10000).until(EC.element_to_be_clickable(
                (By.XPATH, see_more_btn))) #1
            seeMorebtn.click()  # 46
            time.sleep(2)
            listings = driver.find_elements(by=By.CLASS_NAME, value=car_list_main) #2
            #     endPt = len(listings) # 46
            # print('length of listings after see more btn', len(listings))
        driver.close()


#hotfix
