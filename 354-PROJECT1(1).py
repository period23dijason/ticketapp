
# coding: utf-8

# In[130]:


import pymssql
from datetime import datetime
## INSTALLATION INSTRUCTION ON LINUX:
## export PYMSSQL_BUILD_WITH_BUNDLED_FREETDS=1
## pip --user install pymssql


# TEST FUNCTION
def printRows(rows):
    for row in rows:
        print(row)

        
global conn
conn = pymssql.connect(host='cypress.csil.sfu.ca', user='c354g19', password='4YgYgJtFJnyNgGq6', database='c354g19A')
global cur
cur = conn.cursor()


class User:
    def __init__(self, UserID, firstName, lastName, PhoneNum, Email):
        self.UserID = UserID
        self.firstName = firstName
        self.lastName = lastName     
        self.PhoneNum = PhoneNum     
        self.Email = Email

    def orderTicket(self, EventID, Order):
        conn = pyodbc.connect('driver={SQL Server};Server=cypress.csil.sfu.ca;Trusted_Connection=yes;')
        cur = conn.cursor()
        i = 0
        while(i < Order):
            cur.execute("INSERT INTO Ticket_Info VALUES(?, ?);", (self.UserID, EventID))
            i = i + 1
        cur.execute("UPDATE Event_Info SET AvailSeatNum = AvailSeatNum - ? WHERE EventID = ?;", (Order, EventID))
        conn.commit()

    def cancelTicket(self, EventID):
        conn = pyodbc.connect('driver={SQL Server};Server=cypress.csil.sfu.ca;Trusted_Connection=yes;')
        cur = conn.cursor()       
        cur.execute("DELETE FROM Ticket_Info WHERE UserID = ? AND EventID = ?;", (self.UserID, EventID))
        cur.execute("UPDATE Event_Info SET AvailSeatNum = AvailSeatNum + 1 WHERE EventID = ?;", (EventID))
        conn.commit()


        

def searchStadium(stadium):
    cur.execute("SELECT E.EventID, EventName, EventDate, S.Sname FROM Stadiums S, Event_Info E, Locale_Events L WHERE Sname LIKE '%" + stadium + "%' AND E.EventID = L.EventID AND L.StadiumID = S.StadiumID AND E.AvailSeatNum > 0;")
    rows = cur.fetchall()
    return rows

def findStadium(stadium):
    cur.execute("SELECT S.StadiumID, S.Sname FROM Stadiums S, Event_Info E, Locale_Events L WHERE Sname LIKE '%" + stadium + "%' AND E.EventID = L.EventID AND L.StadiumID = S.StadiumID AND E.AvailSeatNum > 0;")
    rows = cur.fetchall()
    return rows

def countStadium(stadium):
    cur.execute("SELECT COUNT(*)  FROM Stadiums S, Event_Info E, Locale_Events L WHERE Sname LIKE '%" + stadium + "%' AND E.EventID = L.EventID AND L.StadiumID = S.StadiumID AND E.AvailSeatNum > 0;")
    rows = cur.fetchall()
    return rows

def searchPerformer(performerName ):
    cur.execute("SELECT E.EventID, EventName, EventDate FROM Performers Per, Participate Par, Event_Info E, Locale_Events L WHERE Per.Pname LIKE '%" + performerName + "%' AND Per.PerformerID = Par.PerformerID AND Par.EventID = L.EventID AND E.EventID = L.EventID AND E.AvailSeatNum > 0;")
    rows = cur.fetchall()
    return rows

def countPerformer(performerName ):
    cur.execute("SELECT COUNT(*) FROM Performers Per, Participate Par, Event_Info E, Locale_Events L WHERE Per.Pname LIKE '%" + performerName + "%' AND Per.PerformerID = Par.PerformerID AND Par.EventID = L.EventID AND E.EventID = L.EventID AND E.AvailSeatNum > 0;")
    rows = cur.fetchall()
    return rows

