/.*/ {
  if ( $(NF-1) ~ /\(/ )
  {
    neg_count++; print "-", ",", $1, ",", $(NF-1);
  }
  else if ( $(NF-1) ~ /-/ )
  {
    neg_count++; print "-", ",", $1, ",", $(NF-1);
  }
  else
  {
    pos_count++; print "+", ",", $1, ",", $(NF-1);
  }
}

END {
        printf("\n+,positive, %d\n", pos_count);
        printf("\n-,negative, %d\n", neg_count);
        printf("\n?,hit rate, %d %\n", pos_count*100/(pos_count+neg_count));
}
