"""
    The Groupme Curse Counter
    -------------------------
    Benson Chau
    Purpose: To annoy Sai Mummalaneni in a groupme chat, dx(5x + x). Other people too.
    Usage = 'python thegroupme_cursecounter.py'
    REQUISITES:
        install groupy.
"""
import groupy
import time
import matplotlib

#Generate possible terms that each user might say; Past 100 messages, because
#I can't have it lag too much. Keeps it updated too. Might increase the
#message count to match accuracy.
def generate_common_terms():
    memberbank_phrase = {}
    messages = group.messages()
    members = group.members()
    for member in members:
        member_messages = [ message.text for message in messages
                                    if message.name == str(member) ]
        memberbank_phrase[str(member)] = member_messages

    """
        For each list of sentences of a member, split the words and
    add them to another dictionary that holds a key (the word) attached
    to a value (the number of times the word has been said in every sentence given).
        Finally, fill another dictionary with a key(the member) and the word_count
    dictionary. Return the dictionary.
    """
    commonenglishwords = []
    with open("commonenglishwords.txt", "r") as f:
        for line in f:
            for word in line.split():
                commonenglishwords.append(word)

    memberbank_wordcount = { key : {} for key, value in memberbank_phrase.items() }
    for key, phrases in memberbank_phrase.items():
        wordcount = {}
        for message in phrases:
            try:
                words = message.split()
                for word in words:
                    if( not(word.lower() in commonenglishwords) ):
                        if( not(word.lower() in wordcount) ):
                            wordcount[word.lower()] = 0
                        wordcount[word.lower()] += 1
                    else:
                        pass
            except AttributeError:
                pass
        memberbank_wordcount[key] = wordcount
    return memberbank_wordcount #Where memberbank_wordcount is ultimately the key
                                #(the name of the member) and value (a dictionary with a word
                                # and the number of times it has been said).

def line_graphs():
    pass

def bar_graphs():
    pass

group = groupy.Group.list().first
bot = groupy.Bot.list().first
members = groupy.Member.list()

#sai_common_curses_bank = {'feg': 0, 'fuck': 0, 'done': 0, 'dick': 0, 'penis': 0, 'bone': 0} #The common words that Sai texts.
#sai_phrases = {}  #Hold every new message Sai puts out.

print("The Groupme Curse Counter: Powered by Groupy, a GM API Wrapper.")
print("Checking messages....")

word_bank = generate_common_terms()
while True:
    messages = group.messages()
    newest_message = messages.newest
    words = newest_message.text.split()
    if( words != None and newest_message.name in word_bank):
        bot_post = newest_message.name + "\n --------- \n"
        for word in words:
            if( word.lower() in word_bank[newest_message.name] ):
                word_bank[newest_message.name][word.lower()] += 1
            else:
                word_bank[newest_message.name][word.lower()] = 1

            bot_post += word.lower() + ": " + str(word_bank[newest_message.name][word.lower()]) + "\n"

        bot.post(bot_post)
        time.sleep(5)
