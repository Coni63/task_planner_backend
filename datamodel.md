```
Table Team {
  id integer [primary key]
  name varchar
}

Table User {
  id integer [primary key]
  username varchar
  role varchar
  created_at timestamp
}

Table Category {
  id integer [primary key]
  title varchar
  junior_factor float
  senior_factor float
}

Table TeamAssignment {
  id integer [primary key]
  user_id integer
  team_id integer
  is_admin bool
  is_member bool
}

Table UserAssignment {
  id integer [primary key]
  category_id integer
  user_id integer
  level varchar
}

Table Project {
  id integer [primary key]
  name varchar
  team_id number
}

Table Task {
  id integer [primary key]
  title varchar
  description varchar
  status varchar
  project_id number
  assigned_user_id number
  picked_at timestamp
  estimated_duration number
  elapsed number
  expected_finalization timestamp
  estimated_finalization timestamp
  category_id number
}

Table TaskAudit {
  id integer [primary key]
  task_id number
  modified_at timestamp
  assigned_user_id number
  status string
}

Table TaskDependancies {
  id integer [primary key]
  task_id number
  after_task_id number
}


Ref: Team.id < TeamAssignment.team_id
Ref: User.id < TeamAssignment.user_id
Ref: User.id < UserAssignment.user_id
Ref: Category.id < UserAssignment.category_id
Ref: Team.id < Project.team_id
Ref: Project.id < Task.project_id
Ref: Task.assigned_user_id < User.id
Ref: Task.category_id < Category.id
Ref: TaskDependancies.task_id > Task.id
Ref: TaskDependancies.after_task_id > Task.id
```
