
Prodigy Project for Human Evaluation of Review Response Generation for the Hospitality Domain.

### Starting the Prodigy Webapp

    `prodigy RECIPE DB_NAME DATAFILE -F PYTHON_SCRIPT`

    - e.g.

    `prodigy rrgen-human-eval rrgen_human_eval.de.tk.db rrgen_human_eval.de.jsonl -F recipe.py`

    **Note**, please replace `tk` in the database (DB_NAME) with your own initials or some other unique identifier for yourself.

### Annotation Instructions

For detailed annotation instructions, see the help guide (`?` icon in the top left of the prodigy web app).

### Exporting Database

Once you are finished with your annotations, export the database (DB_NAME) using the following command:

	`prodigy db-out DB_NAME OUTPUTFILE`

	- e.g.

    `prodigy db-out rrgen_human_eval.de.tk.db rrgen_human_eval.de.tk.jsonl`
    
