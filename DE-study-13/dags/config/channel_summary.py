{
          'table': 'channel_summary',
          'schema': 'phvalue123',
          'main_sql': """
WITH seq_table AS
(
  SELECT
    usc.userid,
    usc.sessionid,
    usc.channel,
    ROW_NUMBER() OVER (PARTITION BY usc.userid ORDER BY st.ts) AS seq
  FROM raw_data.user_session_channel usc
  JOIN raw_data.session_timestamp st
  ON usc.sessionid = st.sessionid
)
SELECT userid,
       MAX(CASE WHEN seq = (SELECT MIN(seq) FROM seq_table t2 WHERE t2.userid = t1.userid) THEN channel END) AS first_channel,
       MAX(CASE WHEN seq = (SELECT MAX(seq) FROM seq_table t2 WHERE t2.userid = t1.userid) THEN channel END) AS last_channel
FROM seq_table t1
GROUP BY userid
ORDER BY 1;
""",
          'input_check':
          [
            {
              'sql': 'SELECT COUNT(1) FROM raw_data.user_session_channel', # 101520
              'count': 100000
            },
          ],
          'output_check':
          [
            {
              'sql': 'SELECT COUNT(1) FROM {schema}.temp_{table}',
              'count': 12
            }
          ],
}
