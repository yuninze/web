from collections import Counter
import sys
import urllib
import random
import webbrowser

from konlpy.tag import Hannanum
from lxml import html
import pytagcloud

openurl=urllib.request.urlopen
hex_gen=lambda:random.randint(0,255)
hex_val=lambda:(hex_gen(),hex_gen(),hex_gen())

#get url response block
def gdstrb(text):
    
    return None