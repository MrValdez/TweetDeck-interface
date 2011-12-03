import PIL
import Image
import ImageGrab

# 1. Take a screenshot of the desktop.
# 2. If TweetDeck isn't running, run it. (possibly put this first)
# 3. Put TweetDeck in front
# 4. Take a screenshot
# 5. Find TweetDeck
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
	#		print Haystack_RawData[x], Needle_RawData[x]
			location = (y * HaystackBBox[2]) + x
			if Haystack_RawData[location] == Needle_RawData[0]:
	#		if Haystack_RawData[x][0] == Needle_RawData[0][0] and \
	#		   Haystack_RawData[x][1] == Needle_RawData[0][1] and \
	#		   Haystack_RawData[x][2] == Needle_RawData[0][2]:
				# possible first pixel found
				# create crop

				CroppedHaystack = Haystack.crop([x, NeedleBBox[2], y, NeedleBBox[3]])
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
					print bbox
					CroppedHaystack.load()
					CroppedHaystack.save("test.png")

				break

			currentIndex = currentIndex + 1

			if currentIndex > len(Haystack_RawData) - len(Needle_RawData):
				print ("Not Found")
				break

	return None

CompareImage(screenshot, TweetDeck_TextBox)
