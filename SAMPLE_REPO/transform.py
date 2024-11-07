from sqlalchemy.sql import text
from load import (
    insert_log_audit
)

# Stored procedure name defined outside the function
UDEMY_USER_ACTIVITY_PROC = 'STG.MERGE_UDEMY_STAGE_TO_MAIN'

def merge_udemy_user_activity(engine, audit_sid):
    """
    Calls the stored procedure to merge data from staging to main Udemy user activity table
    and logs the success or failure.
    """
    try:
        with engine.connect() as connection:
            # Execute the stored procedure using SQLAlchemy's text() function
            connection.execute(text(f"CALL {UDEMY_USER_ACTIVITY_PROC}()"))
        
        # Log success message
        success_message = "Merge of STG.udmy_user_activity to UDMY.user_activity completed successfully."
        print(success_message)
        insert_log_audit(engine, audit_sid, "Merge Udemy User Activity", "Transform", "merge_udemy_user_activity.py", success_message, "SUCCESS")
    
    except Exception as e:
        # Log failure with error summary
        error_message = str(e)
        summary = error_message.split('\n')[0][:95]
        print(f"Failed to execute merge procedure: {summary}")
        insert_log_audit(engine, audit_sid, "Merge Udemy User Activity", "Transform", "merge_udemy_user_activity.py", summary, "FAIL")
        raise  # Re-raise the exception after logging
