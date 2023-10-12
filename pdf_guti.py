# Author : InferiorAK
# 1st Release : 13th October 2023 01:08AM
# Version : 1
# Tool : Google Drive Private Pdf downloader


# MIT License

# Copyright (c) 2023 Mi Taseen

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# colors
r = "\x1b[1;31m"
g = "\x1b[1;32m"
y = "\x1b[1;33m"
b = "\x1b[1;34m"
p = "\x1b[1;35m"
c = "\x1b[1;36m"
w = "\x1b[1;37m"
e = "\033[0m"


import re
import os
import asyncio
from time import perf_counter
try:
    import httpx
    from PIL import Image
    import colorama
except ImportError:
    print(f"{w} [+] {y}Please Install Requirements First!{e}")



__import__("colorama").just_fix_windows_console() if os.name == "nt" else None

cls = lambda: os.system("clear") if os.name == "posix" else (os.system("cls") if os.name == "nt" else None)
cls()

def banner():
    bnnr = """
    ╔─────═════════════════════════════════════════─────┐
    ║ This is a                                         ║
    ║    'Google Drive Private PDF Downloader Tool'     ║
    ║        by "InferiorAK"                            ║
    ║                                                   ║
    ║ Author      : InferiorAK                          ║
    ║ Tool        : PDF Guti                            ║
    ║ Version     : 1.0                                 ║
    ║ Github      : github.com/InferiorAK               ║
    ║ Youtube     : youtube.com/@InferiorAK             ║
    ║ Twitter     : twitter.com/InferiorAK              ║
    ║ Facebook    : fb.com/InferiorAK                   ║
    ║                                                   ║
    ║    Free to use and learn. Not for sell and steal! ║
    └─────══════════════════════════════════════════────╝
    """
    print(f"{b}{bnnr}")

async def download_engine(num, url):
    async with httpx.AsyncClient() as network:
        try:
            res = await network.get(url)
            if res.status_code == 200:
                data = res.content
                if os.path.exists("Saved"):
                    with open(f"Saved/page_{str(num+1)}.png", "wb") as file:
                        file.write(data)
                        file.close()
                    # print(f"Page {num+1} Downloaded! {res.status_code}")
                else:
                    os.makedirs("Saved/")
                    with open(f"Saved/page_{str(num+1)}.png", "wb") as file:
                        file.write(data)
                        file.close()
                    # print(f"Page {num+1} Downloaded! {res.status_code}")
        except:
            pass
            
async def main(link, width, tp):
    pages = []
    for page in range(0, tp):
        edit = link[link.find("&page="):]    # getting the index value
        url = link.replace(edit, f"&page={page}&skiphighlight=true&w={str(width)}")
        pages.append(url)
    tasks = [download_engine(num, url) for num, url in enumerate(pages)]
    await asyncio.gather(*tasks)
    
def img2pdf(pdf_name, tp):
    img = [Image.open(f"Saved/{img}") for img in os.listdir("Saved/")[0:tp]]
    img[0].save(
        f"Saved/{pdf_name}",    # output path
        "PDF",
        save_all=True,
        append_images=img[1:],
        resolution=100.0,
        quality=95,
    )

if __name__ == "__main__":
    banner()
    
    while True:
        link = str(input(f"{w} [+] {c}Input URL:{e} "))
        link_pattern = re.compile(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$')
        validate = bool(link_pattern.match(link))
        if validate == True:
            break
        else:
            print(f" {r}Invalid URL!{e}")
            continue
        
    while True:
        try:
            tp = int(input(f"{w} [+] {c}Total Pages:{e} "))
            if tp >= 1:
                pass
            else:
                print(f" {r}Invalid Input")
                continue
            break
        except ValueError as VE:
            print(f" {r}{VE}\nInvalid Input. Try Again!{e}")

    while True:
        try:
            width = int(input(f"{w} [+] {c}Input width [ 600 < Recommended <= 3000]:{e} "))
            if 0 < width <= 5000:
                pass
            else:
                print(f" {y}Width Can't be greater than 5000px and less than 1!{e}")
                continue
            break
        except ValueError as VE:
            print(f" {r}{VE}\nInvalid Input. Try Again!{e}")
            
    while True:
        pdf_name = str(input(f"{w} [+] {c}Output PDF name:{e} "))
        if pdf_name != "":
            break
        else:
            print(f" {r}PDF name can't be blank!{e}")
            continue

    s = perf_counter()
    asyncio.run(main(link, width, tp))
    img2pdf(pdf_name=pdf_name, tp=tp)
    print(f"{w} [+] {g}PDF Downloaded Successfully! Don't Forget to follow me ( https://github.com/InferiorAK ){e}")
    e = perf_counter()
    print(f"{w} [+] {c}Time taken: {e-s} sec")