def searchEventName(eventName):
    cur.execute("SELECT E.EventID, EventName, EventDate FROM Event_Info E, Locale_Events L WHERE EventName LIKE '%" + eventName + "%' AND E.EventID = L.EventID AND E.AvailSeatNum > 0;")
    rows = cur.fetchall()
    return rows

def countEventName(eventName):
    cur.execute("SELECT COUNT(*) FROM Event_Info E, Locale_Events L WHERE EventName LIKE '%" + eventName + "%' AND E.EventID = L.EventID AND E.AvailSeatNum > 0;")
    rows = cur.fetchall()
    return rows

def searchEventDate(eventDate ):
    cur.execute("SELECT EventName, EventDate FROM Event_Info E, Locale_Events L WHERE E.EventID = L.EventID AND E.AvailSeatNum > 0 AND EventDate = %s;", (eventDate))
    rows = cur.fetchall()
    return rows

def searchLocation(Addr ):
    cur.execute("SELECT E.EventName, L.EventDate FROM Event_Info E, Locale_Events L, Stadiums S WHERE E.EventID = L.EventID AND E.AvailSeatNum > 0 AND S.Addr LIKE '%%s%' AND S.StadiumID = L.StadiumID;", (Addr))
    rows = cur.fetchall()
    return rows

def searchPrice(Price):
    cur.execute("SELECT E.EventName, L.EventDate FROM Event_Info E, Locale_Events L WHERE E.EventID = L.EventID AND E.AvailSeatNum > 0 AND E.Price < %s;", (Price))
    rows = cur.fetchall()
    return rows

def searchNumAvailSeat(NumAvailSeat):
    cur.execute("SELECT E.EventName, L.EventDate FROM Event_Info E, Locale_Events L WHERE E.EventID = L.EventID AND E.AvailSeatNum > %s;", (NumAvailSeat))
    rows = cur.fetchall()
    return rows

def searchGenre(Genre ):
    cur.execute("SELECT E.EventName, L.EventDate FROM Event_Info E, Locale_Events L, Artists A, Participate P WHERE E.EventID = L.EventID AND E.AvailSeatNum > 0 AND E.EventID = P.EventID AND P.PerformerID = A.PerformerID AND A.Genre = %s;", (Genre))
    rows = cur.fetchall()
    return rows

def searchSport(Sport ):
    cur.execute("SELECT E.EventName, L.EventDate FROM Event_Info E, Locale_Events L, Sports_Player S, Participate P WHERE E.EventID = L.EventID AND E.AvailSeatNum > 0 AND E.EventID = P.EventID AND P.PerformerID = S.PerformerID AND S.Sport = %s;", (Sport))
    rows = cur.fetchall()
    return rows

def searchMatchUp(PlayerName1 , PlayerName2 ):
    cur.execute("SELECT E.EventName, L.EventDate FROM Event_Info E, Locale_Events L, Performers P1, Performers P2, Sports_Player SP, Participate Par1, Participate Par2 WHERE P1.Pname = %s AND P2.Pname = %s AND P1.PerformerID = SP.PerformerID AND P2.PerformerID = SP.OpponentID AND P1.PerformerID = Par1.PerformerID AND P2.PerformerID = Par2.PerformerID AND Par1.EventID = E.EventID AND Par2.EventID = E.EventID AND E.EventID = L.EventID AND E.AvailSeatNum > 0;", (PlayerName1, PlayerName2))
    rows = cur.fetchall()
    return rows

def searchDurationMoreThanEqualTo(Duration):
    cur.execute("SELECT E.EventName, L.EventDate FROM Event_Info E, Locale_Events L WHERE E.Duration >= %s AND L.EventID = E.EventID;", (Duration))
    rows = cur.fetchall()
    return rows

def searchDurationLessThanEqualTo(Duration):
    cur.execute("SELECT E.EventNam, L.EventDate FROM Event_Info E, Locale_Events L WHERE E.Duration <= %s AND L.EventID = E.EventID;", (Duration))
    rows = cur.fetchall()
    return rows

