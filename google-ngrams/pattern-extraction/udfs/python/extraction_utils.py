#! /usr/bin/env python
try:
    from pig_util import outputSchema
except ImportError:
    from streaming.pig_util import outputSchema

# try:
#     from IPython import embed
# except ImportError:
#     pass

import re

@outputSchema('headesc:chararray')
def get_escaped_head( head ):
    """
    Returns escaped head noun.
    """
    try:
        return re.escape( head )    
    except ValueError:
        return None


@outputSchema('headpos:chararray')
def get_head_pos( head, ngram ):
    """
    Returns index of head noun in n-gram ( w/ 1 as first index, not 0 ).
    """
    try:
        tokens = ngram.split( ' ' )
        return str([ i for i, t in enumerate( tokens ) if t.startswith( head + "/" )][0] + 1 )
    except ValueError:
        return None


@outputSchema('compoundnoun:chararray')
def get_compound_noun( ngram ):
    """
    Extracts compound nouns involving the head noun from n-gram and returns its text.
    """
    try:
        pattern = re.compile( '((?: ?\\b[^\\s]+(?:/NN.?/[a-z]+/[\\d]+)){2,})' )
        match = re.search( pattern, ngram )
        if match:
            compound = ''
            contains_root = False
            tokens = match.group().strip().split(' ')
            for t in tokens:
                # embed()
                items = t.split('/')
                compound += ( items[0] + ' ' )
                if items[3] == 0:
                    contains_root = True
            if contains_root:
                return compound
            else:
                return None
        else:
            return None
            
    except ValueError:
        return None


if __name__ == '__main__':
    print get_compound_noun( "rarity/NN/pobj/0 and/CC/cc/2 value/NN/conj/2 rug/NN/pobj/5" )
