# GITAM Online ZOOM Classes Attender

<img src="screenshot.jpeg" align="right" width=300/>

### This is just for educational purpose and to understand the concepts of programming. I'm not responsible for any kind of misuse of this script.

This bot attends my university online zoom classes every day on an ubuntu server. It fetches the zoom meeting links from the University student profile website using my login credentials, arranges them in chronological order, and attends every class back-to-back, using Selenium Firefox after authenticating the zoom account.

<b>Features:</b>
1. Checks for updated classes/links in GLearn every 30 seconds.
2. Joins audio also, after joining the meeting.
3. A telegram notification is sent after attending every class.
4. If there are no classes after a specific time, the bot goes to sleep.

<b>Packages used:</b>
1. Requests
2. BeautifulSoup
3. Selenium
4. Datetime

<b>Future updates:</b>
1. Attend polls.
2. Send chat messages.
