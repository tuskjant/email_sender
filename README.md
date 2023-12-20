## Email schedule manager

### About
The Email Schedule Manager is a tool designed to assist with planning and 
automating the sending of emails based on message templates. 
The object of this app is to practice python programming.

**Features:**
+ You can enter a single recipient or select a list of recipients from a
CSV file.
+ You can either write an email message or choose one or several pre-existing
 messages from a TXT file.
+ It provides programming options for scheduling the emails including single 
delivery, daily, weekly, monthly and yearly.
+ Email and message options selection: send to all recipients/all messages 
every time or once at a time.
+ You can choose whether to send the email to all recipients or to one  
recipient at a time. And choose to send all messages at once or one at a time.
+ The tool allows you to create new task that will be automatically managed.
+ You can review the email delivery tasks, including listing tasks, 
adding new ones, and deleting existing tasks.
### Demo



(https://github.com/tuskjant/email_sender/assets/151870795/81c34275-e019-4c31-8083-bd2d86bd8cf8).playbackRate = 1.5




### Usage
**Configuration:**
To use the Email Schedule Manager, you need to enter the necessary details 
for sending emails. This information, including the password, will be stored 
in a JSON file in the data folder. Click the config icon 
<img src="images/configuraciones.png" alt="configuration" width="24" height="24"> to provide this data.

**How to use:**
+ **Recipients:** You can manually enter recipient data for up to one recipient. Alternatively, you can use a CSV file
where each row represents a recipient, with the format: "name, name@email.com". Choose the email basis: sending
to all recipients every time or one recipient at a time. Messages will be sent to recipients by order in one-at-a-time mode. 
+ **Messages:** You can either write up to one message directly or select one or more TXT files to be used as
messages. In a TXT file, the first line will be considered the subject of the email. Whenever the characters
*[NAME]* are found in the text, they will be replaced with the recipient's name. Select the messages' basis:
sending all messages every time or one message at a time. In one-at-a-time mode, messages will be sent by order.
+ **Schedule:** Sending dates will be obtained from start to end sending dates using the selected frequency
(once, daily, weekly, monthly or yearly) All emails will be sent within 30 minutes around selected time.
+ **Task** will be shown for revision. To program the task click on  <img src="images/correo-electronico_prog.png" alt="program task" width="24" height="24"> sending icon. Program will run on silent mode and emails will be sent on 
selected dates. 
Click on <img src="images/correo-electronico_lista.png" alt="tasks list icon" width="24" height="24"> to consult
and review pending tasks. Select one task and click on the <img src="images/error.png" alt="delete icon" width="24" height="24"> to cancel and delete an email delivery task.

### Credits
This python code is made by Gemma Riu, inspired by an exercise from '100 Days of Code' by Angela Yu.

Icons from https://www.flaticon.es :
+ Correo electrónico iconos creados por Uniconlabs
+ Ajustes iconos creados por srip
+ Signo de interrogación iconos creados por sonnycandra 
+ Calendario iconos creados por Md Tanvirul Haque 
+ Bloquear iconos creados por Flowicon 
+ Correo electrónico iconos creados por Freepik 
The code uses tkinter, Pillow and Babel libraries.