def searchDurationInBetween(Duration1, Duration2):
    cur.execute("SELECT E.EventName, L.EventDate FROM Event_Info E, Locale_Events L WHERE E.Duration >= %s AND  E.Duration <= %s AND L.EventID = E.EventID;", (Duration1, Duration2))
    rows = cur.fetchall()
    return rows

def showEventInfo(EventID):
    if(len(EventID) > 0):
        cur.execute("""
        SELECT E.EventName, E.Duration, L.EventDate, S.Sname, S.Addr, E.AvailSeatNum 
        FROM Event_Info E, Locale_Events L, Stadiums S 
        WHERE E.EventID = %s AND E.EventID = L.EventID AND L.StadiumID = S.StadiumID AND E.AvailSeatNum > 0;""", (EventID))
        rows = cur.fetchall()
        return rows
    else:
        return showEveryAvailEventInfo()

def showEveryAvailEventInfo():
    cur.execute("""SELECT E.EventName, E.Duration, L.EventDate, S.Sname, S.Addr, E.AvailSeatNum 
    FROM Event_Info E, Locale_Events L, Stadiums S 
    WHERE E.EventID = L.EventID AND L.StadiumID = S.StadiumID AND E.AvailSeatNum > 0;""")
    rows = cur.fetchall()
    return rows

def showEveryEventInfo():
    cur.execute("""SELECT E.EventName, E.Duration, L.EventDate, S.Sname, S.Addr, E.AvailSeatNum 
    FROM Event_Info E, Locale_Events L, Stadiums S 
    WHERE E.EventID = L.EventID AND L.StadiumID = S.StadiumID;""")
    rows = cur.fetchall()
    return rows

def showEventPerformers(EventName):
    cur.execute("SELECT Per.Pname FROM Participate Par, Performers Per, Event_Info E WHERE E.EventName = %s AND E.EventID = Par.EventID AND Par.PerformerID = Per.PerformerID;", (EventName))
    rows = cur.fetchall()
    return rows

def updateEventName(EventID, EventName):
    cur.execute("Update Event_Info SET EventName ='" + str(EventName) + "' WHERE EventID ='" + EventID + "'")
    conn.commit()

def updateEventDuration(EventID, Duration):
    cur.execute("Update Event_Info SET Duration ='" + str(Duration) + "' WHERE EventID ='" + EventID + "'")
    conn.commit()
    
#####################################################################################################################
def updateEventDate(EventID, EventDate):
    datetime_object = datetime.strptime(EventDate, "%Y-%m-%d")
    cur.execute("Update Event_Info SET EventDate ='Date(" + EventDate + ")' WHERE EventID ='" + EventID + "'")
    conn.commit()
    """"""


def updateAvailSeatNum(EventID="",AvailSeatNum=""):
    cur.execute("Update Event_Info SET AvailSeatNum ='" + str(AvailSeatNum) + "' WHERE EventID ='" + EventID + "'")
    conn.commit()
    
    
def updateAddress(StadiumID="",Addr=""):
    print
    cur.execute("Update Stadiums SET Addr ='" + str(Addr) + "' WHERE StadiumID ='" + StadiumID + "'")
    conn.commit()
    
    
def updateStadiumName(StadiumID, name):
    cur.execute("Update Stadiums SET Sname ='" + str(name) + "' WHERE StadiumID ='" + StadiumID + "'")
    conn.commit()
    
    
def deleteEventInfoTuple(EventID=""):
    cur.execute("DELETE FROM Event_Info WHERE EventID = '" + EventID + "'")
    conn.commit()
    
    
def deleteLocaleEventTuple(EventID=""):
    cur.execute("DELETE FROM Locale_Events WHERE EventID = '" + EventID + "'")
    conn.commit()
    
def countOfPerformer(id):
    cur.execute("""
    SELECT COUNT(*)
    FROM Participate
    GROUP BY EventID
    """)
    rows = cur.fetchall()
    return rows[0][0]


# In[131]:


