# Intelligence_Task_Manager

## System Description

The system manage missions and agents information.

## Files and folders structure

```bash

intelligence-task-manager/
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── utils/
│   ├── exceptions.py
│   └── models.py
├── routes/
│    ├── agent_routes.py
│    ├── mission_routes.py
│    └── report_routes.py
├── logs/
│   └── app.log
├── README.md
├── requirements.txt
└── .gitignore


```

## Tables structure

### missions

| name              | type                                                                                 | description                                                                                    |
| ----------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| id                | INT                                                                                  | auto_increment, PK                                                                             |
| title             | VARCHAR(30) NOT NULL                                                                 | mission title                                                                                  |
| description       | TEXT NOT NULL                                                                        | mission description                                                                            |
| location          | VARCHAR(30) NOT NULL                                                                 | mission location                                                                               |
| difficulty        | INT NOT NULL                                                                         | 1-10                                                                                           |
| importance        | INT  NOT NULL                                                                       | 1-10                                                                                           |
| status            | ENUM(NEW, ASSINGED, IN_PROGRESS,<br />COMPLETE, FAILED, CANCELLED),<br />DEFAULT NEW |                                                                                                |
| risk_level        | ENUM(LOW, MEDIUM, HIGH, CRITICAL)                                                    | not from user,<br />auto calculation,<br />**difficulty \* 2 + importance = risk_level** |
| assigned_agent_id | INT DEFAULT NULL                                                                     |                                                                                                |

### agents

| name               | type                            | description                  |
| ------------------ | ------------------------------- | ---------------------------- |
| id                 | INT                             | auto_increment, PK           |
| name               | VARCHAR(50) NOT NULL            | agent name                   |
| specialty          | VARCHAR(50) NOT NULL            | specialty area               |
| is_active          | BOOLEAN DEFAULT TRUE            |                              |
| completed_missions | INT DEFAULT 0                   | amount of completed missions |
| failed_missions    | INT DEFAULT 0                   | amount of failed missions    |
| agent_rank         | ENUM(Junior, Senior, Commander) |                              |

## Class and Methods explanation

### Class DBConnection

responsible on the DB area.

**Method get_connection().**
return active connection to the MySql database.

**Method create_database().**
creating Intelligence_db database if not exist.

**Method create_tables().**
creating agents and missions tables if they not exist.

### Class AgentDB

responsible on full CRUD in the agents table.

**Method create_agent(data).**
get agent data and create new agent in the table.

**Method get_all_agents().**
return all agents in the table.

**Method get_agent_by_id(id).**
get agent ID and return the agent data.

**Method update_agent(id, data).**
get agent ID and the update data and update the agent in thr table.

**Method deactivate_agent(id).**
define agent is_active status to FALSE.

**Method increment_completed(id).**
get agent ID and update the amount of completed mission to the completed_missions cell.

**Method increment_failed(id).**
get agent ID and update the amount of failed mission to the failed_missions cell.

**Method get_agent_performance(id).**
get ID agent and return dictionary,
total = total missions,
failed = amount of failed missions,
completed = amount of completed missions,
success_rate = calculate how much in % completed.

**Method count_active_agents().**
return amount of active agents.

### Class MissionDB

responsible on full CRUD in the missions table.

**Method create_mission(data).**
get mission data and creating it the table new mission.

**Method get_all_missions().**
show all missions in the table.

**Method get_mission_by_id(id).**
get mission ID and return the mission or None.

**Method assign_mission(m_id, a_id).**
get mission ID and agent ID and adding the mission to the agent.

**Method update_mission_status(id, status).**
get mission ID and mission status and update the mission status.

**Method get_open_missions_by_agent(id).**
get agent ID and return all missions with status ASSIGNED/IN_PROGRESS.

**Method count_all_missions().**
return the amount off all missions.

**Method count_by_status(status).**
get mission status and return the amount.

**Method count_open_missions().**
return count of open missions.

**Method count_critical_missions().**
return count of CRITICAL missions.

**Method get_top_agent().**
return agent with the highest completed_missions.

## System Rules

- agent_rank must be Junior / Senior / Commander,else return ERROR.
- difficulty cell and importance cell must be between 1 - 10,else return ERROR.
- risk_level cell is auto calculate,the user don't sent it.
- agent with is_active=False, cannot get missions.
- agent cant assign more then 3 open mission (ASSIGNED / IN_PROGRESS).
- if mission is in risk_level=CRITICAL, only commander agent can get the mission.
- mission can be assign only if the status is NEW, and after the assignment status=ASSIGNED.
- agent can start a mission only if the status=ASSIGNED, and after he started status=IN_PROGRESS.
- mission can be finish only if status=IN_PROGRESS, and after he finish change the status to failed / completed.
- mission can be cancelled only if the mission in status NEW \ ASSIGNED,
  else ERROR.

## Endpoints list

### Agents endpoints

| Method | Endpoint                 | Description           |
| ------ | ------------------------ | --------------------- |
| POST   | /agents                  | creating new agent    |
| GET    | /agents                  | get all agents        |
| GET    | /agents/{id}             | get agent by ID       |
| PUT    | /agents/{id}             | update agent info     |
| PUT    | /agents/{id}/deactivate  | deactivate agent      |
| GET    | /agents/{id}/performance | get agent performance |

### Missions endpoints

| Method | Endpoint                         | Description                 |
| ------ | -------------------------------- | --------------------------- |
| POST   | /missions                        | create new mission          |
| GET    | /missions                        | get all missions            |
| GET    | /missions/{id}                   | get mission by ID           |
| PUT    | /missions/{id}/assign/{agent_id} | assign mission to agent     |
| PUT    | /missions/{id}/start             | starting mission            |
| PUT    | /missions/{id}/complete          | finish mission as completed |
| PUT    | /missions/{id}/fail              | finish mission as failed    |
| PUT    | /missions/{id}/cancel            | cancelling mission          |

### Reports endpoints

| Method | Endpiont                    | Description               |
| ------ | --------------------------- | ------------------------- |
| GET    | /reports/summary            | summary report            |
| GET    | /reports/missions-by-status | report missions by status |
| GET    | /reports/top-agent          | the top agent             |

## System flow

- creating new agent.
- Show all agents or agent by ID.
- Updating agent info.
- Deactivate agent.
- Show agent performance.
- Creating new mission.
- Show all missions or mission by ID.
- Assign mission to agent.
- Updating missions status.
- Show general report of the system.
- Show report by status.
- Show the top agent.

## Running Instructions

1. create a docker container.

```bash
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
  -e MYSQL_DATABASE=Intelligence_db -p 3320:3306 mysql:latest

```

(I'm using PORT 3320 because i'm using LINUX UBUNTU and port 3306 already in use by UBUNTU.)

2. install packages.

```bash
pip install -r requirements.txt
```

3. Two options

- run in the terminal.

```bash
uvicorn main:app --reload
```

or

- run main.py
