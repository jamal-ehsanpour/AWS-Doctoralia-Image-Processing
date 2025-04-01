from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
from selenium.common.exceptions import TimeoutException


#First create lists to store features of doctors
Name=[]
Gender=[]
Specilaty=[]
Price=[]
Address=[]
Review_num=[]
Online=[]
Languages=[]
Payment_methods=[]
Insurance=[]
Education=[]
Image=[]
Opinion=[]


# Replace 'path_to_chromedriver' with the path to your downloaded ChromeDriver executable
options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')


driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(10)

def open_window():
    #open a new window
    driver.execute_script("window.open('');")

    #switch to new window
    driver.switch_to.window(driver.window_handles[1])

def extract_doctor_links():
    doctor_links=driver.find_elements(By.XPATH , "//h3[contains(@class, 'h4 mb-0 flex-wrap')]/a" )
    urls=[doctor.get_attribute('href') for doctor in doctor_links]
    doctors_urls=[url for url in urls if 'strutture' not in url]
    
    return doctors_urls


def get_doctor_name():
    try :
        xpath="//div[contains(@class, 'unified-doctor-header-info__name')]"
        doctor_names=driver.find_elements(By.XPATH , xpath)
        for element in doctor_names :
            name=element.text
        return name
    except :
        return 'Not specified'


def male_or_female(name):
    if 'Dott.ssa' in name:
       return 'Female'
    else:
       return 'Male'


def get_price():
    try :
        xpath="//span[contains(@data-id, 'service-price')]"
        price_elements=driver.find_elements(By.XPATH , xpath)
        elements=[]
        for element in price_elements:
            if element.text != "" :
                elements.append(element.text.split())
        if len(elements) !=0 :
            price=elements[0][-2]
            return price
        else :
        
            return 'Nan'
    except :
        return 'Nan'


def get_reviews_num():
    try:
        xpath="//u[contains(@class, 'rating rating-lg')]"
        reviews_num_elements=driver.find_elements(By.XPATH , xpath)
        for element in reviews_num_elements:
            element=element.text.split()
            reviews_num=element[0]
        return reviews_num
    except :
        return 'Not specified'

def get_address(): 
    try :
        xpath="//div[contains(@class, 'col-md-8 col-lg-8 col-xl-9')]"
        address_elements= driver.find_elements(By.XPATH , xpath)
        elements=[]
        for element in address_elements: 
            if element.text != "" :
                elements.append(element.text.split('Dettagli'))
        address=elements[0][0]
        return address
    except :
        return 'Not specified'


def get_speciality():
    try:
        xpath="//span[contains(@class, 'text-truncate')]"
        especiality_elements=driver.find_elements(By.XPATH , xpath)
        elements=[]
        for element in especiality_elements:
            if element.text != "" :
                elements.append(element.text)
        especiality=elements[0]

        return especiality
    except :
        return 'Not specified'

def get_langueges():
        try: 
            see_more_xpath= "//button[contains(@class, 'btn btn-light btn-lg btn-block mt-3')]"
            element=driver.find_element(By.XPATH , see_more_xpath)
            driver.execute_script("arguments[0].click();", element)
            time.sleep(4)
            
            xpath="//ul[contains(@id, 'language')]"
            language_elements=driver.find_elements(By.XPATH , xpath)
            languages=[element.text.split() for element in language_elements if element.text != ""]
            return languages

        except Exception as e :
            return "Not specified"
    
    
def online_or_not(): 
    try:
        xpath="//a[contains(@class, 'nav-link')]"
        elements= driver.find_elements(By.XPATH , xpath)
        elements_text=[element.text for element in elements]
        if "Consulenza online" in elements_text :
            return "Yes"
        else :
            return "No"
    except :
        return 'Not specified'


def get_payment_methods() :
    try :
        xpath="//div[@data-test-id='payment-info']"
        elements=driver.find_elements(By.XPATH , xpath)
        payment_methods=[element.text for element in elements if element.text !=""]

        return payment_methods   
    except :
        return 'Not specified'




def get_insurance() :
    try:
        xpath="//div[@class='check-your-insurance']"
        insurance_elements=driver.find_elements(By.XPATH , xpath)
        insurance=[element.text for element in insurance_elements if element.text != ""]
        return insurance
    except :
        return "Not specified"



def education():
    try :
        xpath="//ul[contains(@id , 'school')]"
        education_elements=driver.find_elements(By.XPATH , xpath)
        educations=[element.text.split('•') for element in education_elements if element.text != ""]
        
        return educations
    
    except Exception:
        return "Not specified"
    



def get_images():
    try:
        xpath="//a[contains(@class, 'avatar unified-doctor-header-info__avatar')]"
        image_elements=driver.find_elements(By.XPATH , xpath)
        for element in image_elements:
            image_url=element.get_attribute('href')

        return image_url
    except:
        return "No Images"


