import re
from string import Template

try:
    import simplejson as json
except ImportError:
    import json

class Extractor( object ):
    """
    A simple extractor object which defines a filter over Google's syntactic n-grams.
    For instance, a selector of all n-grams where the head word is preceded by an 
    adjective. The extractor should specify its name, extraction pattern ( as regular 
    expression ), template ( human-readable ) and factoid.

    E.g.
        name: 'adjective'
        extraction pattern: r'([\w-]+/JJ/amod/'
        template: '{___} may be %s'  # placeholder will be filled with pattern match
        factoid: '{%s} may be %s'    # placeholders to be filled with head word and match
    """

    def __init__( self, name, pattern, template, factoid ):
        self.name     = name
        self.pattern  = Template( pattern )
        self.template = template
        self.factoid  = factoid
    
    def update( self, head, match ):
        tokens = match.group(1).split( ' ' )
        text = ''
        tags = ''
        for t in tokens:
            items = t.split( '/' )
            text += ( items[0] + ' ' )
            tags += ( items[1] + '/' + items[2] + ' ' ) 

        self.template = self.template % ( text )
        self.factoid = self.factoid  % ( head, text )
        self.tags = tags


def get_extractors():
    """
    Customize your extractors here;
    specify <name>, <regular expression>, <template>, <factoid>.

    TODO: allow filters for selecting subsets of specified extractors.
    """
    extractors = []
    aword = r'[\w\.-]+'  # spec for a word

    # adjectives right before head noun
    extractors.append( Extractor(
        "adjective",
        r'\b(%s/JJ/amod/${head_pos}) ${head}/' % aword,
        "{___} may be %s", # template
        "{%s} may be %s",  # factoid
    ))
    # gerunds before head noun
    extractors.append( Extractor(
        "gerund",
        r'\b(%s/VBN/\w+/${head_pos}) ${head}/' % aword,
        "{___} may be %s",
        "{%s} may be %s",
    ))
    # VBG
    extractors.append( Extractor(
        "VBG",
        r'\b(%s/VBG/\w+/${head_pos}) ${head}/' % aword,
        "{___} may be %s",
        "{%s} may be %s",
    ))
    # coordination constructs with a possessive pronoun
    extractors.append( Extractor(
        "possessive",
        r'\band/CC/cc/${head_pos} %s/PRP.?/poss/\d+ ([\w-]+/NN/\w+/)' % aword, # $head_pos in the end ?
        "{___} may have %s",
        "{%s} may have %s",
    ))
    # coordination constructs
    extractors.append( Extractor(
        "coordination",
        r'\b(?:and|or)/CC/cc/${head_pos} .* (%s/NN/[\w]+/${head_pos})' % aword,
        "{___} and %s",
        "{%s} and %s",
    ))
    # compound nouns
    extractors.append( Extractor(
        "compounds",
        r'\b(%s/NNP?/nn/${head_pos} ${head}/NNP?/(?:conj|pobj|dobj)/)' % aword,
        "{___} may be %s",
        "{%s} may be %s",
    ))

    # return json.dumps( extractors )
    return extractors