from tkinter import *
from tkinter import messagebox


global user



###########################################################################
def newEvent():
    window = Tk()
    window.title('New Event')
    window.geometry("500x500")
    frame0 = Frame(window)
    frame1 = Frame(window)
    frame2 = Frame(window)
    label0 = Label(frame0, text = 'Event ID')
    label1 = Label(frame1, text = 'Event Date')
    label2 = Label(frame2, text = 'Stadium Name')
    label0.pack(side=LEFT)
    label1.pack(side=LEFT)
    label2.pack(side=LEFT)
    frame0.pack()
    frame1.pack()
    frame2.pack()
    
    eventidEntry = Entry(frame0, width=30)
    eventDateEntry = Entry(frame1, width=30)
    variable = StringVar(frame2)
    variable.set('')
    lst = findStadium('')
    stadiumOptionMenu = OptionMenu(frame2, variable, *lst)
    stadiumOptionMenu.pack(side=RIGHT)
    
    eventidEntry.pack(side=RIGHT)
    eventDateEntry.pack(side=RIGHT)
    
    
    window.mainloop()
    
    
    
    
def showAllUserOrderedEveryEvent():
    window = Tk()
    window.title("Users Ordered Every Event")
    
    cur.execute("SELECT U.Firstname, U.Lastname FROM User_Info U WHERE NOT EXISTS (SELECT * FROM Event_Info E WHERE NOT EXISTS (SELECT T.UserID FROM Ticket_Info T WHERE U.UserID = T.UserID AND E.EventID = T.EventID))")
    rows = cur.fetchall()
    
    
    for i in rows:
        s = "{0:<10}{1:<10}".format(i[0], i[1])
        label = Label(window, text=s)
        label.pack()
        
        
    

###########################################################################    

def logout():
    search.destroy()
    main()
    
def initSearchWindow(search):
    search.title("Search")
    search.geometry("500x500")
    if admin:
        name = 'Admin'
    else:
        name = 'Guest'
    label0 = Label(search, text = 'Welcome! '+ name)
    label0.config(justify = CENTER)
    label0.pack()
    
    entry0 = Entry(search, width=30)
    entry0.pack()
    
    variable = StringVar(search)
    variable.set('Event')
    option = OptionMenu(search, variable, 'Event', 'Stadium', 'Performer')
    option.pack()
    
    button0 = Button(search, text = 'Search')
    button0.config(command = lambda: displayEvents(entry0.get(), variable.get()))
    button0.pack()
    
    if admin:
        button1 = Button(search, text = "New Event", command = newEvent)
        button1.pack()
        usersOrderedAllEventButton = Button(search, text = "Show Users Ordered All Events", command = showAllUserOrderedEveryEvent)
        usersOrderedAllEventButton.pack()
    logoutButton = Button(search, text = "Logout", command = logout)
    logoutButton.pack()
    
    
def closeWindow(window):
    window.destroy()
    
#############################################################################################



