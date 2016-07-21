insert into apps_ui (type, `values`)
    values ('size','["num_jobs", "wage"]' );

insert into apps_ui (type, `values`)
    values ('y','["num_jobs", "wage"]' );

UPDATE apps_build_ui
SET ui_id = (select id from apps_ui where type = 'size' and `values` = '["num_jobs", "wage"]')
where apps_build_ui.build_id in (3,4) and apps_build_ui.ui_id = 7;

UPDATE apps_build_ui
SET ui_id = (select id from apps_ui where type = 'y' and `values` = '["num_jobs", "wage"]')
where apps_build_ui.build_id in (19,20) and apps_build_ui.ui_id = 63;
