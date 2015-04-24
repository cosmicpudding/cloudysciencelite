# Cloudy Science Lite - Wordclouds of arXiv astro-ph papers
# Lite version to generate wordles for individual papers and return word stats
# Vanessa A. Moss 24/04/2015
# 

import urllib
import os
import sys
import random
from pylab import *
from numpy import *
from scipy import misc
from matplotlib import rc
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['serif']})
import matplotlib.pyplot as pl
import unicodedata
import re
import time
import subprocess
import pyPdf
from wordcloud import WordCloud,STOPWORDS
import colorsys

# # List of ID names to process
# idnames = ["1306.3227"]

def cloudyscience(idnames):

    # colormap version
    def cmap_color_func(word, font_size, position, orientation,alph,random_state):
        colr = cm.jet(random.randint(0, 255))
        colr2 = colorsys.rgb_to_hsv(colr[0],colr[1],colr[2])
        sat = "70%" 
        var = "%s" % alph +"%"
        return "hsl(%d, %s, %s)" % (int(float(colr2[0])*255),sat,var)

    stp = ['1','2','3','4','5','6','7','8','9','0','10','et','al',
           'a','b','c','d','e','f','g','h','i','j',
           'k','l','m','n','o','p','q','r','s','t',
           'u','v','w','x','y','z']


    # Shuffle randomly
    random.shuffle(idnames)
    papernum = len(idnames)

    print 'PROCESSING PAPERS...'

    for idname in idnames:

        print idname

        # Make temp file
        os.system('rm -rf temp')
        os.system('mkdir temp')

        ######## Wordle post ########

        pdfpath = 'http://arxiv.org/pdf/'+idname
        out = open('temp/test.pdf','w')
        out.write(urllib.urlopen(pdfpath).read())
        out.flush()

        # Convert the PDF to text
        os.system('pdftotext temp/test.pdf > temp/test.txt')

        # Turn into a Wordle
        text = open('temp/test.txt').read()
        outname = '%s_wordle.png' % idname

        # Initalise wordcloud
        wc = WordCloud(stopwords=STOPWORDS.update(stp),width=500,height=500,prefer_horizontal=0.95,scale=1,color_func=cmap_color_func,font_path='DensiaSans.otf')

        # Check text    
        if len(text) > 0:
            wc.generate(text)
        else:
            print 'PDF text corrupted... skipping this paper'
            continue

        imshow(wc)
        axis("off")
        wc.to_file(outname)

    return 
    
