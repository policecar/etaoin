/**
    minimize_input.pig 
  
    Reduce file size by removing dispensable fields.
    Note: makes for 2.1G instead of 11G here.
  */

-- declare variables
%DEFAULT BASE_DIR '/user/priska/data/experiments/nounargs';
%DECLARE INPUT_DIR '$BASE_DIR/original.gz';
%DECLARE OUTPUT_DIR '$BASE_DIR/minified.gz';

-- load nounargs ( from compressed files )
ngrams = LOAD '$INPUT_DIR' USING PigStorage( '\t' );

-- remove unused fields, here: frequency counts over time
minified = FOREACH ngrams GENERATE $0 AS head, $1 AS ngram, $2 AS count;

-- remove old results, store new results
rmf $OUTPUT_DIR;
STORE minified INTO '$OUTPUT_DIR';