def editEvent(id, row):
    window = Tk()
    window.title('Edit Event')
    window.geometry("500x500")
    frame0 = Frame(window)
    frame1 = Frame(window)
    frame2 = Frame(window)
    frame3 = Frame(window)
    label0 = Label(frame0, text = 'Event Name')
    label1 = Label(frame1, text = 'Duration')
    label2 = Label(frame2, text = 'Date')
    label3 = Label(frame3, text = 'Available Seat')
    label0.pack(side=LEFT)
    label1.pack(side=LEFT)
    label2.pack(side=LEFT)
    label3.pack(side=LEFT)
    frame0.pack()
    frame1.pack()
    frame2.pack()
    frame3.pack()
    eventNameEntry = Entry(frame0, width=30)
    eventDurationEntry = Entry(frame1, width=30)
    eventDateEntry = Entry(frame2, width=30)
    availableSeatEntry = Entry(frame3, width=30)
    eventNameEntry.insert(0, row[0])
    eventDurationEntry.insert(0, row[1])
    eventDateEntry.insert(0, row[2])
    availableSeatEntry.insert(0, row[5])
    
    eventNameButton = Button(frame0, text = "Submit", command=lambda: updateEventName(id, eventNameEntry.get()))
    eventDurationButton = Button(frame1, text = "Submit", command=lambda: updateEventDuration(id, eventDurationEntry.get()))
    eventDateButton = Button(frame2, text = "Submit", command=lambda: updateEventDate(id, eventDateEntry.get()))
    availableSeatButton = Button(frame3, text = "Submit", command=lambda: updateAvailSeatNum(id, availableSeatEntry.get()))
    
    eventNameEntry.pack(side=LEFT)
    eventDurationEntry.pack(side=LEFT)
    eventDateEntry.pack(side=LEFT)
    availableSeatEntry.pack(side=LEFT)
    eventNameButton.pack(side=RIGHT)
    eventDurationButton.pack(side=RIGHT)
    eventDateButton.pack(side=RIGHT)
    availableSeatButton.pack(side=RIGHT)
    
    window.mainloop()
##############################################################################################



def editStadium(id, row):
    window = Tk()
    window.title('Edit Stadium')
    window.geometry("500x500")
    frame0 = Frame(window)
    frame1 = Frame(window)
    label0 = Label(frame0, text = 'Name')
    label1 = Label(frame1, text = 'Address')
    label0.pack(side=LEFT)
    label1.pack(side=LEFT)
    frame0.pack()
    frame1.pack()
    stadiumNameEntry = Entry(frame0, width=30)
    stadiumAddrEntry = Entry(frame1, width=30)
    stadiumNameEntry.insert(0, row[3])
    stadiumAddrEntry.insert(0, row[4])
    
    stadiumNameButton = Button(frame0, text = "Submit", command=lambda: updateStadiumName(id, stadiumNameEntry.get()))
    stadiumAddrButton = Button(frame1, text = "Submit", command=lambda: updateAddress(id, stadiumAddrEntry.get()))
    
    stadiumNameEntry.pack(side=LEFT)
    stadiumAddrEntry.pack(side=LEFT)
    stadiumNameButton.pack(side=RIGHT)
    stadiumAddrButton.pack(side=RIGHT)
    
    
def deleteEvent(id, window):
    result = messagebox.askquestion("Order", "Are You Sure?")
    if result == 'yes':
        deleteEventInfoTuple(id)
        deleteLocaleEventTuple(id)
        window.destroy()

    
def info(id):
    global eventInfo
    eventInfo = Tk()
    eventInfo.title("Event Info")
    s = showEventInfo(id)
    
    
    #key = ['Event Name', 'Duration', 'Date', 'Stadium', 'Address', 'Seat Availability']
    key = [' Event', 'Duration', ' Date', ' Stadium', '     Address', 'Seat']
    
    for i in range(len(s[0])):
        frame = Frame(eventInfo)
        title = Label(frame, text = "{0:<50}{1:<50}".format(key[i], str(s[0][i])))
        title.pack(side=LEFT)
        if admin:
            if i == 0 or i == 5:
                editButton = Button(frame, text="Edit Event", command = lambda: editEvent(id, s[0]))
                editButton.pack(side=RIGHT)
            if i == 3:
                editButton = Button(frame, text="Edit Stadium", command = lambda: editStadium(id, s[0]))
                editButton.pack(side=RIGHT)
        frame.pack()
    
    buttons = Frame(eventInfo)
#     if admin:
#         editButton = Button(buttons, text="Edit", command = lambda: editEvent(id))
#         editButton.pack(side=LEFT)
    quantityLabel = Label(buttons, text = "Quantity")
    quantityLabel.pack(side=LEFT)
    spinbox = Spinbox(buttons, from_ = 0, to = 10)
    spinbox.pack(side=LEFT)
    orderButton = Button(buttons, text="Order", command = lambda: orderTicket(id, s[0][5], spinbox.get()))
    orderButton.pack(side=LEFT)
    deleteButton = Button(buttons, text="Delete Event", command = lambda: deleteEvent(id, eventInfo))
    deleteButton.pack(side=LEFT)
    button = Button(buttons, text="Close", command = lambda: closeWindow(eventInfo))
    button.pack(side=RIGHT)
    buttons.pack()
    eventInfo.mainloop()
    

