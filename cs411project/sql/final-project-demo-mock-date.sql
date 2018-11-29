/* Wipe the slate clean */
DELETE FROM HeartbeatSequence;
DELETE FROM Comments;
DELETE FROM Machine;
DELETE FROM Users;
DELETE FROM Hardware;

/* 10 Machines and Heartbeat sequence inserts
   Only the first 7 machines will have a HeartbeatSequence row */
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


INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (1,1,1);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (2,3,1);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (3,1,2);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (4,3,2);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (5,1,3);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (6,3,3);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (7,1,4);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (8,3,4);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (9,1,5);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (10,3,5);


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



/* Mock users */
/* All 4 of devs are students, 1 TA named Dan w/ netId dmace2 */
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('rchnbrg2', 0, 'Michael', 'Rechenberg');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('aburket2', 0, 'Adam', 'Burkett');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('hop2', 0, 'Tianyu', 'Liang');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('tvargh4', 0, 'Thomas', 'Varghese');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('dmace2', 1, 'Dan', 'Mace');


/* Mock Hardware */
/* TODO: map somewhere what each Hardware.TYPE value means (0 -> headset) etc. */
INSERT INTO Hardware(HardwareID, Type) VALUES (1, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (2, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (3, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (4, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (5, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (6, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (7, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (8, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (9, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (10, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (11, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (12, 1);


/* Mock Comments */
/*
  Machine 1 has 2 unresolved comments
  Machine 2 has 1 resolved comment and 1 unresolved comment
  Machine 3 has 2 resolved comments

  Every other machine (except for machine 7) has 1 resolved comment
*/
/* TODO: Change Category to an FK to DownageCategory after midterm demo */
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Software Problem', 'Lighting engine is giving stack overflow error for MP2', 0, NULL, 'rchnbrg2', 1);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'Lens is dirty', 0, 1, 'rchnbrg2', 1);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'The strap is broken', 0, NULL, 'aburket2', 1);

INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Machine Problem', 'Missing a driver for nvidia', 1, NULL, 'aburket2', 2);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'Left analog stick of controller is stuck', 0, 2, 'hop2', 2);

INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Software Problem', 'Unity crashes after opening up MP4', 1, NULL, 'hop2', 3);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'The B button is stuck', 1, NULL, 'rchnbrg2', 3);

INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Machine Problem', 'Missing HDMI cable', 1, NULL, 'hop2', 4);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'Could not calibrate headset', 1, NULL, 'hop2', 5);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'Difficulty calibrating headset', 1, NULL, 'hop2', 6);

INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Machine Problem', 'Dead pixels on the right monitor', 1, NULL, 'hop2', 8);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Software Problem', 'Cannot load unity package due to missing drivers', 1, NULL, 'hop2', 9);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Software Problem', 'License for Oculus expired', 1, NULL, 'hop2', 10);
