CREATE TABLE plan_names (
   plan_no INTEGER PRIMARY KEY,
   plan_name TEXT
);

CREATE TABLE training_plans (
   plan_no INTEGER REFERENCES plan_names(plan_no),
   run_id INTEGER PRIMARY KEY,
   week_no INTEGER,
   day_no INTEGER,
   description_string TEXT
);

