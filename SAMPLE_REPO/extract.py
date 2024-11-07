import time
start = time.time()

# ------------------------------------- imports 
from datetime import datetime, timedelta, timezone
import requests
import base64
import pandas as pd
import json
import sys 
import os 


from config import (base_url_user_course_activity, base_url_learning_activity_attempt,  # type: ignore
                   base_url_user_assessment_activity, base_url_user_path_activity, 
                   base_url_user_lab_activity, headers, base_url_user_activity,
                     
                   insert_log_audit, get_audit_sid
                   
)



#---------------------- master utils 
from SAMPLE_REPO.master_utils import getLogger #type: ignore
logger = getLogger('Udemy', 'Udemy Pipeline')


# ------------------------------------------------------- Function to fetch data from Udemy API
def fetch_data_from_udemy_api(base_url, headers, logger, activity_type, engine, audit_sid):
    """
    Generalized function to fetch paginated data from Udemy API.
    :param base_url: URL for the Udemy API endpoint
    :param headers: Request headers
    :param logger: Logger instance
    :param activity_type: Description of activity type (for logging)
    :param engine: Database connection engine for logging
    :param audit_sid: Audit SID for logging
    :return: List of all data records
    """
    all_data = []
    page = 1

    logger.info(f"Starting data fetch from Udemy API for {activity_type}.")
    logger.debug(f"Base URL: {base_url}")
    
    try:
        while True:
            logger.info(f"Fetching page {page} of {activity_type}...")
            response = requests.get(f"{base_url}?page={page}&start_time=2024-01-01T00:00:00Z", headers=headers)

            if response.status_code != 200:
                error_message = f"Failed to fetch data: Status Code: {response.status_code}, {response.text}"
                logger.error(error_message)
                insert_log_audit(engine, audit_sid, f"Fetch {activity_type} Data", "Extract", 
                                 "fetch_data_from_udemy_api.py", error_message, "FAIL")
                raise Exception(error_message)
            try:
                data = response.json()
                logger.debug(f"Data fetched for page {page}: {json.dumps(data, indent=2)}")
            except json.JSONDecodeError as e:
                error_message = f"Failed to decode JSON for page {page}: {str(e)}"
                summary = str(e).split('\n')[0][:95]
                logger.error(error_message)
                insert_log_audit(engine, audit_sid, f"Fetch {activity_type} Data", "Extract", 
                                 "fetch_data_from_udemy_api.py", summary, "FAIL")
                raise Exception(error_message)
            if 'results' in data:
                all_data.extend(data['results'])
                logger.info(f"Page {page} successfully fetched and data appended. Total records so far: {len(all_data)}")
            else:
                logger.warning(f"No 'results' key found in page {page}. Ending fetch.")
                break
            if 'next' not in data or not data['next']:
                logger.info(f"No more pages to fetch. Data fetching completed for {activity_type}.")
                break
            page += 1
        success_message = f"Data fetch completed successfully for {activity_type}. Total records fetched: {len(all_data)}"
        logger.info(success_message)
        insert_log_audit(engine, audit_sid, f"Fetch {activity_type} Data", "Extract", 
                         "fetch_data_from_udemy_api.py", success_message, "SUCCESS")   
    except Exception as e:
        error_message = str(e)
        summary = error_message.split('\n')[0][:95]
        print(f"Failed to fetch data: {summary}")
        insert_log_audit(engine, audit_sid, f"Fetch {activity_type} Data", "Extract", 
                         "fetch_data_from_udemy_api.py", summary, "FAIL")
        raise  

    return all_data


# ------------------------------------------------------- Unique Courses
def print_course_activity_summary(user_course_activity_df):
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    
    # Ensure course_start_date is properly converted to a datetime with timezone awareness
    user_course_activity_df['course_start_date'] = pd.to_datetime(
        user_course_activity_df['course_start_date'], errors='coerce', utc=True
    )

    # Filter courses started in the past week
    recent_courses = user_course_activity_df[
        user_course_activity_df['course_start_date'] >= one_week_ago
    ].dropna(subset=['course_id'])

    # Get unique course details
    unique_courses = recent_courses[['course_id', 'course_title', 'course_category']].drop_duplicates()
    num_unique_courses = unique_courses['course_id'].nunique()

    # Extract topics and participant emails
    course_topics = unique_courses['course_title'].unique()
    aaretians = recent_courses['user_email'].unique()

    # Print summary in a structured format
    print("*************** Udemy Course Activity Summary ***************")
    print(f"** Course Activity from the Past Week **")
    print(f"Total Courses Started: {len(recent_courses)}")
    print(f"Unique Courses: {num_unique_courses}")
    print("------------------------------------------------------------")

    print("** Topics Include **")
    print("| {:<40} | {:<20} |".format("Course Title", "Category"))
    print("|" + "-" * 62 + "|")
    for _, row in unique_courses.iterrows():
        print("| {:<40} | {:<20} |".format(row['course_title'], row['course_category']))
    
    print("------------------------------------------------------------")
    print(f"** AAretians Participated: {len(aaretians)} **")
    print("Participants Emails:")
    print(", ".join(aaretians))
    print("************************************************************")



