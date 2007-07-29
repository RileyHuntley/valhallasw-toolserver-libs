
__version__ = "$Id$"
__versiondict__ = re.match("\$Id: (?P<file>.*?) (?P<revision>[0-9]*) (?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2}) (?P<time>[0-9]{2}:[0-9]{2}:[0-9]{2})(?P<timezone>.*?) (?P<user>.*) \$", __version__).groupdict()

class tcp:
    class protocols:
        from twisted.words.protocols import irc
        from twisted.protocols import basic
    from twisted.internet import reactor, protocol
    
import re

# IRC Client
class RCBot(tcp.protocols.irc.IRCClient):
    nickname = "TSRCRelay"
    realname = "Toolserver RC relay bot [[docpage]]"
    username = "tsrcrelay"
    versionName = "Toolserver RC relay bot"
    versionNum = '%s (%s)' % (__versiondict__['revision'], __versiondict__['date'])
    
    def signedOn(self):
        self.join('#nl.wikipedia')
    
    def privmsg(self, source, target, data):
        print 'Message: source [%s] target [%s] data [%s]' % (source, target, data)
        
f = tcp.protocol.ClientFactory()
f.protocol = RCBot

tcp.reactor.connectTCP("irc.wikimedia.org", 6667, f)
tcp.reactor.run()