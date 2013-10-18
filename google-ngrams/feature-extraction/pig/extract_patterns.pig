/** 
    extract_patterns.pig 
    
    Extract signatures from syntactic n-grams; 
    cf. e.g. in the following: head \t signature \t count
    earth   {___} may be natural    16 
  */

-- enable compression for intermediate results
SET pig.tmpfilecompression 'true';
SET pig.tmpfilecompression.codec 'gz';

-- declare variables
-- %DEFAULT BASE_DIR '/mnt/hdfs/user/priska/data/nounargs'; -- local
%DEFAULT BASE_DIR '/user/priska/data/nounargs'; -- hdfs
%DECLARE INPUT_DIR '$BASE_DIR/minified.gz';
%DECLARE OUTPUT_DIR '$BASE_DIR/signature.gz';

-- register user-defined functions ( UDF )
REGISTER '../udfs/python/extract_patterns.py' USING streaming_python AS extract_patterns;

-- load nounargs and split them into components
nounargs = LOAD '$INPUT_DIR' USING PigStorage( '\t' ) AS ( head: chararray, ngram: chararray, count: int );

-- filter nounargs for specific patterns, s. extract_patterns.py
patterns = FOREACH nounargs GENERATE head, extract_patterns.signature( head, ngram ) AS signature, count;
patterns = FILTER patterns BY signature is not null;

-- remove old results, store new ones
rmf $OUTPUT_DIR;
STORE patterns INTO '$OUTPUT_DIR' USING PigStorage( '\t' );
