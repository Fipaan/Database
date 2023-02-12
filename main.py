import sys, os



#---------------------------------------------------------- base methods <start>

def append(path, value):
	f = open(path, "a")
	f.write(value)
	f.close()
	return

def get(path):
	f = open(path, "r")
	output = f.read()
	f.close()
	return output

def getlines(path):
	f = open(path, "r")
	output = f.readlines()
	f.close()
	return output

def rewrite(path, value):
	f = open(path, "w")
	f.write(value)
	f.close()
	return

def clearLine(path, substringInStart):
	if get(path).find(substringInStart) == -1:
		return
	lines = getlines(path)
	rewrite(path, "")
	for line in lines:
		if line.find(substringInStart) != 0:
			append(path, line)
	return

#Removes all spaces at the beginning and end of a string
def DZSE(inputValue):
    lenInput = len(inputValue)
    startIndex = 0
    endIndex = lenInput
    findStart = findEnd = False
    while startIndex < lenInput and not findStart:
        if inputValue[startIndex] != " ":
            findStart = True
            continue
        startIndex += 1
    if not findStart:
        return ""
    while endIndex > 0 and not findEnd:
        endIndex -= 1
        if inputValue[endIndex] != " ":
            findEnd = True
    return inputValue[startIndex:endIndex+1]

#---------------------------------------------------------- base methods <end>



#---------------------------------------------------------- Manipulating with keys <start>

def detectKey(path, key):
	if get(path).find(key) == -1:
		return False
	for line in getlines(path):
		if getKeys(line).find(key) != -1:
			return True
	return False

def clearKey(path, key):
	if get(path).find(key) == -1:
		return
	lines = getlines(path)
	rewrite(path, "")
	isClear = False
	for line in lines:
		indexKey = line.find(key)
		if (indexKey == -1) or isClear:
			append(path, line)
			continue
		isClear = True
		firstTab = line.find("-")
		if firstTab == -1:
			continue
		linewithout = getLineWithoutKey(line, key, firstTab)
		append(path, linewithout)
	return

def getExclude(keys, key):
    countKeys = len(keys)
    if countKeys == 2:
        if keys[0] == key:
            return keys[1]
        else:
            return keys[0]
    if countKeys == 3:
        if keys[0] == key:
            return keys[1] + "-" + keys[2]
        elif keys[1] == key:
            return keys[0] + "-" + keys[2]
        else:
            return keys[0] + "-" + keys[1]
    output = ""
    if keys[0] == key:
        output = keys[1]
    elif keys[1] == key:
        output = keys[0]
    else:
        output = keys[0] + "-" + keys[1]
    for i in range(2, countKeys):
        ikey = keys[i]
        if ikey == key:
            continue
        output += "-" + ikey
    return output

def getLineWithoutKey(line, key, firstTab):
	keys = line.split("-")
	keys[0] = keys[0].split(" ")[-1]
	keys[-1] = keys[-1].split(" ")[0]
	keysWithoutKey = getExclude(keys, key)
	lenFirstKey = lenLastKey = -1
	if keys[0] == key:
		lenFirstKey = len(keys[1])
	else:
		lenFirstKey = len(keys[0])
	if keys[-1] == key:
		lenLastKey = keys[-2]
	else:
		lenLastKey = keys[-1]
	startindex = firstTab - lenFirstKey
	endindex = startindex + len(keysWithoutKey) + len(key) + 1
	output = line[:startindex] + keysWithoutKey + line[endindex:]
	return output

def getNumberLineWithKey(path, key, lines = -1):
	if lines == -1:
		lines = getlines(path)
	for i in range(len(lines)):
		line = lines[i]
		keys = getKeys(line)
		if key in keys:
			return i
	return -1

def setValueByKey(path, key, value):
	lines = getlines(path)
	rewrite(path, "")
	index = getNumberLineWithKey(path, key, lines)
	for i in range(len(lines)):
		line = lines[i]
		if i != index:
			append(path, line)
		else:
			listItems = line.split("|")
			changedline = listItems[0] + "|" + listItems[1] + "| " + value
			append(path, changedline + "\n")

#---------------------------------------------------------- Manipulating with keys <end>



#---------------------------------------------------------- Manipulating with tags <start>

def detectTag(path, tag):
	for line in getlines(path):
		if getTag(line) == tag:
			return True
	return False

def clearTag(path, tag):
	if get(path).find(tag) == -1:
		return
	lines = getlines(path)
	rewrite(path, "")
	for line in lines:
		if line.find(tag) == 0:
			continue
		append(path, line)

def findLineByTag(path, tag):
	if get(path).find(tag) == -1:
		return -1
	lines = getlines(path)
	for i in range(len(lines)):
		if getTag(lines[i]) == tag:
			return i

def newKeyByTag(path, tag, key):
	index = findLineByTag(path, tag)
	lines = getlines(path)
	rewrite(path, "")
	for i in range(len(lines)):
		line = lines[i]
		if i != index:
			append(path, line)
		else:
			carved = getTag(line) + " | " + getKeys(line) + "-" + key + " | " + getValueInLine(line)
			append(path, carved)

