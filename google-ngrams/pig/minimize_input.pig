/*  minimize_input.pig 
	Reduce file size by removing dispensable fields. */

-- declare variable(s)
%DECLARE BASE_DIR '/user/priska/data/experiments/nounargs';

-- load nounargs ( from compressed files )
ngrams = LOAD '$BASE_DIR/original.gz' USING PigStorage( '\t' );

-- remove unused frequency counts and store minified version back to disk
minified = FOREACH ngrams GENERATE $0 AS head, $1 AS ngram, $2 AS count;
STORE minified INTO '$BASE_DIR/minified.gz';
