

/* You can test this by replacing MachineID = k with whaterver id for k added in mike-heartbeat-insert.sql */
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
