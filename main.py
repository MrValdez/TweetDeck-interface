import win32api, win32con
import win32com.client
import subprocess
import PIL
import Image
import ImageGrab
import os

# 1. Take a screenshot of the desktop.
# 2. If TweetDeck isn't running, run it. (possibly put this first)
# 3. Put TweetDeck in front
# 4. Take a screenshot
# 5. Find TweetDeck. Return the x, y of the textarea
# 6. Click on TweetDeck's textarea
# 7. Type a tweet
# 8. Press Enter
# 9. ???
# 10. Profit!

# helpful link:
# http://code.activestate.com/recipes/65107/

# bugs:
# * will fail if you have another program with the name TweetDeck running
#	(such as a windows explorer folder)

def CompareImage(Haystack, Needle):
	"""
		Returns the position where Needle can be found in Haystack.
		Returns None if not found.
	"""
	Needle_RawData = Needle.getdata()
	Haystack_RawData = Haystack.getdata()

	currentIndex = 0

	HaystackBBox = Haystack.getbbox()
	NeedleBBox = Needle.getbbox()
	found = False

	for y in range(HaystackBBox[3] - NeedleBBox[3]):
		for x in range(HaystackBBox[2] - NeedleBBox[2]):
			location = (y * HaystackBBox[2]) + x

			# we check against each other's RGB
			if Haystack_RawData[location][0] == Needle_RawData[0][0] and \
			   Haystack_RawData[location][1] == Needle_RawData[0][1] and \
			   Haystack_RawData[location][2] == Needle_RawData[0][2]:
				# possible first pixel found
				# create crop

				CroppedHaystack = Haystack.crop([x, y, x + NeedleBBox[2], y + NeedleBBox[3]])
				CroppedHaystack_RawData = CroppedHaystack.getdata()

				Found = True
				i = 0
				for pixel in CroppedHaystack_RawData:
					if Needle_RawData[i][0] != pixel[0] and \
					   Needle_RawData[i][1] != pixel[1] and \
					   Needle_RawData[i][2] != pixel[2]:
						Found = False
						break

					i = i + 1

				if i == 0:
					continue

				bbox = [x, y, x + NeedleBBox[2], y + NeedleBBox[3]]
				CroppedHaystack = Haystack.crop(bbox)
				CroppedHaystack.load()
				CroppedHaystack.save("debug2.png")

				if Found:
					bbox = [x, y, x + NeedleBBox[2], y + NeedleBBox[3]]
					CroppedHaystack = Haystack.crop(bbox)
					CroppedHaystack.load()
					CroppedHaystack.save("debug.png")
					return [x, y]

				continue

			currentIndex = currentIndex + 1

			if currentIndex > len(Haystack_RawData) - len(Needle_RawData):
				print ("Not Found")
				break

	return None, None

def ClickOnTweetdeck(x, y):
	offset = 10
	x = x + offset
	y = y + offset

	win32api.SetCursorPos((x,y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def SendMessage(message):
	shell.SendKeys(message)
	shell.SendKeys("~")

def RunTweetDeck():
	# check if TweetDeck is already running. If not, try to run it.
	def FindExe(ExePath):
				#http://stackoverflow.com/questions/1187264/how-to-check-if-some-process-is-running-in-task-manager-with-python
		import win32com.client
		strComputer = "."
		objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
		objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
		colItems = objSWbemServices.ExecQuery("Select * from Win32_Process")
		for objItem in colItems:
		   if objItem.ExecutablePath == ExePath:
			   return True
		return False

	#win32ui.FindWindow(None, "TweetDeck")

	# check x86 first
	environKey = "ProgramFiles(x86)"
	exe = os.environ[environKey] + r"\TweetDeck\TweetDeck.exe"

	if not os.path.isfile(exe):
		environKey = "ProgramFiles"
		exe = os.environ[environKey] + r"\TweetDeck\TweetDeck.exe"

	if not os.path.isfile(exe):
		print ("TweetDeck not found in Program Files")
		return False

	#subprocess.call([exe])
	subprocess.Popen([exe])
	return True

def Main():
	shell = win32com.client.Dispatch("WScript.Shell")

	TweetDeck_TextBox = Image.open("click_here.png")

	if not RunTweetDeck():
		print ("Tweetdeck was not found")
		return

	# keep looking for the tweetdeck's textbox until 1min has passed
	import time
	timer = time.clock()
	timeout = timer + 60.0

	while True:
		shell.AppActivate('TweetDeck')
		screenshot = ImageGrab.grab()

		x, y = CompareImage(screenshot, TweetDeck_TextBox)
		if not (x == None and y == None):
			break

		print ("Looking for Tweetdeck... (%.0f seconds left)" % (timeout - timer))

		time.sleep(1)
		timer = time.clock()
		if (timer > timeout):
			print ("Timeout: Tweetdeck was not found")
			return

	if x == None or y == None:
		print ("Tweetdeck was not found")
	else:
		ClickOnTweetdeck(x, y)
		#SendMessage("")

Main()