def get_opinions():
    try :
        for i in range(5):
            try:
                load_more_button=driver.find_element(By.XPATH , "//a[contains(@data-id, 'load-more-opinions')]")
                driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(2)
            except Exception as e:
                break
        opinions_elements=driver.find_elements(By.XPATH , "//p[contains(@class, 'text-break')]")
        opinions=[element.text for element in opinions_elements]
        return opinions
    except : 
        return 'Not specified'

# Navigate to the Doctoralia Spain website

urls = ['https://www.miodottore.it/cerca?q=prima%20visita%20ginecologica&loc=&filters%5Bservices%5D%5B%5D=2901' , 'https://www.miodottore.it/cerca?q=prima%20visita%20ortopedica&loc=&filters%5Bservices%5D%5B%5D=2910'
       , 'https://www.miodottore.it/cerca?q=prima%20visita%20dermatologica&loc=&filters%5Bservices%5D%5B%5D=2883' , 'https://www.miodottore.it/cerca?q=prima%20visita%20oculistica&loc=&filters%5Bservices%5D%5B%5D=2906'
       , 'https://www.miodottore.it/cerca?q=prima%20visita%20urologica&loc=&filters%5Bservices%5D%5B%5D=2920' , 'https://www.miodottore.it/cerca?q=prima%20visita%20otorinolaringoiatrica&loc=&filters%5Bservices%5D%5B%5D=2913' 
       , 'https://www.miodottore.it/cerca?q=prima%20visita%20dentistica&loc=&filters%5Bservices%5D%5B%5D=2803' , 'https://www.miodottore.it/cerca?q=prima%20visita%20endocrinologica&loc=&filters%5Bservices%5D%5B%5D=2895'
       , 'https://www.miodottore.it/cerca?q=prima%20visita%20neurologica&loc=&filters%5Bservices%5D%5B%5D=2905' , 'https://www.miodottore.it/cerca?q=prima%20visita%20pediatrica&loc=&filters%5Bservices%5D%5B%5D=2914' 
       , 'https://www.miodottore.it/cerca?q=prima%20visita%20andrologica&loc=&filters%5Bservices%5D%5B%5D=2878' , 'https://www.miodottore.it/cerca?q=prima%20visita%20proctologica&loc=&filters%5Bservices%5D%5B%5D=2916' 
       , 'https://www.miodottore.it/cerca?q=prima%20visita%20gastroenterologica&loc=&filters%5Bservices%5D%5B%5D=2899' , 'https://www.miodottore.it/cerca?q=prima%20visita%20chirurgia%20estetica&loc=&filters%5Bservices%5D%5B%5D=2975'
       , 'https://www.miodottore.it/cerca?q=prima%20visita%20psichiatrica&loc=&filters%5Bservices%5D%5B%5D=2917'] 

for url in urls :
    driver.get(url)
    time.sleep(2)
   
    #First create lists to store features of doctors
    Name=[]
    Gender=[]
    Specilaty=[]
    Price=[]
    Address=[]
    Review_num=[]
    Online=[]
    Languages=[]
    Payment_methods=[]
    Insurance=[]
    Education=[]
    Image=[]
    Opinion=[]

    all_links=[]
    # Navigate to the next page if available
    for i in range(19):
        time.sleep(2)
        doctor_links=extract_doctor_links()
        all_links.extend(doctor_links)
        try:
            next_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'd-none d-md-inline-block mr-0-5')]")))
            next_button.click()   
        except Exception as e:
            print(f"End of pages.")
            break 

    for link in all_links:
        try:
            driver.get(link)
            time.sleep(2)
            WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//a[@data-test-id='dp-logo']")))
        except TimeoutException :
            print("Page load Timeout Occurred. Refreshing !!!")
            driver.refresh()
            time.sleep(3)
        name=get_doctor_name()
        Name.append(name)
        gender=male_or_female(name)
        Gender.append(gender)
        address=get_address()
        Address.append(address)
        price=get_price()
        Price.append(price)
        review_num=get_reviews_num()
        Review_num.append(review_num)
        specilaty=get_speciality()
        Specilaty.append(specilaty)
        image=get_images()
        Image.append(image)
        online=online_or_not()
        Online.append(online)
        payment_methods=get_payment_methods()
        Payment_methods.append(payment_methods)
        opinions=get_opinions()
        Opinion.append(opinions)
        insurance=get_insurance()
        Insurance.append(insurance)
        languages=get_langueges()
        Languages.append(languages)   
        educations=education()
        Education.append(educations)

    #Create a Dataframe from the lists we have created
    data={'Doctor Name' : Name , 'Specilaty' : Specilaty ,  'Gender' : Gender , 'Address' : Address , 'Price' : Price , 'Review Number' : Review_num , 'Languaegs' : Languages  ,  'Online' : Online   ,  'Payment_methods' : Payment_methods   , 'Insurance' : Insurance  , 'Education' : Education   , 'Opinion' : Opinion , 'Image Url' : Image }
    df=pd.DataFrame(data)
    df.to_csv('DoctraliaData-Italy-New.csv' , mode='a' , index=True , header=not pd.io.common.file_exists('DoctraliaData-Italy-New.csv')   , encoding='utf-8-sig')

    print(df.head())
    print(f"Data for {url} successfully saved.")
