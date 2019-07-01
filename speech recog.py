import mysql.connector
import speech_recognition as sr 
import sys
import pygame
import time


def lookup_table(rxID):
    conn = mysql.connector.connect(host='localhost', 
                                   database='rx_info',
                                   user='root',
                                   password='root')
    cursor = conn.cursor()
    connection_string = "SELECT sig, quantity, days_of_supply, patient_id, prescriber_id, product_id from rx where rx_id=%s" %(rxID)
    cursor.execute(connection_string)
    row1 = cursor.fetchall()
    for row in row1:
        sig = row[0]
        qty = row[1]
        days_supply = row[2]
        patient_id = row[3]
        prescriber_id = row[4]
        product_id = row[5]
    
    connection_string = "SELECT firstname, lastname FROM patient WHERE patient_id=%s" %(patient_id)
    cursor.execute(connection_string)
    row2 = cursor.fetchall()
    for row in row2:
        patient_name = str(row[0])+','+str(row[1])
    
    connection_string = "SELECT npi FROM prescriber WHERE prescriber_id=%s" %(prescriber_id)
    cursor.execute(connection_string)
    row3 = cursor.fetchall()
    for row in row3:
        npi = row[0]
    
    connection_string = "SELECT productname FROM product WHERE product_id=%s" %(product_id)
    cursor.execute(connection_string)
    row4 = cursor.fetchall()
    for row in row4:
        drug = row[0]
    
    table_df = {"name":patient_name,"drug_name":drug,"qty":qty,"days_supply":days_supply,"SIG":sig,"NPI":npi}   
    
    if(conn.is_connected()):
        cursor.close()
        conn.close()
        
    return(table_df)
    
#df=lookup_table(115)    

from gtts import gTTS
import os 

#speech to text
def speech_to_text():  
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Speak:")  
        #r.adjust_for_ambient_noise(source)                                                                                 
        audio = r.listen(source)   
        try:
            user_question=r.recognize_google(audio)
            print(r.recognize_google(audio))
            if user_question=="repeat":
                #speech_to_text("Take one tablet by mouth daily")
                text_to_speech(dic['SIG']+'for'+str(dic['days_supply'])+'days')
            elif 'chewable' in user_question:
                text_to_speech("No it is not chewable")
        except sr.UnknownValueError:
            print("didn't understand speech")  
 
#text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    i = 8
    while os.path.exists("audio%s.mp3" % i):
        i += 1
    aud="audio%s.mp3" %i    
    tts.save(aud)        
    pygame.mixer.init()
    pygame.mixer.music.load(aud)
    pygame.mixer.music.play()
    #os.close("audio2.mp3")
    

if(__name__=='__main__'):
    dic=lookup_table(sys.argv[1])
    text_to_speech("hello" + dic['name'])
    time.sleep(1)
    text_to_speech(dic['SIG']+'for'+str(dic['days_supply'])+'days')
    time.sleep(3)
    speech_to_text()
    
    
    
    