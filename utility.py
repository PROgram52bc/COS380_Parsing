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
        if isinstance(other, self.__class__):
            return self.head == other.head and self.body == other.body
        else:
            print("__eq__ in Rule failed:")
            print(other.__class__, "is not", self.__class__)
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
        """ short cut to add many one-element rules """
        for rule in args:
            self.addRule(rule)
        return self
    def isPOS(self):
        """ returns true if every rule has a single string """
        return all(rule.isPOS() for rule in self._rules)
    def __repr__(self):
        return "<Lexicon {}>".format(self.name)
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        else:
            return False

class Rules:
    """ a collection of rules """
    def __init__(self):
        self._rules = []
        self._lexicons = {}
    def hasLexicon(self, name):
        return name in self._lexicons
    def getLexicon(self, name):
        """ returns the lexicon with 'name' if it exists, otherwise create an empty lexicon and return it """
        if name not in self._lexicons:
            self._lexicons[name] = Lexicon(name)
        return self._lexicons[name]
    def addRule(self, head, body):
        """ head is a lexicon|string, body is a list or tuple of lexicon(s)
        This method does not make copy. To ensure unique rule objects in the collection, client should either call 'addRuleCopy' method or call getLexicon() method to get the lexicon to pass them as arguments
        This method does equality check before adding to the collection, so if the rule already exists, it will not be added again.
        returns the rule added, if any, otherwise returns None
        """
        if isinstance(head, str):
            head = self.getLexicon(head)
        rule = Rule(head, body)
        if rule not in self._rules:
            self._rules.append(Rule(head, body))
            head.addRule(*body)
            # print("Added new rule", rule)
            return rule
    def addRuleCopy(self, head, body):
        """ same as addRule, but make a copy of the rule's component instead of linking directly to it """
        # copy the head
        headCopy = self.getLexicon(head.name) if isinstance(head, Lexicon) else self.getLexicon(head)
        # copy the body
        bodyCopy = [ self.getLexicon(lexicon.name) if isinstance(lexicon, Lexicon) else lexicon for lexicon in body ]
        return self.addRule(headCopy, bodyCopy)
    def fromLexicon(self, lexicon, recursive=True):
        """ add rules from a lexicon, if lexicon's name already exists in rule, it will be ignored to prevent from infinite recursion """
        if (not isinstance(lexicon, Lexicon) or
            lexicon.name in self._lexicons): return
        for rule in lexicon.getRules():
            if recursive: 
                # handles recursion first, otherwise the children will be ignored because they already exist in the collection
                for bodyLexicon in rule.body:
                    self.fromLexicon(bodyLexicon, True)
            self.addRuleCopy(rule.head, rule.body)
        return self
    def getRules(self, lmda = lambda r : True):
        """ get rules that satisfy lmda(r) """
        return [ r for r in self._rules if lmda(r) ]
    def __contains__(self, item):
        return item in self._rules

