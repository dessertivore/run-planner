import psycopg
from celery import Celery
from datetime import datetime, timedelta

app = Celery("tasks", broker="pyamqp://guest@localhost//")


con = psycopg.connect(
    dbname="planner",
    user="myuser",
    password="password",
    host="db",
    port="5432",
)


def db_connection_check():
    if str(con.info.status) == "ConnStatus.OK":
        return True
    else:
        return False


def add_plan(plan_num: int, plan_name: str):
    cursor = con.cursor()
    cursor.execute(
        """INSERT INTO planner.public.plan_names (plan_no, plan_name) 
                VALUES (%s, %s);""",
        (plan_num, plan_name),
    )
    cursor.close()
    con.commit()


def add_run(plan_num: int, week: int, day: int, details: str):
    cursor = con.cursor()
    run_id = cursor.execute(
        """SELECT MAX(run_id) AS highest_run_id
        FROM planner.public.training_plans;"""
    ).fetchone()
    if run_id == (None,):
        run_id = 1
    else:
        run_id = run_id[0] + 1
    cursor.execute(
        """INSERT INTO planner.public.training_plans 
                VALUES (%s, %s, %s, %s, %s);""",
        (
            plan_num,
            run_id,
            week,
            day,
            details,
        ),
    )
    cursor.close()
    con.commit()


def find_run_func(plan_num: int, week: int, day: int):
    cursor = con.cursor()
    found_run = cursor.execute(
        """SELECT description_string FROM planner.public.training_plans WHERE
            plan_no = %s
            AND week_no = %s 
            AND day_no = %s;""",
        (
            plan_num,
            week,
            day,
        ),
    ).fetchall()
    cursor.close()
    con.commit()
    return found_run


def find_plan_func(search_plan: int | str) -> list:
    """
    Search for all plans which match search parameter in database.

    Args:
        search_plan (int | str): enter plan ID or plan name

    Returns:
        list | None: list of tuples containing matching run plans, or None.
    """
    cursor = con.cursor()
    if isinstance(search_plan, str):
        found_plans = cursor.execute(
            """SELECT plan_no FROM planner.public.plan_names WHERE
                plan_name = %s;""",
            (search_plan,),
        ).fetchall()
    elif isinstance(search_plan, int):
        found_plans = cursor.execute(
            """
            SELECT plan_name FROM planner.public.plan_names WHERE plan_no = %s
            """,
            (search_plan,),
        ).fetchall()
    cursor.close()
    return found_plans


@app.task
def reminder(description: str):
    print("Time to run! Today's run is " + description)


def set_run_reminder(plan_of_choice: int) -> None:
    """
    Create run reminders once running plan has been chosen.

    Args:
        plan_of_choice (int): chosen plan. Generates run reminders for all runs
        in plan

    Requires improved reminders - currently just prints reminder to terminal. Need to
    create celery docker container, and link with API as well.
    """
    cursor = con.cursor()
    runs_in_plan = cursor.execute(
        """SELECT run_id, week_no, day_no, description_string FROM planner.public.training_plans WHERE
            plan_no = %s;""",
        (plan_of_choice,),
    ).fetchall()
    cursor.close()
    print(runs_in_plan)
    for run in runs_in_plan:
        weeks = run[1]
        days = run[2]
        description = run[3]
        days_from_now = weeks * 7 + days
        send_time = datetime.now() + timedelta(seconds=days_from_now)
        reminder.apply_async(args=[description], eta=send_time)
