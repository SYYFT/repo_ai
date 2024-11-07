# ------------------------------------- imports 
import time
start = time.time()

import warnings
warnings.filterwarnings("ignore", message="Bad owner or permissions on .*connections.toml")

#---------------------- udemy utils 
from extract import fetch_udemy_tables

from load import (
    insert_user_activity,
    insert_user_assessment_activity,
    insert_user_course_activity,
    insert_user_lab_activity,
    insert_user_learning_activity_attempt,
    insert_user_path_activity
)

from transform import (
    merge_udemy_user_activity,

    
    UDEMY_USER_ACTIVITY_PROC
)

from config import ( # type: ignore
    get_audit_sid,
    USER_ACTIVITY_MODEL,
    USER_ASSESSMENT_ACTIVITY_MODEL,
    USER_COURSE_ACTIVITY_MODEL,
    USER_LAB_ACTIVITY_MODEL,
    USER_LEARNING_ACTIVITY_ATTEMPT_MODEL,
    USER_PATH_ACTIVITY_MODEL,
    UDMY_USER_ACTIVITY_TABLE,
    UDMY_USER_COURSE_ACTIVITY_TABLE,
    UDMY_USER_LAB_ACTIVITY_TABLE,
    UDMY_USER_LEARNING_ACTIVITY_ATTEMPT_TABLE,
    UDMY_USER_PATH_ACTIVITY_TABLE,
    UDMY_USER_ASSESSMENT_ACTIVITY_TABLE
)

#---------------------- master utils 
from SAMPLE_REPO.master_utils import getCredsFromAWS, getLogger, getSnowflakeEngine # type: ignore 
logger = getLogger('Udemy', 'Udemy ETL PIPELINE')
credsObj = getCredsFromAWS(['SF'])
engine = getSnowflakeEngine(credsObj)

# ------------------------------------ CALL THE FUNCTION 
def load_udemy_tables(engine):
    """Updates the Udemy tables in Snowflake with data from respective dataframes."""

    # Loading dataframes from CSV files
    print("***** Fetching data from Udemy API *****")
    USER_COURSE_ACTIVITY, USER_ACTIVITY, LEARNING_ACTIVITY_ATTEMPT_SUMMARY, USER_ASSESSMENT_ACTIVITY, USER_PATH_ACTIVITY, USER_LAB_ACTIVITY = fetch_udemy_tables(engine)
    print("***** All data retrieved successfully *****\n")

    # Insert data into tables using the dataframes and respective models
    print("Getting Snowflake Credentials from AWS")
    print("Credentials from AWS Obtained!!\n\n")
    audit_sid = get_audit_sid(engine)
    
    print(f"Inserting data from USER_ACTIVITY_DF into '{UDMY_USER_ACTIVITY_TABLE}' table...")
    insert_user_activity(USER_ACTIVITY, UDMY_USER_ACTIVITY_TABLE, engine, audit_sid, USER_ACTIVITY_MODEL)
    print("***** Successfully inserted USER_ACTIVITY_DF *****\n")
    
    audit_sid = get_audit_sid(engine)
    print(f"Inserting data from USER_PATH_ACTIVITY_DF into '{UDMY_USER_PATH_ACTIVITY_TABLE}' table...")
    insert_user_path_activity(USER_PATH_ACTIVITY, UDMY_USER_PATH_ACTIVITY_TABLE, engine, audit_sid, USER_PATH_ACTIVITY_MODEL)
    print("***** Successfully inserted USER_PATH_ACTIVITY_DF *****\n")

    audit_sid = get_audit_sid(engine)
    print(f"Inserting data from USER_ASSESSMENT_ACTIVITY_DF into '{UDMY_USER_ASSESSMENT_ACTIVITY_TABLE}' table...")
    insert_user_assessment_activity(USER_ASSESSMENT_ACTIVITY, UDMY_USER_ASSESSMENT_ACTIVITY_TABLE, engine, audit_sid, USER_ASSESSMENT_ACTIVITY_MODEL)
    print("***** Successfully inserted USER_ASSESSMENT_ACTIVITY_DF *****\n")

    audit_sid = get_audit_sid(engine)
    print(f"Inserting data from USER_COURSE_ACTIVITY_DF into '{UDMY_USER_COURSE_ACTIVITY_TABLE}' table...")
    insert_user_course_activity(USER_COURSE_ACTIVITY, UDMY_USER_COURSE_ACTIVITY_TABLE, engine, audit_sid, USER_COURSE_ACTIVITY_MODEL)
    print("***** Successfully inserted USER_COURSE_ACTIVITY_DF *****\n")

    audit_sid = get_audit_sid(engine)
    print(f"Inserting data from LEARNING_ACTIVITY_ATTEMPT_SUMMARY_DF into '{UDMY_USER_LEARNING_ACTIVITY_ATTEMPT_TABLE}' table...")
    insert_user_learning_activity_attempt(LEARNING_ACTIVITY_ATTEMPT_SUMMARY, UDMY_USER_LEARNING_ACTIVITY_ATTEMPT_TABLE, engine, audit_sid, USER_LEARNING_ACTIVITY_ATTEMPT_MODEL)
    print("***** Successfully inserted LEARNING_ACTIVITY_ATTEMPT_SUMMARY_DF *****\n")

    audit_sid = get_audit_sid(engine)
    print(f"Inserting data from USER_LAB_ACTIVITY_DF into '{UDMY_USER_LAB_ACTIVITY_TABLE}' table...")
    insert_user_lab_activity(USER_LAB_ACTIVITY, UDMY_USER_LAB_ACTIVITY_TABLE, engine, audit_sid, USER_LAB_ACTIVITY_MODEL)
    print("***** Successfully inserted USER_LAB_ACTIVITY_DF *****\n")

    print(f"***** UDEMY data loading completed *****")




def transform_udemy_tables(engine):
    """Updates the Udemy tables in Snowflake and calls stored procedure to merge into Prod tables - eliminating duplicates"""

    print("Getting Audit SID...")
    audit_sid = get_audit_sid(engine)
    print("***** Starting Transformations *****\n")
    print(f"Starting Stored Procedure: {UDEMY_USER_ACTIVITY_PROC}")
    merge_udemy_user_activity(engine, audit_sid)
    print("***** Successfully processed USER_ACTIVITY from Stage to Prod *****\n")
    return



def etl(engine):
    load_udemy_tables(engine)
    transform_udemy_tables(engine)

    end = time.time()
    total_time = end - start
    return print(f"SUCCESS: UDEMY ETL COMPLETED in {total_time:.2f} seconds ")



etl(engine)