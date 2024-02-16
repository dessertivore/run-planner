import psycopg

con = psycopg.connect(
    dbname="planner",
    user="myuser",
    password="password",
    host="localhost",
    port="5432",
)


def add_run(plan_num, week, day, details):
    cursor = con.cursor()
    cursor.execute(
        """INSERT INTO planner.public.training_plans 
                VALUES (%s, %s, %s, %s);""",
        (
            plan_num,
            week,
            day,
            details,
        ),
    )
    cursor.close()
    con.commit()


def add_plan(plan_num, plan_name):
    cursor = con.cursor()
    cursor.execute(
        """INSERT INTO planner.public.plan_names (plan_no, plan_name) 
                VALUES (%s, %s);""",
        (plan_num, plan_name),
    )
    cursor.close()
    con.commit()


def find_run_func(plan_num, week, day):
    cursor = con.cursor()
    found_run = cursor.execute(
        """SELECT description_string FROM planner.public.training_plans WHERE
            plan_no = %s,
            week_no = %s, 
            day_no = %s;""",
        (plan_num, week, day),
    )
    cursor.close()
    con.commit()
    return found_run
