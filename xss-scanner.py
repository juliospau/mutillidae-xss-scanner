#!/usr/bin/env python

import re, requests, uritools
from bs4 import BeautifulSoup as bs
from colorama import init, Fore

init(autoreset=True)
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN

class scanner():

    def __init__(self, payload):
        self.payload = payload

    def crawl(self, url):

        self.url = url

        requestContent = requests.get(self.url)
        storeLinks = re.findall('(?:href=")(.*?)"', str(requestContent.content))
        targetLinks = []

        for i in storeLinks:
            link = uritools.urijoin(self.url, i)

            if link not in targetLinks and "#" not in link and link[-5:] == ".html" or link[-4:] == ".php" or link[-1] == "/" and self.url in link:
                targetLinks.append(link)

            else:
                pass


        return targetLinks

    def crawlSecLevel(self):

        # Se escanea la URL introducida y se pasa a un segundo nivel a partir de los enlaces encontrados

        inpLink = input("\n-> Introduce la URL a escanear: ")
        if inpLink[-1] != "/": inpLink += "/";
        
        links = self.crawl(inpLink)
        
        print (f"{GREEN}[+] Escaneando la URL ...")
        
        level2 = []


        for l2 in links:
            if l2 not in level2:
                level2 += (self.crawl(l2))


        return level2

    def xssForm(self, filterForm, link):

        self.link = link
        self.filterForm = filterForm
        triggeredForms = []

        for form in self.filterForm:

            if form not in triggeredForms:
                triggeredForms.append(form)
                

                action = form.get("action")
                postURL = uritools.urijoin(self.link, action)

                inputList = form.findAll("input")

                postData = {}
            
                method = form.get("method")
                    
                for inputF in inputList:

                    inputName = inputF.get("name")
                    inputType = inputF.get("type")
                    inputValue = inputF.get("value")

                    if inputType == "text":
                        inputValue = self.payload

                        postData.update({inputF.get("name") : inputValue})
                
                    if inputType == "submit":
                        postData.update({inputF.get("name") : inputF.get("value")})


                    # Al finalizar la recolección de atributos y modificación de valores, se procede a enviar cada formulario

                if method == "post":
                    result = requests.post(postURL, data=postData)
                    parsedResponse = bs(result.content, features="html.parser")

                # Si se encuentra el payload se indica como XSS reflejado

                    xss = re.findall(self.payload, str(parsedResponse))
                
                    for vuln in xss:
                        print (f"{RED}[+] Posible XSS Reflejado en {CYAN}{self.link} {RED}en el formulario:{YELLOW}\n\n{form}\n")
                        print (f"{RED}[+] Razón: se ha podido reflejar el payload {CYAN}{self.payload} {RED} en el campo de entrada de texto\n")

                else:
                    pass


    def tryPayload(self, targetLinks):

        print (f"{GREEN}[+] Escaneando los formularios y sus campos ...")
        
        self.targetLinks = targetLinks
        # Por cada enlace se escanean los formularios y se prueba a enviar el payload establecido como valor de un campo tipo texto
        
        for link in self.targetLinks:
            response = requests.get(link)
            parsedHTML = bs(response.content, features="html.parser")
            filterForm = parsedHTML.findAll("form")
        
            self.xssForm(filterForm, link)


scann = scanner("<h1>POC23</h1>")
targetLinks = scann.crawlSecLevel()
scann.tryPayload(targetLinks)

