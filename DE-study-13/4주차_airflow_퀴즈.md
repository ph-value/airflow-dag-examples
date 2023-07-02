1. DAGs 폴더는 어디에 지정되는가?
    -  `airflow.cfg` 파일의 `dags_folder` 항목

2. DAGs 폴더에 새로운 Dag를 만들면 언제 실제로 Airflow 시스템에서 이를 알게
되나? 이 스캔 주기를 결정해주는 키의 이름이 무엇인가?
    - Airflow 스케줄러가 실행 중이고 `airflow.cfg` 파일의 `dag_dir_list_interval` 항목의 주기가 경과하면 Airflow 시스템이 DAG를 감지하고 시스템에 등록한다.

3. 이 파일에서 Airflow를 API 형태로 외부에서 조작하고 싶다면 어느 섹션을
변경해야하는가?
    -  `api` 섹션의 항목들을 수정한다.
    - `auth_backend`, `auth_backend_kwargs`, `default_timezone`, `expose_config`, `expose_metrics`, `expose_version`, `hide_paused_dags_by_default`, `worker_refresh_interval`, `worker_refresh_batch_size`, `page_size`,`max_page_limit`, `enable_proxy_fix` 항목이 있다.
  
   - api 섹션의 auth_backend를 airflow.api.auth.backend.basic_auth로 변경

4. Variable에서 변수의 값이 encrypted가 되려면 변수의 이름에 어떤 단어들이
들어가야 하는데 이 단어들은 무엇일까? :)
    - `_password`, `_secret`, `_key`, `_token`, `_encrypted`
    - (예시) `my_key` 라고 변수 이름을 정하면 암호화되어 메타데이터 데이터베이스에 저장된다.

5. 이 환경설정 파일이 수정되었다면 이를 실제로 반영하기 위해서 해야 하는 일은?
    - 서비스를 재시작한다.

6. Metadata DB의 내용을 암호화하는데 사용되는 키는 무엇인가?
    - `fernet_key` 
    - `airflow.cfg` 파일의 `core` 섹션에 있다.
    - `fernet_key` 는 대칭 키로 사용된다. 따라서 변경 시 주의해야한다!
