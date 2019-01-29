#import os
import sys
import time
import datetime
import string
#import RPi.GPIO as GPIO
from weather import Weather, Unit#pip install weather-api
import feedparser #pip install feedparser
from html.parser import HTMLParser
from tkinter import *
from PIL import Image, ImageTk


#Weather Icons designed by Ashley Jager, available under both the MIT and GPL license.
#https://peter.build/weather-underground-icons/


#if os.getuid() != 0:
#    print('ERROR: Need to run as root')
#    sys.exit(1)

TESTGLOB = 9
WeatherIcon = "fog"

parsed_article = 0
WOEID_loc_amherst = 12758287 #WOEID for zip 01003 via http://weather.yahoo.com.
WOEID_loc_worcester = 12758525 #for 01602    
WOEID_loc_ma = 2347580 #for MA          

weather = Weather(unit=Unit.FAHRENHEIT) 
#weather = Weather(unit=Unit.CELSIUS)

ycc2rip  = { #Maps Yahoo Condition codes to relative icon paths
    '0'  : "../res/icon/windy.png",     #tornado
    '1'  : "../res/icon/windy.png",  #tropical storm
    '2'  : "../res/icon/windy.png",  #hurricane
    '3'  : "../res/icon/tstorms.png", #severe thunderstorms
    '4'  : "../res/icon/tstorms.png", #thunderstorms
    '5'  : "../res/icon/sleet.png", #mixed rain and snow
    '6'  : "../res/icon/sleet.png", #mixed rain and sleet
    '7'  : "../res/icon/tstorms.png", #mixed snow and sleet
    '8'  : "../res/icon/sleet.png",  #freezing drizzle
    '9'  : "../res/icon/sleet.png",  #drizzle
    '10' : "../res/icon/sleet.png",  #freezing rain
    '11' : "../res/icon/showers.png", #showers
    '12' : "../res/icon/showers.png", #showers
    '13' : "../res/icon/lightflurries.png", #snow flurries
    '14' : "../res/icon/flurries.png", #light snow showers
    '15' : "../res/icon/blowingsnow.png", #blowing snow
    '16' : "../res/icon/snow.png", #snow
    '17' : "../res/icon/hail.png", #hail
    '18' : "../res/icon/sleet.png", #sleet
    '19' : "../res/icon/hazy.png", #dust
    '20' : "../res/icon/fog.png", #foggy
    '21' : "../res/icon/hazy.png",#haze
    '22' : "../res/icon/smoky.png", #smoky
    '23' : "../res/icon/wind.png",#blustery
    '24' : "../res/icon/wind.png", #windy
    '25' : "../res/icon/cold.png", #cold
    '26' : "../res/icon/cloudy.png", #cloudy
    '27' : "../res/icon/mostlycloudynight.png", #mostly cloudy (night)
    '28' : "../res/icon/mostlycloudy.png", #mostly cloudy (day)
    '29' : "../res/icon/partlycloudynight.png", #partly cloudy (night)
    '30' : "../res/icon/partlycloudy.png", #partly cloudy (day)
    '31' : "../res/icon/clearnight.png", #clear (night)
    '32' : "../res/icon/clear.png", #clear (day)
    '33' : "../res/icon/clearnight.png", #fair (night)
    '34' : "../res/icon/sunny.png", #fair (day)
    '35' : "../res/icon/mixedrainhail.png", #mixed rain and hail
    '36' : "../res/icon/hot.png", #hot
    '37' : "../res/icon/tstorms.png", #isolated thunderstorms
    '38' : "../res/icon/tstorms.png", #scattered thunderstorms
    '39' : "../res/icon/tstorms.png", #scattered thunderstorms
    '40' : "../res/icon/chancerain.png", #scattered showers
    '41' : "../res/icon/heavysnow.png", #heavy snow
    '42' : "../res/icon/chancesnow.png", #scattered snow showers
    '43' : "../res/icon/heavysnow.png",  #heavy snow
    '44' : "../res/icon/partlycloudy.png", #partly cloudy
    '45' : "../res/icon/tstorms.png", #thundershowers
    '46' : "../res/icon/flurries.png",  #snow showers
    '47' : "../res/icon/tstorms.png", #isolated thundershowers
    '3200' : "../res/icon/unknown.png" #unknown
}


#GPIO.setmode(GPIO.BCM)
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class news_HTMLParser(HTMLParser):
    def handle_data(self, data):
        if(len(data)>200):
            global parsed_article 
            parsed_article= data



