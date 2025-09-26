import datetime
import random
import subprocess
import sys
import textwrap
import time
import streamlit as st
from tkinter import *

var=st.session_state
hl=st.divider
if "name" not in var:
    var.name=None
if "age_group" not in var:
    var.age_group=None
if "gender" not in var:
    var.gender=None
if "application" not in var:
    var.application=0
if "mode" not in var:
    var.mode="DND"
if "timelist" not in var:
    var.timelist=[]
if "sleeptime" not in var:
    var.sleeptime=None
if "wi_final" not in var:
    var.wi_final=None
if "rl2" not in var:
    var.rl2=[]
if var.application==0:
    page_bgx = """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #A101EB, #01EBD0);  /* blue to green */
        background-size: cover;
    }
    button {
        background: blue;
    }
    </style>
    """
    st.markdown(page_bgx, unsafe_allow_html=True)
    age_groups=["6-12","13-18","19-30","30-50","50+"]
    st.write("<h2 style='color:white;'>Just a Few Details Before we Dive In...</h2>",unsafe_allow_html=True)
    var.name=st.text_input(" ",placeholder="Name")
    hl()
    st.markdown('<p style="color:white;">Age Group</p>', unsafe_allow_html=True)
    var.age_group=st.selectbox("Age Group",age_groups,label_visibility="collapsed")
    hl()

    st.markdown('<p style="color:white;">Gender</p>', unsafe_allow_html=True)
    var.gender=st.selectbox("Gender",["male","female"],label_visibility="collapsed")
    hl()
    st.markdown('<p style="color:white;">Sleep Time (Hour)</p>', unsafe_allow_html=True)
    var.sleephour=st.selectbox("Sleep Time (Hour)",["1","2","3","4","5","6","7","8","9","10","11","12"],label_visibility="collapsed")
    hl()
    st.markdown('<p style="color:white;">Sleep Time (Minute)</p>', unsafe_allow_html=True)
    var.sleepminute=st.selectbox("Sleep Time (Minute)",["00","15","30","45"],label_visibility="collapsed")
    hl()
    st.markdown('<p style="color:white;">Sleep Time (AM/PM)</p>', unsafe_allow_html=True)
    var.sleepmeridien=st.selectbox("Sleep Time (AM/PM)",["AM","PM"],label_visibility="collapsed")
    hl()
    var.male_water_intake = [1.75, 2.50, 2.75, 2.75, 2.75]    # in liters/day
    var.female_water_intake = [1.50, 1.75, 2.00, 2.00, 2.00]
    if var.gender=="male":
        var.wi=var.male_water_intake[age_groups.index(var.age_group)]*1000
    if var.gender=="female":
        var.wi=var.female_water_intake[age_groups.index(var.age_group)]*1000
    var.whole=[]
    for i in range(250,5250,250):
        var.whole.append(str(i))
    st.markdown(f'<p style="color:white;">Water Target: (Ideally Suggested for you {int(var.wi)} ml)</p>', unsafe_allow_html=True)
    var.wi_final=st.selectbox("Water Target: (Ideally Suggested for you "+str(int(var.wi))+" ml)",var.whole,var.whole.index(str(int(var.wi))),label_visibility="collapsed")
    var.wi_final=int(var.wi_final)
    var.completed=0
    var.final_name=var.name
    if st.button("Advance"):
        if var.name.replace(" ","")=="":
            popen_code=textwrap.dedent(f"""from tkinter import *\nwarning_n=Tk()\nwarning_n.geometry('700x100+410+90')\nwarning_n.config(bg='blue')\nwarning_n.attributes("-topmost",True)\nwarning_n.overrideredirect(True)\nLabel(warning_n,text="Seems like you have forgot to mention your name!",font=("Arial",20),bg='blue',fg='white').pack()\nButton(warning_n,text="Dismiss",font=("Arial",20),bg='green',fg='white',activebackground='green',activeforeground='white',command=lambda: warning_n.destroy()).pack()\nwarning_n.mainloop()""")
            subprocess.Popen([sys.executable,"-c",popen_code])
        else:
            var.application=1
            st.rerun()



