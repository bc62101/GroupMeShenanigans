"""
    The GroupMe Vote System:
        When a user comments "/vote", intiate a vote system. "/vote option"
    will add one vote to said option.
"""

import groupy

group = groupy.Group.list().first
bot = groupy.Bot.list().first
members = groupy.Member.list()

class VoteSystem(object):
    def __init__( self, startUser, targetUser, action ):
        starter = startUser
        target = targetUser
        act = action
        voted = { 'yes': [], 'no': [] }

        poll_name = act + ": " + target + "\n"
        bot.post( starter + " has initiated poll " + poll_name + "!\n" + "Use /vote option to vote." )

    def vote( self, option, voter_id ):
        if( option in vote_options ):
            if( not(voter_id in voted) ):
                voted[option].append(voter_id)
                self.results()
            else:
                voted[option].append(vote_id)
                voted[ 'yes' if option == 'no' else 'no' ].remove(vote_id)
                self.results()

    def results( self ):
        bot_post = poll_name
        bot_post += "\n --------- \n"
        for option, value in vote_options.items():
            bot_post += option + ": " + value + "\n"
        bot.post(bot_post)
        if ( len(voted['yes'] + voted['no']) == len(members) ):
            bot.post("It's judgement time.")
            self.judgement(act)

    def judgement ( self, action ):
        if ( len(voted['yes']) > len(voted['no']) ):
            if ( action == "kick" ):
                self.__kick(target)
            elif ( action == "add" ):
                self.__add(target)
        else:
            bot.post("Alas, failure!")

    def cancel( self, user ):
        bot.post( user + " has canceled the poll!")
        self.results()

    def __kick ( self, target ):
        bot.post("Bzzt! Bye bye, " + "\@" + target )
        group.remove(target)

    def __add ( self, target ):
        bot.post("Bzzt! Welcome!")
        group.add(target)

while True:
    messages = group.messages()
    newest_message = messages.newest
    words = newest_message.text.split() #fix for people who have names with spaces in them
    if ( "/vote" == words[0] ):
        if ( len(words) < 2 or len(words) > 3 ):
            bot.post( "Usage: /vote targetUser kick/add/cancel.\n Note that only one vote can be held at a time.\n" )
            bot.post( "Once a vote is created, use /vote option to vote either yes or no. /vote results will reveal the current count. ")
            pass
        else:
            command = words[1:]
            if ( len(command) == 1 ):
                if ( command[0] == 'cancel' ):
                    try:
                        vote_sys.cancel( newest_message.user )
                    except NameError:
                        bot.post( "A votesystem does not already exist!" )
                elif ( command[0] == 'yes' or command[0] == 'no'  ): #replace try/except with method
                    try:
                        vote_sys.vote( command[0], newest_message.user_id )
                    except NameError:
                        bot.post("A votesystem does not already exist!")
                elif ( command[0] == 'results' ):
                    try:
                        vote_sys.results()
                    except NameError:
                        bot.post("A votesystem does not already exist!")
                else:
                    bot.post("That command doesn't exist!")

            elif ( len(command) == 2 ):
                bot.post("Creating vote system....")
                vote_sys = VoteSystem( newest_message.name, command[0], command[1] )
