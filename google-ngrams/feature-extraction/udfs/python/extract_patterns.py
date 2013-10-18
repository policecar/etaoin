#! /usr/bin/env python
try:
    from pig_util import outputSchema
except ImportError:
    from streaming.pig_util import outputSchema

import re
import extractors as extract

@outputSchema('signature:chararray')
def signature( head, ngram ): # , extractors
    """
    """
    try:
        tokens    = ngram.split( ' ' )
        head_pos  = str([ i for i, t in enumerate( tokens ) if t.startswith( head + "/" )][0] + 1 )

        extractors = extract.get_extractors()
        # extractors = json.loads( extractors )
        substitutions = {
            'head' : re.escape( head ),
            'head_pos' : head_pos,
        }
        signature = None

        for extractor in extractors:
            pattern = extractor.pattern.substitute( substitutions )
            pattern = re.compile( pattern )
            match = re.search( pattern, ngram )
            if match:
                # print match.group(1)
                extractor.update( head, match )
                signature = ( '\t' ).join([ extractor.template, extractor.factoid, extractor.tags ])
                continue

        return signature

    except ValueError:
        return None


if __name__ == '__main__':
    signature( "march", 'the/DT/det/2 march/NN/dobj/0 and/CC/cc/2 their/PRP$/poss/2 body/NN/pobj/3')
    # signature( u'o', u'foo\dbaz/NNP/nn/2 o/NNP/pobj/0' )