def orderTicket(id, current, n):
    result = messagebox.askquestion("Order", "Are You Sure?")
    if result == 'yes':
        if int(n) > int(current):
            messagebox.showinfo("Error", "Not Enough Available Tickets")
        else:
            updateAvailSeatNum(id, (int(current) - int(n)))
        
    eventInfo.destroy()
    info(id)
        
    
def openSearchWindow(current):
    current.destroy()
    global search
    search = Tk()
    initSearchWindow(search)
    search.mainloop()

    
def displayEvents(eventName, searchType):
    search.destroy()
    results = Tk()
    results.title("Search Results")
    
    if searchType == 'Event':
        rows = searchEventName(eventName)
        count = countEventName(eventName)
    elif searchType == 'Stadium':
        rows = searchStadium(eventName)
        count = countStadium(eventName)
    elif searchType == 'Performer':
        rows = searchPerformer(eventName)
        count = countPerformer(eventName)
        
    resultForLabel = Label(results, text="Search \"" + eventName + "\" in " + searchType)
    resultForLabel.pack()
    resultFound = Label(results, text="Found " + str(count[0][0]) + " results.")
    resultFound.pack()
    
    title = Label(results, text = "{0:<20}{1:<20}{2:<20}{3:<15}".format("Event Name", "Date","# of Performers", ""))
    title.pack()
    for i in rows:
        frame = Frame(results)
#         i = i[:-1]
        strip_list = [str(x).strip() for x in i]
        s = "{0:<20}{1:<20}{2:<20}".format(i[1], i[2], countOfPerformer(i[0]))
        label = Label(frame, text=s)
        label.pack(side=LEFT)
        infoButton = Button(frame, text="info", command =lambda i = i : info(i[0]))
        infoButton.pack(side=RIGHT)
        frame.pack()
    backButton = Button(results, text = "back", command =lambda: openSearchWindow(results))
    backButton.pack()
    results.mainloop()
    
    
    
def guest():
    entry1.insert(0, 'guest');
    entry2.insert(0, 'guest');
    
def login():
    global admin
    admin = False
    username = entry1.get()
    password = entry2.get()
    # LOGIN CREDENTIAL CHECK
    if username == 'guest' and password == 'guest':
        # LOGIN SUCCESS
        root.destroy()
        global search
        search = Tk()
        initSearchWindow(search)
        search.mainloop()
    elif username == 'admin' and password == 'admin':
        root.destroy()
        admin = True
        search = Tk()
        initSearchWindow(search)
        search.mainloop()
        
    else:
        messagebox.showinfo('Error', 'Login Failed')
        
def quit():
    root.destroy()

def main():
    global root
    root = Tk()
    root.title("Ticket Ordering App")
    root.geometry("500x500")
    #Label 1
    label0 = Label(root,text = 'Ticket Ordering App')
    label0.pack()
    label0.config(justify = CENTER)
    label1 = Label(root,text = 'User Name')
    label1.pack()
    label1.config(justify = CENTER)

    global entry1
    entry1 = Entry(root, width = 30)
    entry1.pack()

    label3 = Label(root, text="Password")
    label3.pack()
    label1.config(justify = CENTER)

    global entry2
    entry2 = Entry(root, show="*", width = 30)
    entry2.pack()

    button = Button(root, text = 'Use Guest Credentials')
    button.pack() 
    button.config(command = guest)
    button1 = Button(root, text = 'Submit')
    button1.pack() 
    button1.config(command = login)
    button2 = Button(root, text = 'Quit')
    button2.pack() 
    button2.config(command = quit)

    root.mainloop()
    
if __name__ == '__main__':
    main()

