#!/usr/bin/env python

# flashcards.py - a program that interfaces with XML flashcard data
# Copyright Catherine Moresco 2014

import xml.etree.ElementTree as ET
import os

class Card(object):
	def __init__(self, element):
		self.id=element.get("id")
		self.hide=element.get("hide")
		self.front=element.find("front").text
		self.back=element.find("back").text


def open_stack():
	print "Which stack would you like to load?"
	for stack in os.listdir('stacks'):
		print stack
	filename = raw_input('>> ')
	if os.path.isfile("stacks/"+filename) != True:
		print "I'm sorry, that stack does not exist."
		return
	return ET.parse('stacks/'+filename), filename

def make_card_dict(root):
	d = {}
	for item in root:
		item = Card(item)
		d[item.id] = item
	return d

def play(dic, filename, stackname):
	# give user a chance to restore hidden cards
	refreshall = raw_input("Would you like to restore all removed cards before you begin? (Y/N)\n>> ")
	if refreshall == "Y":
		for card in dic.values():
			card.hide = "no"
	if refreshall == "Q":
		exit(0)
	# let user choose whether to see words or definitions first
	first = raw_input("Would you like to see words first (W) or definitions first (D)?\n>> ")
	# iterate over cards
	for cardid, card in dic.iteritems():
		if first == "D":
			first, second = card.back, card.front
		else:
			first, second = card.front, card.back
		moveon = False
		# checks if card is hidden, and moves on if it is
		if card.hide == 'yes':
			moveon = True
		else:
			print "Press 'F' to flip, 'M' to move on, 'R' to remove card from stack.\n"
			print "\n\t\t\t" + first + "\n \n"
		# allow user to interact with card
		while moveon == False:
			action = raw_input('>> ')
			if action == "F":
				print  "\n\n\t\t\t" + second+ "\n \n"
			if action == "M":
				moveon = True
			if action == "R":
				card.hide = "yes"
			if action == "Q":
				exit(0)
	playagain = raw_input("Done with stack. Play again? (Y/N)\n>> ")
	if playagain == "Y":
		play(dic, filename, stackname)
	else:
		writetofile(dic, filename,stackname)
		return

def addcard(dic, root, maxid):
	newcard = ET.SubElement(root, 'card')
	newcard.set('hide', 'no')
	newcard.set('id', str(maxid + 1))
	ET.SubElement(newcard, 'front')
	ET.SubElement(newcard, 'back')
	tocard = Card(newcard)
	tocard.front = raw_input("Enter the front text:\n>> ")
	tocard.back = raw_input("Enter the back text:\n>> ")
	dic[tocard.id] = tocard

def writetofile(carddict, filename, stackname):
	root = ET.Element('stack')
	root.set('name', stackname)
	for c in carddict.values():
		newcard = ET.SubElement(root, "card")
		newcard.set('hide', c.hide)
		newcard.set('id', c.id)
		front = ET.SubElement(newcard, 'front')
		front.text = c.front
		back = ET.SubElement(newcard, 'back')
		back.text = c.back
	ET.ElementTree(root).write("stacks/" + filename)

def edit(dic, root, stackname, filename):
	while True:
		# list cards and find their max id number
		maxid = 0
		print "Here are the cards in the stack you selected:"
		for card in dic.values():
			print card.id + " " + card.front + ": " + card.back
			if int(card.id) > maxid:
				maxid = int(card.id)
		selectcard = raw_input("Select the number of the card you would like to edit, or enter 'A' to add a new card or 'D' if you're done editing.\n>> ")
		if selectcard == "D":
			writetofile(dic, stackname, filename)
			return
		if selectcard == "Q":
			exit(0)
		if selectcard == "A":
			addcard(dic, root, maxid)
		if selectcard in dic.keys():
			changecard = dic[selectcard]
			frontorback = raw_input("Would you like to change front text (F) or back text (B), or delete the card (D)?\n>> ")
			if frontorback == 'F':
				changecard.front = raw_input("Enter new front text:\n>> ")
			if frontorback == 'B':
				changecard.back = raw_input("Enter new back text:\n>> ")
			if frontorback == 'D':
				del dic[selectcard]
			if frontorback == 'Q':
				exit(0)
		else:
			print "Card does not exist. Please try another."

def newstack():
	stackname = raw_input("Enter the name of your new stack.\n>> ")
	filename = raw_input("Enter a file name.\n>> ")
	newdict = {}
	adding = "Y"
	maxid = 1
	while adding == "Y":
		print "Card " + str(maxid) + ":"
		addcard(newdict, ET.Element('stack'), maxid)
		maxid += 1
		adding = raw_input("Would you like to add another card (Y/N)?\n>> ")
	writetofile(newdict, filename, stackname)
	print "New stack saved!"


print "Welcome to FLASHCARDS!\nEnter 'Q' to quit at any time."
while True:
	action = raw_input('Would you like to load a stack (L), or create a new one? (N)\n>> ')
	if action == "L":
		stackdoc, filename = open_stack()
		stack = stackdoc.getroot()
		stackname = stack.get("name")
		carddict = make_card_dict(stack)
		print 'Stack "' + stackname + '" opened.'
		mode = raw_input('Would you like to play (P), or edit (E)?\n>> ')
		if mode == "P":
			play(carddict, filename, stackname)
		if mode == "E":
			edit(carddict, stack, stackname, filename)
		if mode == "Q":
			exit(0)
	if action == "N":
		newstack()
	if action == "Q":
		exit(0)