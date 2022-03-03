SELECT P.project_id, P.project_name, P.project_progress_cd, P.project_end_cd, P.total_src_cnt_pointer, P.open_src_cnt_pointer, P.ready_to_open_src_cnt_pointer, T.data_cnt FROM 
CW_PROJECT P, TB_PRJ_MST T
WHERE P.project_id IN (11881, 11880, 11876, 11872) AND P.project_id = T.project_id;

project_id	project_name	project_progress_cd	project_end_cd	total_src_cnt_pointer	open_src_cnt_pointer	ready_to_open_src_cnt_pointer	data_cnt
11872	일반 면도기 이미지 수집 - 생활용품 10종 촬영하기	ENDED	COMPLETE	30	30	30	30
11876	손톱깎이 이미지 수집 - 생활용품 10종 촬영하기	ENDED	COMPLETE	60	60	60	60
11880	렌치 이미지 수집 - 생활용품 10종 촬영하기	ENDED	COMPLETE	40	40	40	40
11881	아령 이미지 수집 - 생활용품 10종 촬영하기	ENDED	COMPLETE	40	40	40	40

SELECT project_id, project_progress, total_source_count, opened_source_count, ready_to_open_source_count FROM co_project_setup
WHERE project_id IN (11881, 11880, 11876, 11872);

project_id	project_progress	total_source_count	opened_source_count	ready_to_open_source_count
11872	ENDED	30	30	30
11876	ENDED	60	60	60
11880	ENDED	40	40	40
11881	ENDED	40	40	40


UPDATE CW_PROJECT P, TB_PRJ_MST T
SET P.project_progress_cd = 'HOLDING', P.project_end_cd = NULL
WHERE P.project_id IN (11881, 11880, 11876, 11872) AND P.project_id = T.project_id;

UPDATE co_project_setup
SET project_progress = 'HOLDING'
WHERE project_id IN (11881, 11880, 11876, 11872);




SELECT T.project_id AS '프로젝트ID', M.member_nm AS '성명', CONCAT(SUBSTR(M.birthday, 1, 4),'-',SUBSTR(M.birthday, 5, 2),'-',SUBSTR(M.birthday, 7, 2)) AS '생년월일', IF(M.gender_cd = 'M', '남', '여') AS '성별', SUM(H.point) AS '급여' FROM TB_POINT_HISTORY H, TB_MEMBER M, TB_PRJ_MST T WHERE 
T.project_id IN (8505,8509,9042,9043,9258,9260,9261,9271)
AND H.prj_idx = T.prj_idx AND H.member_id = M.member_id
AND H.point_type_cd='POINT_SAVE' AND H.point_state_cd='COMPLETE'
GROUP BY T.project_id, M.member_id HAVING SUM(H.point) > 0
ORDER BY T.project_id, M.member_id;


SELECT T.project_id AS '프로젝트ID', M.member_nm AS '성명', CONCAT(SUBSTR(M.birthday, 1, 4),'-',SUBSTR(M.birthday, 5, 2),'-',SUBSTR(M.birthday, 7, 2)) AS '생년월일', IF(M.gender_cd = 'M', '남', '여') AS '성별', SUM(H.point) AS '급여' FROM TB_POINT_HISTORY H, TB_MEMBER M, TB_PRJ_MST T WHERE 
T.project_id IN (8341,10199,10619)
AND H.prj_idx = T.prj_idx AND H.member_id = M.member_id
AND H.point_type_cd='POINT_SAVE' AND H.point_state_cd='COMPLETE'
GROUP BY T.project_id, M.member_id HAVING SUM(H.point) > 0
ORDER BY T.project_id, M.member_id;


SELECT T.project_id AS '프로젝트ID', M.member_nm AS '성명', CONCAT(SUBSTR(M.birthday, 1, 4),'-',SUBSTR(M.birthday, 5, 2),'-',SUBSTR(M.birthday, 7, 2)) AS '생년월일', IF(M.gender_cd = 'M', '남', '여') AS '성별', SUM(H.point) AS '급여' FROM TB_POINT_HISTORY H, TB_MEMBER M, TB_PRJ_MST T WHERE 
T.project_id IN (9702,9706)
AND H.prj_idx = T.prj_idx AND H.member_id = M.member_id
AND H.point_type_cd='POINT_SAVE' AND H.point_state_cd='COMPLETE'
GROUP BY H.project_id, M.member_id HAVING SUM(H.point) > 0
ORDER BY T.project_id, M.member_id


SELECT A.login_id, A.cnt AS '작업량', A.d AS '확인일', B.cnt  AS '작업량', B.d AS '확인일'
FROM
(SELECT M.login_id, count(1) AS cnt, '2021-10-30' AS d FROM TB_MEMBER M, TB_PRJ_DATA D WHERE 
M.login_id IN ('hyosong@uw.edu','blair.m.lucas@gmail.com','chrischoi0225@gmail.com','markmoonnn@gmail.com','katiec1054@gmail.com','yebinkim2005@gmail.com','Enjungsong@gmail.com','anjelly.choi@gmail.com','thorikerecruiting2022@gmail.com','dragondavid123dk@gmail.com','hheyvivienne@gmail.com')
AND D.project_id = 8793
AND D.work_user = M.member_id
AND D.work_edate < '2021-10-31 00:00:00'
GROUP BY M.login_id) A
JOIN 
(SELECT M.login_id, count(1) AS cnt, '2021-11-02' AS d FROM TB_MEMBER M, TB_PRJ_DATA D WHERE 
M.login_id IN ('hyosong@uw.edu','blair.m.lucas@gmail.com','chrischoi0225@gmail.com','markmoonnn@gmail.com','katiec1054@gmail.com','yebinkim2005@gmail.com','Enjungsong@gmail.com','anjelly.choi@gmail.com','thorikerecruiting2022@gmail.com','dragondavid123dk@gmail.com','hheyvivienne@gmail.com')
AND D.project_id = 8793
AND D.work_user = M.member_id
AND D.work_edate < '2021-11-03 00:00:00'
GROUP BY M.login_id) B ON A.login_id = B.login_id


SELECT T.project_id AS '프로젝트ID', M.member_nm AS '성명', CONCAT(SUBSTR(M.birthday, 1, 4),'-',SUBSTR(M.birthday, 5, 2),'-',SUBSTR(M.birthday, 7, 2)) AS '생년월일', IF(M.gender_cd = 'M', '남', '여') AS '성별', SUM(H.point) AS '급여' FROM TB_POINT_HISTORY H, TB_MEMBER M, TB_PRJ_MST T WHERE 
T.project_id IN (9277,9436,9929)
AND (H.prj_idx = T.prj_idx OR H.project_id = T.project_id) AND H.member_id = M.member_id
AND H.point_type_cd='POINT_SAVE' AND H.point_state_cd='COMPLETE'
GROUP BY T.project_id, M.member_id HAVING SUM(H.point) > 0
ORDER BY T.project_id, M.member_id
