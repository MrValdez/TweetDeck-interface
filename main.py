import PIL
import Image
import ImageGrab

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

screenshot = ImageGrab.grab()
TweetDeck_TextBox = Image.open("click_here.png")

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
			if Haystack_RawData[location] == Needle_RawData[0]:
				# possible first pixel found
				# create crop

				CroppedHaystack = Haystack.crop([x, y, NeedleBBox[2], NeedleBBox[3]])
				CroppedHaystack_RawData = CroppedHaystack.getdata()

				found = True
				i = 0
				for pixel in CroppedHaystack_RawData:
					if Needle_RawData[i] != pixel:
						found = False
						break
					i = i + 1

				if found:
					bbox = [x, y, x + NeedleBBox[2], y + NeedleBBox[3]]
					CroppedHaystack = Haystack.crop(bbox)
					CroppedHaystack.load()
					CroppedHaystack.save("debug.png")
					return [x, y]

				break

			currentIndex = currentIndex + 1

			if currentIndex > len(Haystack_RawData) - len(Needle_RawData):
				print ("Not Found")
				break

	return None

x, y = CompareImage(screenshot, TweetDeck_TextBox)

import win32api, win32con
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

offset = 50
click(x + offset, y + offset)

# http://code.activestate.com/recipes/65107/

import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")
shell.SendKeys("It works! Just a few more cleanup... https://github.com/MrValdez/TweetDeck-interface")
shell.SendKeys("~")
