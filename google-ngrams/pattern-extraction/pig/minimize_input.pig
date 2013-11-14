/**
    minimize_input.pig 
  
    Reduce file size by removing dispensable fields.
    Note: reduces 11G to 2.1G here.
  */

-- declare variables
-- %DEFAULT BASE_DIR '/mnt/hdfs/user/priska/data/nounargs'; -- local mode
%DEFAULT BASE_DIR '/user/priska/data/nounargs'; -- mapreduce mode
%DEFAULT INPUT_DIR '$BASE_DIR/original.gz';
%DEFAULT OUTPUT_DIR '$BASE_DIR/minified.gz';

-- load nounargs ( from compressed files )
ngrams = LOAD '$INPUT_DIR' USING PigStorage( '\t' );

-- remove unused fields, here: frequency counts over time
minified = FOREACH ngrams GENERATE $0 AS head, $1 AS ngram, $2 AS count;

-- remove old results, store new results
rmf $OUTPUT_DIR;
STORE minified INTO '$OUTPUT_DIR';