# ------------------------------------------------------- Function to fetch learning activity attempt summary for the last 90 days
def fetch_learning_attempt_last_90_days(base_url_learning_activity_attempt, headers, logger, engine, audit_sid, activity_type="Learning Attempt Summary", days=90):
    """
    Fetch data for learning attempts within the last specified number of days from the Udemy API.
    :param base_url_learning_activity_attempt: Base URL for the learning attempt summary endpoint
    :param headers: Request headers for authentication
    :param logger: Logger instance
    :param engine: Database connection engine for logging
    :param audit_sid: Audit SID for logging
    :param activity_type: Description of the activity type for logging
    :param days: Number of days for the date range (default is 90)
    :return: DataFrame containing learning attempt data
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    last_activity_time_from = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    last_activity_time_to = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    url_with_params = f"{base_url_learning_activity_attempt}?last_activity_time_from={last_activity_time_from}&last_activity_time_to={last_activity_time_to}"

    logger.info(f"Fetching data for {activity_type} from the last {days} days.")
    logger.debug(f"Full URL with parameters: {url_with_params}")

    try:
        response = requests.get(url_with_params, headers=headers)
        if response.status_code == 200:
            logger.info(f"Response succeeded for {activity_type}.")
            df = pd.DataFrame(response.json().get('results', []))

            # Log success
            success_message = f"Data fetch completed successfully for {activity_type}."
            insert_log_audit(engine, audit_sid, f"Fetch {activity_type} Data", "Extract", "fetch_learning_attempt_last_90_days.py", success_message, "SUCCESS")
            logger.info(success_message)

        else:
            error_message = f"Request failed with status code {response.status_code}: {response.text}"
            summary = error_message.split('\n')[0][:95]
            logger.error(error_message)
            insert_log_audit(engine, audit_sid, f"Fetch {activity_type} Data", "Extract", "fetch_learning_attempt_last_90_days.py", summary, "FAIL")
            raise Exception(error_message)

    except Exception as e:
        error_message = str(e)
        summary = error_message.split('\n')[0][:95]
        print(f"Failed to fetch data: {summary}")
        insert_log_audit(engine, audit_sid, f"Fetch {activity_type} Data", "Extract", "fetch_learning_attempt_last_90_days.py", summary, "FAIL")
        raise  # Re-raise the exception after logging

    return df


# ------------------------------------------------------- FUNCTIONS FOR EACH ENDPOINT
# User Course Activity
# --------------------

def fetch_user_course_activity():
    return fetch_data_from_udemy_api(
        base_url_user_course_activity,
        headers,
        logger,
        "User Course Activity"
    )
# --------------------
# User Activity
# --------------------

def fetch_user_activity():
    return fetch_data_from_udemy_api(
        base_url_user_activity,
        headers,
        logger,
        "User Activity"
    )

# --------------------
# Learning Activity Attempt Summary (with last 90 days)
# --------------------

def fetch_learning_activity_attempt_summary(days=90):
    return fetch_learning_attempt_last_90_days(
        base_url_learning_activity_attempt,
        headers,
        logger,
        "Learning Activity Attempt Summary",
        days
    )

# --------------------
# User Assessment Activity
# --------------------

def fetch_user_assessment_activity():
    return fetch_data_from_udemy_api(
        base_url_user_assessment_activity,
        headers,
        logger,
        "User Assessment Activity"
    )

# --------------------
# User Path Activity
# --------------------
def fetch_user_path_activity():
    return fetch_data_from_udemy_api(
        base_url_user_path_activity,
        headers,
        logger,
        "User Path Activity"
    )
# --------------------
# User Lab Activity
# --------------------
def fetch_user_lab_activity():
    return fetch_data_from_udemy_api(
        base_url_user_lab_activity,
        headers,
        logger,
        "User Lab Activity"
    )



def fetch_udemy_tables(engine):
    print("Getting Audit SID")
    audit_sid = get_audit_sid(engine)
    print("Fetching User Course Activity data..\n.")
    user_course_activity = pd.DataFrame(fetch_data_from_udemy_api(base_url_user_course_activity, headers, logger, "User Course Activity", engine, audit_sid))
    print("User Course Activity data fetched. Number of records:", len(user_course_activity), "\n")

    print("Fetching User Activity data...")
    user_activity = pd.DataFrame(fetch_data_from_udemy_api(base_url_user_activity, headers, logger, "User Activity", engine, audit_sid))
    print("User Activity data fetched. Number of records:", len(user_activity), "\n")

    print("Fetching Learning Activity Attempt Summary data...")
    learning_activity_attempt_summary = pd.DataFrame(fetch_learning_attempt_last_90_days(base_url_learning_activity_attempt, headers, logger, "Learning Activity Attempt Summary", engine, audit_sid))
    print("Learning Activity Attempt Summary data fetched. Number of records:", len(learning_activity_attempt_summary), "\n")

    print("Fetching User Assessment Activity data...")
    user_assessment_activity = pd.DataFrame(fetch_data_from_udemy_api(base_url_user_assessment_activity, headers, logger, "User Assessment Activity", engine, audit_sid))
    print("User Assessment Activity data fetched. Number of records:", len(user_assessment_activity), "\n")

    print("Fetching User Path Activity data...")
    user_path_activity = pd.DataFrame(fetch_data_from_udemy_api(base_url_user_path_activity, headers, logger, "User Path Activity", engine, audit_sid))
    print("User Path Activity data fetched. Number of records:", len(user_path_activity)), "\n"

    print("Fetching User Lab Activity data...")
    user_lab_activity = pd.DataFrame(fetch_data_from_udemy_api(base_url_user_lab_activity, headers, logger, "User Lab Activity", engine, audit_sid))
    print("User Lab Activity data fetched. Number of records:", len(user_lab_activity), "\n")

    print("All data successfully fetched and transformed into DataFrames.")
    return user_course_activity, user_activity, learning_activity_attempt_summary, user_assessment_activity, user_path_activity, user_lab_activity