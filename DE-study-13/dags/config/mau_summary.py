{
          'table': 'mau_summary',
          'schema': 'phvalue123',
          'main_sql': """
SELECT TO_CHAR(DATE_TRUNC('month', st.ts), 'YYYY-MM') AS year_month, COUNT(DISTINCT uc.userid) AS MAU
FROM raw_data.user_session_channel uc
INNER JOIN raw_data.session_timestamp st ON uc.sessionid = st.sessionid
GROUP BY DATE_TRUNC('month', st.ts)
ORDER BY 1 asc; 
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
              'count': 7
            }
          ],
}
