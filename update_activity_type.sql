update activity_activity as t set activity_type = at.id
from activity_type at, ir_model_data md
where md.model = 'activity.type' and
at.id = md.db_id and
md.fs_id = direction || '_' || "type" || '_type' ;

update activity_activity as t set activity_type = at.id
from activity_type at, ir_model_data md
where md.model = 'activity.type' and
at.id = md.db_id and
md.fs_id = "type" || '_type' ;

update ir_sequence
set number_next_internal = (select max(code::integer)+1
from activity_activity) where code = 'activity.activity';

ALTER TABLE activity_activity alter column activity_type set not null;
