class Rule:
    """ defines a grammatical rule of the form:
    lexicon => (lexicon | string) +
    """
    def __init__(self, head, body):
        """ 'head' should be a lexicon, 
        'body' should be a tuple of (lexicon | string)s """
        if not isinstance(head, Lexicon):
            raise Exception("head should be a lexicon object")
        self.head = head
        if not isinstance(body, (list, tuple)):
            raise Exception("body must be a list or a tuple")
        self.body = tuple(body)
    def isPOS(self):
        """ return true if the rule has only one string as its body """
        return len(self.body) == 1 and isinstance(self.body[0], str)
    def __repr__(self):
        return "<Rule {} => {}>".format(repr(self.head), repr(self.body))
    def __eq__(self, other):
        if isinstance(other, Rule):
            return self.head == other.head and self.body == other.body
        else:
            return False


class Lexicon:
    """ defines the lexicon class """
    def __init__(self, name):
        self.name = name
        self._rules = []
    def addRule(self, *args):
        self._rules.append(Rule(self, args))
        return self
    def getRules(self, lmda = lambda r : True):
        """ get rules that satisfy lmda(r) """
        return [ r for r in self._rules if lmda(r) ]
    def addRules(self, *args):
        for rule in args:
            self.addRule(rule)
        return self
    def isPOS(self):
        """ returns true if every rule has a single string """
        return all(rule.isPOS() for rule in self._rules)
    def __repr__(self):
        return "<Lexicon {}>".format(self.name)
