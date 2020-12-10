/.*/ {
  if ( $(NF-1) ~ /\(/ )
  {
    all_neg_count++; print "-", ",", $1, ",", $(NF-1);
  }
  else if ( $(NF-1) ~ /-/ )
  {
    if ( $(NF-1) < -10 )
    {
        m10p_neg_count++;

        if ( $(NF-1) < -20 )
        {
            m20p_neg_count++;

            if ( $(NF-1) < -30 )
            {
                m30p_neg_count++;
            }
        }
    }

    all_neg_count++; print "-", ",", $1, ",", $(NF-1);
  }
  else
  {
    if ( $(NF-1) > 10 )
    {
        m10p_pos_count++;

        if ( $(NF-1) > 20 )
        {
            m20p_pos_count++;

            if ( $(NF-1) > 30 )
            {
                m30p_pos_count++;
            }
        }
    }

    all_pos_count++; print "+", ",", $1, ",", $(NF-1);
  }
}

END {
        printf("\n");

        printf("+,all_positive, %d\n", all_pos_count);
        printf("-,all_negative, %d\n", all_neg_count);
        printf("?,all_hit_rate, %d %\n", all_pos_count*100/(all_pos_count+all_neg_count));

        printf("\n");

        printf("+,more_than_10p_positive, %d\n", m10p_pos_count);
        printf("-,more_than_10p_negative, %d\n", m10p_neg_count);
        printf("?,more_than_10p_hit_rate, %d %\n", m10p_pos_count*100/(m10p_pos_count+m10p_neg_count));

        printf("\n");

        printf("+,more_than_20p_positive, %d\n", m20p_pos_count);
        printf("-,more_than_20p_negative, %d\n", m20p_neg_count);
        printf("?,more_than_20p_hit_rate, %d %\n", m20p_pos_count*100/(m20p_pos_count+m20p_neg_count));

        printf("\n");

        printf("+,more_than_30p_positive, %d\n", m30p_pos_count);
        printf("-,more_than_30p_negative, %d\n", m30p_neg_count);
        printf("?,more_than_30p_hit_rate, %d %\n", m30p_pos_count*100/(m30p_pos_count+m30p_neg_count));
}
