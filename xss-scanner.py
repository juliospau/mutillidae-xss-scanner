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

        links = self.crawl(input("\n-> Introduce la URL a escanear: "))

        print (f"{GREEN}[+] Escaneando la URL ...")
        
        level2 = []

        for l2 in links:
            if l2 not in level2:
                level2 += (self.crawl(l2))


        return level2
  
    def tryPayload(self, targetLinks, payload):

        print (f"{GREEN}[+] Escaneando los formularios y sus campos ...")
        
        self.targetLinks = targetLinks
        self.payload = payload
        triggeredForms = []

        # Por cada enlace se escanean los formularios y se prueba a enviar el payload establecido como valor de un campo tipo texto
        
        for i in self.targetLinks:
            response = requests.get(i)
            parsedHTML = bs(response.content, features="html.parser")
            filterForm = parsedHTML.findAll("form")

            for form in filterForm:

                if form not in triggeredForms:
                    triggeredForms.append(form)
                

                    action = form.get("action")
                    postURL = uritools.urijoin(i, action)

                    inputList = form.findAll("input")


                    postData = {}
            
                    for inputF in inputList:

                        inputName = inputF.get("name")
                        inputType = inputF.get("type")
                        inputValue = inputF.get("value")

                        if inputType == "text":
                            inputValue = self.payload

                            postData.update({inputF.get("name") : inputF.get("value")})
                
                        if inputType == "submit":
                            postData.update({inputF.get("name") : inputF.get("value")})


                    # Al finalizar la recolección de atributos y modificación de valores, se procede a enviar cada formulario

                    result = requests.post(postURL, data=postData)
                    parsedResponse = bs(result.content, features="html.parser")

                    # Si se encuentra el payload se indica como XSS reflejado

                    xss = re.findall(self.payload, str(parsedResponse))
                    if xss is not None:
                        print (f"{RED}[+] Posible XSS Reflejado en {CYAN}{i} {RED}en el formulario:{YELLOW}\n\n{form}\n")
                        print (f"{RED}[+] Razón: se ha podido reflejar el payload {CYAN}{self.payload} {RED} en el campo de entrada de texto\n")

                else:
                    pass



scann = scanner()
targetLinks = scann.crawlSecLevel()
scann.tryPayload(targetLinks, "<h1>POC23</h1>")
