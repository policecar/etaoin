/** 
    extract_patterns.pig 
    
    Extract patterns from syntactic n-grams; e.g.
    
    becomes
    earth   {___} may be natural    16 
  */

-- enable compression for intermediate results
SET pig.tmpfilecompression 'true';
SET pig.tmpfilecompression.codec 'gz';

-- declare variables
-- %DEFAULT BASE_DIR '/mnt/hdfs/user/priska/data/nounargs'; -- local
%DEFAULT BASE_DIR '/user/priska/data/nounargs'; -- hdfs
%DEFAULT INPUT_DIR '$BASE_DIR/minified.gz';
%DEFAULT OUTPUT_DIR '$BASE_DIR/inspect.gz';

-- register user-defined functions ( UDF )
REGISTER '../udfs/python/extraction_utils.py' USING streaming_python AS utils;
REGISTER '../udfs/python/inflect.py' USING streaming_python AS inflect;

-- load nounargs and split them into components
nounargs = LOAD '$INPUT_DIR' USING PigStorage('\t') AS ( head:chararray, ngram:chararray, count:int );

-- escape head noun for regex matching and compute position of head word
nounargs = FOREACH nounargs GENERATE head, ngram, count,
    utils.get_escaped_head( head ) AS headesc, utils.get_head_pos( head, ngram ) AS headpos;

-- filter nounargs for specific patterns
-- adjectives
adjectives = FILTER nounargs BY ( ngram MATCHES CONCAT( CONCAT( '.*\\b[^\\s]+/JJ/amod/', headpos ), '.*' ));
adjectives = FOREACH adjectives GENERATE inflect.singularize( head ), headpos, CONCAT( '{___} may be ', 
    REGEX_EXTRACT( ngram, CONCAT( CONCAT( '.*\\b([^\\s]+)/JJ/amod/', headpos ), '.*' ), 1 )) AS signature, count, ngram;

-- compound nouns
compounds = FILTER nounargs BY ( ngram MATCHES 
    '.*\\b[^\\s]+/NN.?/[a-z]+/[\\d]+ \\b[^\\s]+/NN.?/[a-z]+/[\\d]+.*' );
compounds = FOREACH compounds GENERATE head, CONCAT( '{___} may be ', utils.get_compound_noun( ngram )) AS signature, count, ngram;
compounds = FILTER compounds BY signature is not null;

-- coordination constructs  ( stored as is for now )
coordination = FILTER nounargs BY ( ngram MATCHES '.*/CC/cc/.*' );

-- remove old results, store new ones
rmf $OUTPUT_DIR;
STORE adjectives INTO '$OUTPUT_DIR/adjectives' USING PigStorage('\t');
STORE compounds INTO '$OUTPUT_DIR/compounds' USING PigStorage('\t');
STORE coordination INTO '$OUTPUT_DIR/coordination' USING PigStorage('\t');