#---------------------------------------------------------- Manipulating with tags <end>

def getValueBySplit(line, index, substring = "|"):
	return DZSE(line.split(substring)[index])

def getTag(line):
	return getValueBySplit(line, 0)
def getKeys(line):
	return getValueBySplit(line, 1)
def getValueInLine(line):
	return getValueBySplit(line, 2)

def keyEqualsTag(tag, dependence):
	if dependence:
		return tag
	return ""
	


def update(path, isUpdate, MIN_COUNT_LINES = 2):
	if not isUpdate:
		return
	lines = getlines(path)
	rewrite(path, "")
	for line in lines:
		if line.count("|") < MIN_COUNT_LINES:
			continue
		append(path, line)

def showFile(PATH):
	print("--------------------------- Start file \n")
	print(get(PATH))
	print("--------------------------- End file")

def help_list(commands):
	for comm in commands:
		if comm == "help":
			print("help - show this list")
		elif comm == "exit":
			print("exit - exit the program")
		elif comm == "getfile":
			print("getfile - get file with database")
		elif comm == "save":
			print("save - save file in buffer")
		elif comm == "load":
			print("load - load from buffer in file")
		elif comm == "clear":
			print("clear - clear current database")
		elif comm == "'clear typeObject nameObject'":
			print("clear | 'type' | 'name' - delete line by value with type 'type' with name 'name'")
		elif comm == "'new typeObject nameObject'":
			print("new | 'type' | 'name' - create line with value type 'type' and name 'name'")
		elif comm == "'new typeObject nameObject1 nameObject2'":
			print("new | 'type' | 'name1' | 'name2' - create object with 'name2' and type 'type' by search 'name1' in database")

def main(folder, namefile, namelogs, isUpdate, COMMANDS, MIN_COUNT_LINES = 2, showLoadedFile = True, comListInError = True, alwaysShowFile = False, inGetClearConsole = False, byDefaultTagAssignedWithKey = True):
	PATH = folder + namefile
	session_logs = folder + namelogs
	saved = get(PATH)
	rewrite(session_logs, "")
	ASF_clear_commands = ["save", "load", "clear"]
	ASF_show_commands = ["save", "load","clear"]
	while True:
		update(PATH, isUpdate, MIN_COUNT_LINES)
		inp = input()
		append(session_logs, inp + "\n")
		words = inp.split("|")
		if inp == "exit":
			sys.exit()
		elif inp == "save":
			saved = get(PATH)
		elif inp == "load":
			rewrite(PATH, saved)
			if showLoadedFile and not alwaysShowFile:
				print(get(PATH))
		elif inp == "getfile":
			if inGetClearConsole:
				os.system("cls")
			showFile(PATH)
		elif inp == "clear":
			rewrite(PATH, "")
		elif inp == "help":
			help_list(COMMANDS)
		elif len(words) > 2:
			keywordAction = DZSE(words[0])
			keywordObject = DZSE(words[1])
			object1 = DZSE(words[2])
			object2 = "_unknownValue"
			if keywordAction == "clear":
				if keywordS == "key":
					clearKey(PATH, object1) #object1 - key
				elif keywordS == "tag":
					clearTag(PATH, object1) #object1 - tag
			elif keywordAction == "new":
				checkKeys = detectKey(PATH, object1)
				checkTags = detectTag(PATH, object1)
				if len(words) == 4:
					object2 = DZSE(words[3])
				if keywordObject == "key":
					if detectKey(PATH, object2): #object2 - key
						print("Already exists")
					else:
						newKeyByTag(PATH, object1, object2) #object1 - tag; object2 - key
				elif keywordObject == "tag":
					if detectTag(PATH, object1): #object1 - tag
						print("Already exists")
					else:
						append(PATH, "\n" + object1 + " | " + keyEqualsTag(object1, byDefaultTagAssignedWithKey) + " | ") #object1 - tag
				elif keywordObject == "value":
					if not detectKey(PATH, object1) and not detectTag(PATH, object1):
						print("Key/Tag isn't exists")
					else:
						if checkKeys:
							setValueByKey(PATH, object1, object2) #object1 - key; object2 - value
						else:
							pass #setValueByTag(PATH, object1, object2) #object1 - tag; object2 - value
				else:
					print("Invalid command")
					if comListInError:
						help_list(COMMANDS)
			else:
				print("Invalid command")
				if comListInError:
					help_list(COMMANDS)
		else:
			print("Invalid command")
			if comListInError:
				help_list(COMMANDS)
		if inp in ASF_clear_commands and alwaysShowFile:
			os.system('cls')
		if inp in ASF_show_commands and alwaysShowFile:
			showFile(PATH)
		

if __name__ == "__main__":
	PATH = os.path.abspath(os.path.dirname(sys.argv[0])) + "\\" #path folder of this file
	namefile = "database.txt"
	namelogs = "templogs.txt" 
	COMMANDS = ["exit", "getfile", "save", "load", "clear", "br", "help", "'clear typeObject nameObject'", "'new typeObject nameObject'", "'new typeObject nameObject1 nameObject2'"]
	main(PATH, namefile, namelogs, isUpdate, COMMANDS)