# ✨ 실리콘밸리에서 날아온 데이터 엔지니어링 스타터 키트 with Python

## 4주차
[퀴즈](./4%EC%A3%BC%EC%B0%A8_airflow_%ED%80%B4%EC%A6%88.md)
 
[세계 나라 정보 API 사용 DAG 작성](./WorldCountriesInfo.py)

## 5주차
[애플 주가 Incremental Update 방식 DAG 작성](./UpdateSymbol_v3.py)

---
## 6주차
[mysql -> s3 -> redshift (full-refresh 방식)](./MySQL_to_Redshift.py)
[mysql -> s3 -> redshift (Incremental Update 방식)](./MySQL_to_Redshift_v2.py)

- airflow cli에서 backfill 실행 명령어 예시:
    ```
    airflow dags backfill dag_id -s 2018-07-01 -e 2018-08-01
    ```
    - 전제조건: 
    1. catchUp이 True여야 함.
    2. execution date를 쓰는 Incremental Update 방식인 DAG여야 함. -> 당연함. full-refresh 방식이라면 그냥 한번 실행 해주면 되니까.

    - 유의사항
        - 이미 작동 중이던 dag였다면, backfill 지정 기간 중 성공한 날짜가 있다면 그 날짜는 skip된다.
        - 위의 예시의 겅우 1일 부터 순차적으로 실행되지는 않는다. 실행 날짜가 랜덤하게 널뛴다!
        날짜 순차적으로 하고 싶다면 DAG default_args의 depends_on_past를 true로 설정해야한다.

- Summary Table을 포함한 간단한 DAG 구현 해보기.
    - DBT의 필요성: 
        - CTAS(Create Table As Select) 앞뒤로 TEST를 많이 붙이기가 쉽지않음
        - ELT로 데이터를 조작할 때 기록이 안 남기 때문에(어제는 어땠고, 지난주는 어땠는지)
        - DBT를 많이 사용하는 직군은 Analytics Engineer.
