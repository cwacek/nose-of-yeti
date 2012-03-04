from tokenize import generate_tokens
from tracker import Tracker

class Tokeniser(object):
    """Endpoint for tokenising a file"""
    def __init__(self, default_kls='object', with_describe_attrs=True, import_tokens=None):
        self.default_kls = default_kls
        self.import_tokens = import_tokens
        self.with_describe_attrs = with_describe_attrs

    ########################
    ###   TRANSLATE
    ########################

    def translate(self, readline, result=None):
        # Tracker to keep track of information as the file is processed
        self.tracker = Tracker(result, self.default_kls)
        
        # Add import stuff at the top of the file
        if self.import_tokens:
            self.tracker.addTokens(self.import_tokens)

        # Looking at all the tokens
        with self.tracker.add_phase() as tracker:
            for tokenum, value, (_, scol), _, _ in generate_tokens(readline):
                self.tracker.next_token(tokenum, value, scol)

        # Add attributes to our Describes so that the plugin can handle some nesting issues
        # Where we have tests in upper level describes being run in lower level describes
        if self.with_describe_attrs:
            self.tracker.addTokens(self.tracker.makeDescribeAttrs())
        
        # Add lines to bottom of file to add __testname__ attributes
        self.tracker.addTokens(self.tracker.makeMethodNames())
        
        # Return translated list of tokens
        return self.tracker.result
