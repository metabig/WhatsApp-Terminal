#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from subprocess import call

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def clear(): 
    _ = call('clear' if os.name =='posix' else 'cls') 

def orderContacts(contacts):
    array = []
    array.append(str(contacts[0].text))
    for contact in reversed(contacts):
        if (str(contact.text) != str(contacts[0].text)):
            array.append(str(contact.text))
    array = array[:-1]
    return array

def loadWhatsApp():
    options = Options()
    options.add_argument('user-data-dir=/home/metabig/projectX/User_Data')
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.implicitly_wait(15)
    driver.get('https://web.whatsapp.com/')
    driver.find_element_by_class_name('app')
    return driver

def getContacts(driver):
    contacts = driver.find_elements_by_xpath("//div[@class='KgevS']/div/span")
    contacts = orderContacts(contacts)
    return contacts

def fuzeArray(array):
    result = ""
    for s in array:
        result += s + " "
    result = result[:-1]
    return result


def selectOption(name):
    r = []
    while len(r) == 0:
        r = list(map(str, input(color.GREEN + color.BOLD + name + color.END + color.END + "$ ").split()))
    return r

def printHelp():
    print("\tcat\tPrint messages with the contact")
    print("\tcd\tSelect of a contact (-n <number>) to select it by number")
    print("\tm\tType a message")
    print("\tls\tDisplay Contacts")
    print("\tclear\tClear the screen")
    print("\texit\tExit WhatsApp-Terminal")

def printMessages(driver):
    for i in range(10, -1, -1):
        elem = driver.find_element_by_xpath('//div[@class = "_1ays2"]/div[last()-{}]'.format(i))
        print (elem.text)

def printContacts(contacts):
    for c in range(0, len(contacts)):
        print(str(c) + ".\t" , contacts[c])

def sendMessage(driver, option):
    if len(option) == 1:
        msg = input("Type " + str(name) + ": ")
    else:
        option.pop(0)
        msg = fuzeArray(option)
    msg_box = driver.find_element_by_class_name('_13mgZ')
    msg_box.send_keys(msg)
    button = driver.find_element_by_class_name('_3M-N-')
    button.click()
    driver.find_element_by_xpath('//div[@class = "_1ays2"]/div[last()]/div/div/div/div[last()]/div/div/span[@data-icon="msg-check"]')

def accessContact(driver, option, contacts, name):
    if len(option) == 1:
        NewName = input('Chat: ')
        if NewName in contacts:
            name = NewName
    else:
        option.pop(0)
        if option[0] == "-n":
            NewName = contacts[int(option[1])]
        else:
            NewName = fuzeArray(option)

    if NewName in contacts:
        name = NewName
        user = driver.find_element_by_xpath('//span[contains(text(),"{}")]'.format(name))
        user.click()
        driver.execute_script("document.getElementById('pane-side').scroll(0,0)")
    else:
        print("Contact", NewName , "not found")
    return name

def exitProgram(driver):
    print('Closing WhatsApp...')
    driver.close()
    print('See you, hipster!')
    exit()

def start():

    print("Loading WhatsApp")
    driver = loadWhatsApp()
    contacts = getContacts(driver)
    name = ""
    print(color.GREEN  + 'Welcome to' + color.BOLD +
            ' WhatsApp-Terminal'+ color.END 
            + color.GREEN + ' by Metabig' + color.END)

    print("Type 'help' for help")
    option = selectOption(name)

    while option[0] != "exit":
        if option[0] == "ls":
            printContacts(contacts)

        elif option[0] == "cd":
            name = accessContact(driver, option, contacts, name)
            
        elif option[0] == "m":
            sendMessage(driver, option)
            
        elif option[0] == "cat":
            if name != "":
                printMessages(driver)
            else:
                print("No contact selected")

        elif option[0] == "clear":
            clear()

        elif option[0] == "help":
            printHelp()

        else: 
            print("{}: Command not found".format(option[0]))
            print("Type 'help' for help")
        
        option = selectOption(name)

    exitProgram(driver)
    print("Not displayed Message")

start()