class ImageT(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        image = Image.open("../res/icon/" + WeatherIcon + ".png")
        #image = image.resize((127, 127), Image.ANTIALIAS)
        #image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)

class WeatherBox(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.weatherbox = Frame(self, bg="black")
        self.weatherbox.pack(side=LEFT, anchor=S)
        ###
        self.refresh_weather()

    def refresh_weather(self):
        cur_cond_text = "unknown"
        cur_cond_code = '3200'
        cur_temp = 0
        hig_temp = 0
        low_temp = 0 
        sunset = ""

        #try:
        lookup = weather.lookup(WOEID_loc_amherst) 
        
        #print(lookup._weather_data['item']['forecast'])

        current = lookup.condition
        cur_cond_text = current.text
        cur_cond_code = current.code
        cur_temp = current.temp
        forecast = lookup.forecast 
        hig_temp = forecast[0].high
        low_temp = forecast[0].low
        astro = lookup.astronomy
        sunset = astro['sunset']
       # except:
            #print("COULD NOT FETCH WEATHER DATA, PROCEEDING")

            

        weather_iconBox = Frame(self.weatherbox, bg="black") 
        weather_iconBox.pack(side=TOP, anchor=CENTER)
        #############
       
        weather_textBox = Frame(self.weatherbox, bg="black")
        weather_textBox.pack(side=BOTTOM)
        L_weather_textBox = Frame(weather_textBox, bg="black")
        L_weather_textBox.pack(side=LEFT)
        R_weather_textBox = Frame(weather_textBox, bg="black")
        R_weather_textBox.pack(side=RIGHT, anchor=S)
        RL_weather_textBox = Frame(R_weather_textBox, bg="black", padx=8)
        RL_weather_textBox.pack(side=LEFT, anchor=S)
        RR_weather_textBox = Frame(R_weather_textBox, bg="black", padx=8)
        RR_weather_textBox.pack(side=RIGHT, anchor=S)
        Sun_textBox = Frame(RR_weather_textBox, bg="black", padx=8)
        Sun_textBox.pack(side=RIGHT, anchor=S)
       
   
        #GET WEATHER INFO

        weatherIconSplash = Label(weather_iconBox, text=cur_cond_text, font=('Arial', 18, 'bold'), fg='white', bg='black')
        weatherIconSplash.pack(side=LEFT)

        rawimage = Image.open(ycc2rip[cur_cond_code])
        rawimage = rawimage.resize((300, 300), Image.ANTIALIAS)
        weathericon = ImageTk.PhotoImage(rawimage)
        weatherIconLbl = Label(weather_iconBox, bg='black', image=weathericon)
        weatherIconLbl.image = weathericon
        weatherIconLbl.pack(side=TOP, anchor=CENTER)
        
        #Label Frames:
        CURweatherLbl= LabelFrame(L_weather_textBox, text="Now:", font=('Arial',36,'bold'), fg="white", bg="black", bd=5, labelanchor='nw')
        HIGHweatherLbl= LabelFrame(RL_weather_textBox, text="High:", font=('Arial',18,'bold'), fg="white", bg="black", bd=3, labelanchor='nw')
        LOWweatherLbl= LabelFrame(RR_weather_textBox, text="Low:", font=('Arial',18,'bold'), fg="white", bg="black", bd=3, labelanchor='nw')

        SunsetLbl= LabelFrame(Sun_textBox, text="Today's sunset:", font=('Arial',18,'bold'), fg="white", bg="black", bd=3, labelanchor='nw')

        #Temps:
        CURweatherTemp = Label(CURweatherLbl, text=str(cur_temp) +"°", font=('Arial', 128, 'bold'), fg="white", bg="black")
        HIGHweatherTemp = Label(HIGHweatherLbl, text=str(hig_temp) +"°", font=('Arial', 36), fg="white", bg="black")
        LOWweatherTemp = Label(LOWweatherLbl, text=str(low_temp) +"°", font=('Arial', 36), fg="white", bg="black")
        
        SunsetText = Label(SunsetLbl, text=sunset, font=('Arial', 36), fg="white", bg="black")

        #Pack:
        CURweatherTemp.pack()
        HIGHweatherTemp.pack(side=TOP, anchor=N)
        LOWweatherTemp.pack(side=TOP, anchor=N)
        CURweatherLbl.pack()
        HIGHweatherLbl.pack(side=LEFT, anchor=S)
        LOWweatherLbl.pack(side=RIGHT, anchor=S)

        SunsetText.pack()
        SunsetLbl.pack(side=RIGHT,anchor=S)




class DateBox(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.datebox = Frame(self, bg="green", padx=2,pady=2)
        self.datebox.pack(side=LEFT, anchor=CENTER)
        ###
        self.refresh_date()

    def refresh_date(self):
        curdate = datetime.datetime.now()
        curdate_str = curdate.strftime("%A, %B ")

        if(4<= (curdate.day) %100<=20):
            curdate_str += str(curdate.day) + "th" 
        else:
            curdate_str += {1:"st",2:"nd",3:"rd"}.get((curdate.day)%10, "th")


        global TESTGLOB
        if(TESTGLOB == 9):
            print(feedparser.parse('https://rayshobby.net/scripts/python/getfortune.py?t=\'+Date.now(),true'))

        datetext = Label(self, text= curdate_str, font=('Helvetica', 48, 'bold'), fg="white", bg="black")
        datetext.pack(side = LEFT, anchor=N)

class NewsBox(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.newsbox = Frame(self, bg="black", padx=2,pady=2)
        self.newsbox.pack(side=BOTTOM, anchor=S)
        ###
        self.refresh_news()

    def refresh_news(self):
        for widget in self.newsbox.winfo_children():
                widget.destroy()
        try:
            newsfeed = feedparser.parse('https://news.google.com/news?ned=us&output=rss')
       
            for post in newsfeed.entries[1:5]:
                headline = NewsHeadline(self.newsbox, post.title)
                headline.pack(anchor=W) 
                article = NewsArticle(self.newsbox, post)
                article.pack(anchor=CENTER)
        except:
            print("COULD NOT FETCH NEWS DATA, PROCEEDING")
    
        #    self.after(5, self.refresh_news)

class NewsHeadline(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')

        image = Image.open("../res/icon/bullet_pt.png")
        image = image.resize((20, 20), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)

        if(len(event_name) > 95):
            event_name = event_name[:95] + "..."

        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', 16, 'bold'), fg="white", bg="black")
        self.eventNameLbl.pack(side=LEFT, anchor=N)
            
class NewsArticle(Frame):
    def __init__(self, parent, entry=""):
        Frame.__init__(self, parent, bg='black')
        p = news_HTMLParser()
        p.feed(entry.summary)
        p.close()
        output_data = parsed_article[:len(parsed_article)-1] + "..."

        self.eventText = Text(self, font=('Helvetica', 14), fg="white", bg="black", bd=0, wrap=WORD, height=5)
        self.eventText.insert(INSERT, output_data)
        self.eventText.pack(side=RIGHT, anchor=N)

class FullscreenWindow:

    def __init__(self):
        #SETUP:
        self.window = Tk()
        self.window.title("DumbMirror")
        self.state = False
        self.window.configure(background='black')

        #KEYBINDS:
        self.window.bind("<Return>", self.toggle_fullscreen)
        self.window.bind("<Escape>", self.end_fullscreen)

        #FRAMES:
        self.NFrame = Frame(self.window, background = 'black')
        self.SFrame = Frame(self.window, background = 'black')

        self.NFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.SFrame.pack(side = BOTTOM, fill=BOTH, expand = YES) 

        #GREETING
        #self.greeting = Label(self.NFrame, text="Hello", font=('Helvetica', 40, 'bold'), fg="white", bg="black")
        #self.greeting.pack(side=TOP, anchor=CENTER, pady=20)

        #WEATHER:
        self.weather = WeatherBox(self.SFrame)
        self.weather.pack(side=LEFT, anchor=S, padx=30, pady=30)

        #NEWS:
        self.news = NewsBox(self.SFrame)
        self.news.pack(side=RIGHT, anchor=E, padx=30, pady=0)

        #DATE:
        self.date = DateBox(self.NFrame)
        self.date.pack(side=LEFT, anchor=N, padx=30, pady=30)


    def toggle_fullscreen(self, event=None):
        self.state = not self.state  
        self.window.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.window.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    mirror = FullscreenWindow()
    mirror.toggle_fullscreen
    LOOPING = True
    while LOOPING:
        mirror.window.update()
        #time.sleep(1)

        #if USER_INPUT == "exit":
        #    mirror.window.quit()
        #    LOOPING = False;
       # else:

    #mirror.window.mainloop()
