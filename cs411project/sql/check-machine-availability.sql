/*
 To test these queries, source heartbeat-insert-test.sql within the MySQL prompt
  and then source this file. You should compare the output of this file versus
  the expected results denoted in heartbeat-insert-test.sql. Note that the
  test uses CURRENT_TIMESTAMP and these queries also user CURRENT_TIMESTAMP,
  so it is important to run this query after inserting the test records because
  if you wait too long (4 min), then all machines will be returned as 
  AVAILABLE (since all heartbeats have timed out w.r.t. CURRENT_TIMESTAMP
  of a later time) 
*/



/* Check the availability of a single machine (7 for this example) */
/* Assuming for Machine.Status that 0 is BROKEN, 1 is ALIVE */
SELECT
  CASE WHEN Status = 0
        THEN 'Machine is BROKEN' 
       WHEN Status = 1 AND (
          /* If the last heartbeat for a machine occurred AFTER (Tfail amount of time BEFORE the current time), then the machine is still in use */
          SELECT SUBTIME(CURRENT_TIMESTAMP, Tfail) <= (CASE WHEN (LastTS IS NULL) THEN FirstTS ELSE LastTS END) AS StillInUse
          FROM HeartbeatSequence
          WHERE (LastTS = (SELECT CASE 
                              /* Find the last timestamp between the FirstTS and LastTS columns out of all HeartbeatSequence rows */
                              /* TODO: could be replaced with GREATEST() (MySQL, not in ANSI) */
                              WHEN MAX(LastTS) > MAX(FirstTS) THEN MAX(LastTS)
                              ELSE MAX(FirstTS) END
                              FROM HeartbeatSequence
                              WHERE MachineID = 7) OR
                FirstTS = (SELECT CASE 
                              WHEN MAX(LastTS) > MAX(FirstTS) THEN MAX(LastTS)
                              ELSE MAX(FirstTS) END
                              FROM HeartbeatSequence
                              WHERE MachineID = 7))
                AND MachineID = 7
       ) 
        THEN 'Machine is ALIVE, IN-USE'
       ELSE
        'Machine is AVAILABLE'
  END AS MachineAvailability
FROM Machine WHERE MachineID = 7;

/* Bulk version (get availability if all machines at once */
SELECT
  M.MachineID,
  CASE WHEN M.Status = 0
        THEN 'BROKEN' 
       WHEN M.Status = 1 AND tmp2.StillInUse = 1 
        THEN 'IN-USE'
       ELSE
        'AVAILABLE'
  END AS MachineAvailability
FROM Machine M
LEFT JOIN (SELECT HS.MachineID, SUBTIME(CURRENT_TIMESTAMP, HS.Tfail) <= tmp.LatestHeartbeatTS AS StillInUse
      FROM
        (SELECT MachineID,
             CASE WHEN MAX(LastTS) > MAX(FirstTS) THEN MAX(LastTS) ELSE MAX(FirstTS) END AS LatestHeartbeatTS
         FROM HeartbeatSequence
        GROUP BY MachineID) tmp
      JOIN HeartbeatSequence HS
        ON (tmp.LatestHeartbeatTS = HS.FirstTS OR tmp.LatestHeartbeatTS = HS.LastTS) AND tmp.MachineID = HS.MachineID) tmp2
ON M.MachineID = tmp2.MachineID;


/* Can we use non-standard sequel in our stuff? MAX(MAX(LastTS), MAX(FirstTS)) ??? Piazza asked */
/* https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_greatest */

/* Return 1 if the we received the last heartbeat at sometime before Tfail time before the current time, as return 0 */
/*
SELECT SUBTIME(CURRENT_TIMESTAMP, Tfail) <= (CASE WHEN (LastTS IS NULL) THEN FirstTS ELSE LastTS END) AS ActiveHeartBeat
FROM HeartbeatSequence
WHERE (LastTS = (SELECT CASE 
                    WHEN MAX(LastTS) > MAX(FirstTS) THEN MAX(LastTS)
                    ELSE MAX(FirstTS) END
                    FROM HeartbeatSequence
                    WHERE MachineID = 6) OR
      FirstTS = (SELECT CASE 
                    WHEN MAX(LastTS) > MAX(FirstTS) THEN MAX(LastTS)
                    ELSE MAX(FirstTS) END
                    FROM HeartbeatSequence
                    WHERE MachineID = 6))
      AND MachineID = 6;
*/
