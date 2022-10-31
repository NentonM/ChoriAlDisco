from selenium import webdriver
import time

url = 'https://www.hardgamers.com.ar/'
browser = webdriver.Firefox(executable_path="C:\webdriver\geckodriver.exe")

try:
    browser.get(url)
    #time.sleep(1)

    busqueda = browser.find_element("xpath", '//*[@id="input-search-text w-100"]')
    busqueda.click()
#INSERTAR NOMBRE DEL    ↓PROD↓
    busqueda.send_keys('Nvidia')
    browser.find_element("xpath", '/html/body/div/header/nav/div[1]/div[3]/form/div/div/button').click()
    #time.sleep(1)

    index = 0
#CANTIDAD DE PAG QUE ↓RECORRE
    for p in range(20):
        container = browser.find_element("xpath", '/html/body/div/div[4]/div/div[3]/div')
        t_container = container.find_elements("class name", 'col-6')
        #browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        change_pag = browser.find_element("xpath", '//a[contains(@aria-label, "Next")]')  
        for i in t_container:   
                index += 1         
                store = i.find_element("class name", 'subtitle').text
        #COMPARA ENTRE:     ↓MAXIMUS↓             ↓MEXX↓             ↓VENEX↓             ↓GEZATEK↓
                if store == 'Maximus' or store == 'Mexx' or store == 'Venex' or store == 'Gezatek':
                    name = i.find_element("class name", 'product-title').text
                    price_elements = i.find_elements("class name", 'product-price')
                    price = price_elements[1].text

                    print(f'{index}: {name} \n ${price} \n {store}')
                    print('______________________________________________________________________________')

                else:
                    pass 
        change_pag.click()
        time.sleep(1)
    browser.delete_all_cookies()    
    browser.quit()

except Exception as error:
    print(error)
    browser.quit()


