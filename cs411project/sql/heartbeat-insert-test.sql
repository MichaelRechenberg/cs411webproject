/* Wipe the slate clean */
DELETE FROM HeartbeatSequence;
DELETE FROM Users;
DELETE FROM Machine;

INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('testNetId', TRUE, 'TestFirst', 'TestLast');

/* 
  Status of 0 -> BROKEN
  Status of 1 -> ALIVE
*/
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (1, NULL, 0);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (2, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (3, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (4, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (5, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (6, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (7, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (8, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (9, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (10, NULL, 1);

/* Check that current heartbeat sequences are detected correctly */
/* TFail is 5 minutes for all heartbeat sequences */

/* Machine Alive, but not available b/c the last received heartbeat (which happened to be the first one ever) was 3 minutes ago */
INSERT INTO HeartbeatSequence(SeqID, Tfail, NumHeartBeats, NetID, MachineID, FirstTS, LastTS) VALUES
          (1, '00:05:00', 1, 'testNetId', 2, SUBTIME(CURRENT_TIMESTAMP, '00:03:00'), NULL);
/* Machine Available (we recieved more than one heartbeat and the last heartbeat was more than Tfail minutes ago */
INSERT INTO HeartbeatSequence(SeqID, Tfail, NumHeartBeats, NetID, MachineID, FirstTS, LastTS) VALUES 
          (2, '00:05:00', 7, 'testNetId', 3, SUBTIME(CURRENT_TIMESTAMP, '00:10:00'), SUBTIME(CURRENT_TIMESTAMP, '00:07:00'));
/* Machine Available (only one heartbeat was ever sent and it was more than Tfail minutes ago */
INSERT INTO HeartbeatSequence(SeqID, Tfail, NumHeartBeats, NetID, MachineID, FirstTS, LastTS) VALUES 
          (3, '00:05:00', 1, 'testNetId', 4, SUBTIME(CURRENT_TIMESTAMP, '00:10:00'), NULL);
/* Machine Alive, but not available */
INSERT INTO HeartbeatSequence(SeqID, Tfail, NumHeartBeats, NetID, MachineID, FirstTS, LastTS) VALUES 
          (4, '00:05:00', 7, 'testNetId', 5, SUBTIME(CURRENT_TIMESTAMP, '00:10:00'), SUBTIME(CURRENT_TIMESTAMP, '00:03:00'));

/* Duplicate Heartbeat sequences for a machine...use the latest heartbeat sequence to judge availablility
  Machine 6 is available b/c the last hearbeat sequence for machine 6 (last insert) has the last heartbeat more than Tfail minutes ago */
INSERT INTO HeartbeatSequence(SeqID, Tfail, NumHeartBeats, NetID, MachineID, FirstTS, LastTS) VALUES 
          (5, '00:05:00', 7, 'testNetId', 6, SUBTIME(CURRENT_TIMESTAMP, '00:40:00'), SUBTIME(CURRENT_TIMESTAMP, '00:29:00'));
INSERT INTO HeartbeatSequence(SeqID, Tfail, NumHeartBeats, NetID, MachineID, FirstTS, LastTS) VALUES 
          (6, '00:05:00', 1, 'testNetId', 6, SUBTIME(CURRENT_TIMESTAMP, '00:20:00'), NULL);
INSERT INTO HeartbeatSequence(SeqID, Tfail, NumHeartBeats, NetID, MachineID, FirstTS, LastTS) VALUES 
          (7, '00:05:00', 1, 'testNetId', 6, SUBTIME(CURRENT_TIMESTAMP, '00:10:00'), SUBTIME(CURRENT_TIMESTAMP, '00:09:00'));

/* Test adding a heartbeat to a valid heartbeat sequence (Machine 7 should be alive, but not available after heartbeat update) */
INSERT INTO HeartbeatSequence(SeqID, Tfail, NumHeartBeats, NetID, MachineID, FirstTS, LastTS) VALUES 
          (8, '00:05:00', 1, 'testNetId', 7, SUBTIME(CURRENT_TIMESTAMP, '00:10:00'), SUBTIME(CURRENT_TIMESTAMP, '00:09:00'));
UPDATE HeartbeatSequence SET NumHeartBeats = NumHeartBeats + 1 WHERE MachineID = 7;





/* TODO: Check that inserting a new heartbeat leads to a machine going from ALIVE to IN-USE */
