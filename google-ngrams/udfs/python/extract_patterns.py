from pig_util import outputSchema
import re
 
@outputSchema('signature:chararray')
def signature( head, ngram ):
    """

    """
    try:
        tokens    = ngram.split( ' ' )
        head_pos  = str([ i for i,t in enumerate( tokens ) if t.startswith( head + "/" ) ][0] + 1 )

        patterns = [ 
            r' ([\w]+)/JJ/[\w]+/%s'  %  head_pos,   # amod
            r' ([\w]+)/VBN/[\w]+/%s' %  head_pos,   # amod, partmod, dep
            r' ([\w]+)/NNP/[\w]+/%s' %  head_pos    # nn, amod
        ]

        signature = None
        for p in patterns:
            match = re.search( p, ngram )
            if match:
                signature = "{___} may be %s" % match.group(1)
        
        return signature

    except ValueError:
        return None
