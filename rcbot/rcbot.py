
import re
__version__ = "$Id$"
__versiondict__ = re.match("\$Id: (?P<file>.*?) (?P<revision>[0-9]*) (?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2}) (?P<time>[0-9]{2}:[0-9]{2}:[0-9]{2})(?P<timezone>.*?) (?P<user>.*) \$", __version__).groupdict()

class tcp:
    class protocols:
        from twisted.words.protocols import irc
        from twisted.protocols import basic
    from twisted.internet import reactor, protocol
import sys
regexps = [
    re.compile(r'\x0314\[\[\x0307(?P<title>.*?)\x0314\]\]\x034 (?P<flags>.*?)\x0310 \x0302http:\/\/.*?\/w\/index\.php\?title=.*?&diff=(?P<diff>[0-9]*)&oldid=(?P<oldid>[0-9]*)(&rcid=(?P<rcid>[0-9]*))?\x03 \x035\*\x03 \x0303(?P<user>.*?)\x03 \x035\*\x03 \(\x02?(?P<diffsize>[+-][0-9]*)\x02?\) \x0310(?P<comment>.*)\x03'),  # changed page, with or without rcid, with or without comment
    re.compile(r'\x0314\[\[\x0307(?P<title>.*?)\x0314\]\]\x034 (?P<flags>.*?N)\x0310 \x0302http:\/\/.*?\/w\/index\.php\?title=.*?&rcid=(?P<rcid>[0-9]*)\x03 \x035\*\x03 \x0303(?P<user>.*?)\x03 \x035\*\x03 \(\x02?(?P<diffsize>[+-][0-9]*)\x02?\) \x0310(?P<comment>.*)\x03'), # new page with rcid
    re.compile(r'\x0314\[\[\x0307(?P<title>.*?)\x0314\]\]\x034 (?P<flags>.*?N)\x0310 \x0302http:\/\/.*?\/wiki/.*?\x03 \x035\*\x03 \x0303(?P<user>.*?)\x03 \x035\*\x03 \(\x02?(?P<diffsize>[+-][0-9]*)\x02?\) \x0310(?P<comment>.*)\x03'), # new page without rcid
    re.compile(r'\x0314\[\[\x0307(?P<title>.*?)\x0314\]\]\x034 (?P<flags>.*?)\x0310 \x0302\x03 \x035\*\x03 \x0303(?P<user>.*?)\x03 \x035\*\x03  \x0310(?P<comment>.*)\x03') # admin options, new users, etc
    ]

parsefile = open('parseerror', 'a')
# IRC Client
class RCBot(tcp.protocols.irc.IRCClient):
    nickname = "TSRCRelay"
    realname = "Toolserver RC relay bot [[docpage]]"
    username = "tsrcrelay"
    versionName = "Toolserver RC relay bot"
    versionNum = '%s (%s)' % (__versiondict__['revision'], __versiondict__['date'])
    
    def __init__(self):
        bot.updatechannels = self.updatechannels
        
    def joined(self, channel):
        bot.channels[channel] = bot.wchannels[channel]
        
    def left(self, channel):
        bot.channels.pop(channel)
    
    def updatechannels(self):
        for channel in bot.wchannels.keys():
            print "\n%i subscribers to %s" % (len(bot.wchannels[channel]), channel)
            if len(bot.wchannels[channel]) == 0:
                bot.wchannels.pop(channel)
        
        print "Joined channels: %r" % (bot.channels.keys(),)
        joinchannels = set(bot.wchannels.keys()).difference(set(bot.channels.keys()))
        partchannels = set(bot.channels.keys()).difference(set(bot.wchannels.keys()))
        print "joining %r, parting %r" % (joinchannels, partchannels)
                
        for channel in joinchannels:
            self.join(channel)
        for channel in partchannels:
            self.leave(channel, 'No listening clients')
        
    def privmsg(self, source, target, line):
        if (source == 'rc!~rc@localhost'):
            data = None
            for r in regexps:
                m = r.match(line)
                if m:
                    data = m.groupdict()
                    data['channel'] = target
                    break
            if data == None:
                print "\nParse error: %r" % (line)
                parsefile.write(line + '\n')
                parsefile.flush()
                data = {'raw': line,
                        'channel': target}
            if target in bot.wchannels:
                print "%s%i\t" % (target[1:].split('.')[0], len(bot.wchannels[target])),
                sys.stdout.flush()
                for client in bot.wchannels[target]:
                    client.sendLine(repr(data).replace('"', '\"').replace("'", '"'))
        else:
            print '%s>%s: %s' % (source, target, line)
        
bot = tcp.protocol.ClientFactory()
bot.protocol = RCBot

bot.channels = {}
bot.wchannels = {}
bot.updatechannels = None

tcp.reactor.connectTCP("irc.wikimedia.org", 6667, bot)

# TCP reader
class RCServ(tcp.protocols.basic.LineReceiver):
    def __init__(self):
        self.channels = []
        
    def lineReceived(self, line):
        if len(line) == 0:
            return
        if (line[0] in ('J', 'j', 'A', 'a')):
            if line[2] == '#':
                channel = line[2:]
            else:
                channel = '#%s' % (line[2:],)
            channel = channel.lower().strip()
            if channel[-4:] == '.org':
                channel = channel[:-4]
            if channel not in self.channels:
                self.channels.append(channel)
                if channel in bot.wchannels:
                    bot.wchannels[channel].append(self)
                else:
                    bot.wchannels[channel] = [self,]
                bot.updatechannels()
        elif (line[0] in ('P', 'p', 'R', 'r', 'D', 'd')):
            if line[2] == '#':
                channel = line[2:]
            else:
                channel = '#%s' % (line[2:],)
            print self.channels
            print channel
            if channel in self.channels:
                self.channels.remove(channel)
                if channel in bot.wchannels:
                    bot.wchannels[channel].remove(self)
            bot.updatechannels()
        else:
            self.sendLine("{'error': 'Unknown command %r'}" % (line,))

    def connectionLost(self, reason):
        for channel in self.channels:
            if channel in bot.wchannels:
                bot.wchannels[channel].remove(self)
        bot.updatechannels()

serv = tcp.protocol.ServerFactory()
serv.protocol = RCServ
tcp.reactor.listenTCP(8267,serv,interface='127.0.0.1')

tcp.reactor.run()