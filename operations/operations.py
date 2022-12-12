from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def iniciarSesionTrivo(browser, email, password, projectName):
    try:
        projectNameField = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/form/div/div/input')) #This is a dummy element
        )
        projectNameField.send_keys(projectName)
        projectNameField.send_keys(Keys.ENTER)
    except Exception as e:
        print(e)
        browser.quit()

    try:
        #espero a que se cargue el campo de texto del correo
        emailField = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div/form/div/div[1]/div/input')) #This is a dummy element
        )
        emailField.send_keys(email)
        #encuentro el campo de texto para contrasenia
        passwordField = browser.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/form/div/div[2]/div/input')
        passwordField.send_keys(password)
        time.sleep(0.5)
        passwordField.send_keys(Keys.ENTER)
    except Exception as e: 
        print(e)
        browser.quit()


def orderListByDate(browser):
    try:
        #espero a que se cargue el campo de texto del correo
        lastDayContactHeader = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[2]/table/thead/tr/th[12]')) #This is a dummy element
        )
        lastDayContactHeader.click()
        lastDayContactHeader = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[2]/table/thead/tr/th[12]')) #This is a dummy element
        )
        lastDayContactHeader.click()
    except Exception as e: 
        print(e)
        browser.quit()