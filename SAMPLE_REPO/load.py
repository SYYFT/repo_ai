from datetime import datetime
import os 
import sys


#--------------------------- utils for inserting data into snowflake 
from config import ( # type: ignore
    insert_log_audit,
 )

# #---------------------- master utils 
current_path = os.path.dirname(os.path.realpath(__file__))
the_path = os.path.join(current_path, '../Common_Utilities')
sys.path.append(os.path.abspath(the_path))

from SAMPLE_REPO.master_utils import getLogger  #type:ignore
logger = getLogger('Udemy', 'Udemy to Snowflake ETL')


def insert_user_activity(df, table_name, engine, audit_sid, USER_ACTIVITY_MODEL):
    """ Writes a DataFrame to Snowflake, appending rows without overwriting. Logs each insert's success or failure."""

    df['audit_sid'] = audit_sid
    df['load_dt'] = datetime.now()  
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False, dtype=USER_ACTIVITY_MODEL)
        print(f"{len(df)} rows successfully inserted into {table_name}.")
        insert_log_audit(engine, audit_sid, "Insert USER_ACTIVITY to Snowflake", "Load", "insert_user_activity.py", 
                         "Data inserted successfully", "SUCCESS")
    except Exception as e:
        error_message = str(e)
        summary = str(e).split('\n')[0][:95]
        print(f"Failed to insert data: {summary}")
        insert_log_audit(engine, audit_sid, "Insert USER_ACTIVITY to Snowflake", "Load", "insert_user_activity.py", 
                         error_message, "FAIL")


def insert_user_assessment_activity(df, table_name, engine, audit_sid, USER_ASSESSMENT_ACTIVITY_MODEL):
    """ Writes a DataFrame to Snowflake, appending rows without overwriting. Logs each insert's success or failure."""
    df['audit_sid'] = audit_sid
    df['load_dt'] = datetime.now()  
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False, dtype=USER_ASSESSMENT_ACTIVITY_MODEL)
        print(f"{len(df)} rows successfully inserted into {table_name}.")
        insert_log_audit(engine, audit_sid, "Insert USER_ASSESSMENT_ACTIVITY to Snowflake", "Load", 
                         "insert_user_assessment_activity.py", "Data inserted successfully", "SUCCESS")
    except Exception as e:
        error_message = str(e)
        summary = str(e).split('\n')[0][:95]
        print(f"Failed to insert data: {summary}")
        insert_log_audit(engine, audit_sid, "Insert USER_ASSESSMENT_ACTIVITY to Snowflake", "Load", 
                         "insert_user_assessment_activity.py", error_message, "FAIL")


def insert_user_course_activity(df, table_name, engine, audit_sid, USER_COURSE_ACTIVITY_MODEL):
    """ Writes a DataFrame to Snowflake, appending rows without overwriting. Logs each insert's success or failure."""
    df['audit_sid'] = audit_sid
    df['load_dt'] = datetime.now()  
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False, dtype=USER_COURSE_ACTIVITY_MODEL)
        print(f"{len(df)} rows successfully inserted into {table_name}.")
        insert_log_audit(engine, audit_sid, "Insert USER_COURSE_ACTIVITY to Snowflake", "Load", 
                         "insert_user_course_activity.py", "Data inserted successfully", "SUCCESS")
    except Exception as e:
        error_message = str(e)
        summary = str(e).split('\n')[0][:95]
        print(f"Failed to insert data: {summary}")
        insert_log_audit(engine, audit_sid, "Insert USER_COURSE_ACTIVITY to Snowflake", "Load", 
                         "insert_user_course_activity.py", error_message, "FAIL")


def insert_user_lab_activity(df, table_name, engine, audit_sid, USER_LAB_ACTIVITY_MODEL):
    """ Writes a DataFrame to Snowflake, appending rows without overwriting. Logs each insert's success or failure."""
    df['audit_sid'] = audit_sid
    df['load_dt'] = datetime.now()  
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False, dtype=USER_LAB_ACTIVITY_MODEL)
        print(f"{len(df)} rows successfully inserted into {table_name}.")
        insert_log_audit(engine, audit_sid, "Insert USER_LAB_ACTIVITY to Snowflake", "Load", 
                         "insert_user_lab_activity.py", "Data inserted successfully", "SUCCESS")
    except Exception as e:
        error_message = str(e)
        summary = str(e).split('\n')[0][:95]
        print(f"Failed to insert data: {summary}")
        insert_log_audit(engine, audit_sid, "Insert USER_LAB_ACTIVITY to Snowflake", "Load", 
                         "insert_user_lab_activity.py", error_message, "FAIL")


def insert_user_path_activity(df, table_name, engine, audit_sid, USER_PATH_ACTIVITY_MODEL):
    """ Writes a DataFrame to Snowflake, appending rows without overwriting. Logs each insert's success or failure."""
    df['audit_sid'] = audit_sid
    df['load_dt'] = datetime.now()  
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False, dtype=USER_PATH_ACTIVITY_MODEL)
        print(f"{len(df)} rows successfully inserted into {table_name}.")
        insert_log_audit(engine, audit_sid, "Insert USER_PATH_ACTIVITY to Snowflake", "Load", 
                         "insert_user_path_activity.py", "Data inserted successfully", "SUCCESS")
    except Exception as e:
        error_message = str(e)
        summary = str(e).split('\n')[0][:95]
        print(f"Failed to insert data: {summary}")
        insert_log_audit(engine, audit_sid, "Insert USER_PATH_ACTIVITY to Snowflake", "Load", 
                         "insert_user_path_activity.py", error_message, "FAIL")


def insert_user_learning_activity_attempt(df, table_name, engine, audit_sid, USER_LEARNING_ACTIVITY_ATTEMPT_MODEL):
    """ Writes a DataFrame to Snowflake, appending rows without overwriting. Logs each insert's success or failure."""
    df['audit_sid'] = audit_sid
    df['load_dt'] = datetime.now()  
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False, dtype=USER_LEARNING_ACTIVITY_ATTEMPT_MODEL)
        print(f"{len(df)} rows successfully inserted into {table_name}.")
        insert_log_audit(engine, audit_sid, "Insert USER_LEARNING_ACTIVITY_ATTEMPT to Snowflake", "Load", 
                         "insert_user_learning_activity_attempt.py", "Data inserted successfully", "SUCCESS")
    except Exception as e:
        error_message = str(e)
        summary = str(e).split('\n')[0][:95]
        print(f"Failed to insert data: {summary}")
        insert_log_audit(engine, audit_sid, "Insert USER_LEARNING_ACTIVITY_ATTEMPT to Snowflake", "Load", 
                         "insert_user_learning_activity_attempt.py", error_message, "FAIL")