if var.application==1:
    var.init_time=datetime.datetime.now()
    if var.sleepmeridien=="PM":
        var.meridien_adjustment=12
    else:
        var.meridien_adjustment=0
    var.hour_meridien=int(var.sleephour)+var.meridien_adjustment
    var.timeleft=int((var.hour_meridien-var.init_time.hour)*60)+(int(var.sleepminute)-30-var.init_time.minute)
    if var.timeleft<=0:
        var.application=3
        st.rerun()
    else:
        var.d=250
        var.n=var.wi_final/var.d
        var.per=int(var.timeleft/var.n)
        print(var.timeleft,var.per)
        if round(var.per,-1)<30:
            var.application=3
            st.rerun()
        var.reminder_list=[]
        for item in range(1,int(var.n+1)):
            var.reminder_list.append([int(((var.init_time.hour*60)+var.init_time.minute+(item*var.per))//60),int(((var.init_time.hour*60)+var.init_time.minute+(item*var.per))%60)])
        print(var.reminder_list)
    motivating_words=["Come on","You can do it","Keep pushing","Nail it"]
    code=f"""
    from tkinter import *
    import datetime
    import pygame
    warning_n=Tk()
    # warning_n.geometry('500x100+1400+650')
    warning_n.config(bg='white')
    list_time={var.reminder_list}
    def update():
        time=datetime.datetime.now()
        for i in list_time:
            if time.hour==i[0]:
                if time.minute==i[1]:
                    warning_n.deiconify()
                    message['text']='{random.choice(motivating_words)}! Take your Glass of Water!'
                    warning_n.attributes("-topmost",True)
                    pygame.mixer.init()
                    pygame.mixer.music.load("closure-542.mp3")
                    pygame.mixer.music.play()
                    del list_time[0]
        warning_n.after(100,update)
    
    # warning_n.overrideredirect(True)
    message=Label(warning_n,text="Take your Glass of Water!",font=("Arial",20),bg='blue',fg='white')
    message.pack()
    Button(warning_n,text="Dismiss",font=("Arial",20),bg='green',fg='white',activebackground='green',activeforeground='white',command=lambda: warning_n.withdraw()).pack()
    update()
    warning_n.withdraw()
    warning_n.mainloop()
    """
    popen_code=textwrap.dedent(code)
    subprocess.Popen([sys.executable,"-c",popen_code])

    page_bg = """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0A48F5, #4DF50A);  /* blue to green */
        background-size: cover;
    }
    button {
        background: blue;
    }
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)
    st.write(f"<h1 style='color: white;'>Hi {var.name}!</h1>",unsafe_allow_html=True)
    st.write(f"<h4 style='color: white;'>Today's Target: {int(var.wi_final)} ml</h4>",unsafe_allow_html=True)
    var.bar=st.progress(0)
    init="90deg, #0A48F5, #4DF50A"
    end="90deg, #FF8C42, #FF4B2B"
    st.markdown("""
<style>
/* Change the progress bar height */
div[data-testid="stProgress"] > div > div > div {
    height: 30px;
    border-radius: 15px;
}

/* Change the progress bar color */
div[data-testid="stProgress"] > div > div > div > div {
    background: linear-gradient("""+init+""");
}
</style>
""", unsafe_allow_html=True)
    if st.button("Quick +250 ml"):
        var.completed+=250
        
        if var.completed/var.wi_final<=0.6:
            main=init
        else:
            main=end
        st.markdown("""
    <style>
    /* Change the progress bar height */
    div[data-testid="stProgress"] > div > div > div {
        height: 30px;
        border-radius: 15px;
    }

    /* Change the progress bar color */
    div[data-testid="stProgress"] > div > div > div > div {
        background: linear-gradient("""+main+""");
    }
    </style>
    """, unsafe_allow_html=True)
        var.bar.progress(var.completed/var.wi_final)
        st.write(f"<h4 style='color: white;'>Water Drunk: {var.completed} ml</h4>",unsafe_allow_html=True)
        st.write(f"<h4 style='color: white;'>Percentage: {round((var.completed/var.wi_final)*100,1)}</h4>",unsafe_allow_html=True)
        time.sleep(0.05)
        now=datetime.datetime.now()
        ampm=""
        hour=""
        if now.hour>=12:
            hour=now.hour-12
            ampm="P.M."
        else:
            hour=now.hour
            ampm="A.M."
        var.timelist.append(f"{now.day}/{now.month}/{now.year} - {hour}:{now.minute} {ampm}")
        print(var.timelist)
        st.write("<br><br><h4 style='color: white;'>Time Record</h4>",unsafe_allow_html=True)
        for x in var.timelist[::-1]:
            st.write(f"<h5 style='color: white;'>{x}</h5>",unsafe_allow_html=True)
        if var.wi_final-var.completed<=0:
            var.application=2
            st.rerun()
    st.write("<h3 style='color: white;'>Time Reminders</h3>",unsafe_allow_html=True)
    
    for m in var.reminder_list:
        show_hour=m[0]
        show_minute=m[1]
        show_ampm="A.M."
        if show_hour>12:
            show_hour=show_hour-12
            show_ampm="P.M."
        else:
            show_ampm="A.M."
if var.application==2:
    page_bg = """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0A48F5, #4DF50A);  /* blue to green */
        background-size: cover;
    }
    button {
        background: blue;
    }
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)
    st.write(f"<h1 style='color: white;'>Hi {var.name}</h1>",unsafe_allow_html=True)
    st.write(f"<h4 style='color: white;'>Congratulations! You have reached your today's target! Your target has been reset. Come back tomorrow</h4>",unsafe_allow_html=True)
    st.write(f"<h4 style='color: white;'>Till then, Bye Bye...</h4>",unsafe_allow_html=True)
    st.write("<br><br><h4 style='color: white;'>Time Record</h4>",unsafe_allow_html=True)
    for x in var.timelist[::-1]:
        st.write(f"<h5 style='color: white;'>{x}</h5>",unsafe_allow_html=True)
    for m in range(0,5):
        st.balloons()
        time.sleep(0.05)
if var.application==3:
    page_bg = """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0A48F5, #4DF50A);  /* blue to green */
        background-size: cover;
    }
    button {
        background: blue;
    }
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)


    st.markdown(f"<h1 style='color: white;'>Hi {var.name}</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: white;'>Sorry but it seems that we have ran out of time as its too late. Our day ends at 12:00 AM (Midnight)</h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: white;'>Don't Worry. Give a fresh try tomorrow</h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: white;'>Till then, GOOD NIGHT!</h4>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="display:flex; justify-content:center; align-items:center;">
            <img src='https://copilot.microsoft.com/th/id/BCO.cfa057af-5533-40e9-978a-9ac3f0950d38.png' width='250'>
        </div>
        """,
        unsafe_allow_html=True
    )