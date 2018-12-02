/* Wipe the slate clean */
DELETE FROM HeartbeatSequence;
DELETE FROM Comments;
DELETE FROM Machine;
DELETE FROM Users;
DELETE FROM Hardware;
DELETE FROM MachineLocation;

/* 10 Machines and Heartbeat sequence inserts
   Only the first 7 machines will have a HeartbeatSequence row */
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('testNetId', TRUE, 'TestFirst', 'TestLast');

/*
  Status of 0 -> BROKEN
  Status of 1 -> ALIVE
*/
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (1, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (2, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (3, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (4, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (5, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (6, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (7, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (8, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (9, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (10, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (11, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (12, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (13, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (14, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (15, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (16, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (17, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (18, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (19, NULL, 1);
INSERT INTO Machine(MachineID, NetIDOfLastUsed, Status) VALUES (20, NULL, 1);


INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (1,1,1);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (2,2,1);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (3,3,1);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (4,4,1);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (5,5,1);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (6,1,3);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (7,2,3);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (8,3,3);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (9,4,3);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (10,5,3);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (11,1,4);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (12,2,4);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (13,3,4);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (14,4,4);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (15,5,4);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (16,1,6);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (17,2,6);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (18,3,6);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (19,4,6);
INSERT INTO MachineLocation(MachineID, X_COORDINATE, Y_COORDINATE) VALUES (20,5,6);


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
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('tvarghe2', 0, 'Thomas', 'Varghese');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('dmace2', 1, 'Dan', 'Mace');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('shaffer1', 1, 'Eric', 'Shaffer');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('tchen72', 1, 'Tianyu', 'Chen');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('sofiam2', 1, 'Sofia', 'Meyers');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('junsitu2', 1, 'Jason', 'Situ');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('stoehr2', 1, 'Benjamin', 'Stoehr');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('mkong8', 1, 'Matthew', 'Ong');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('hoezel2', 1, 'Jonathan', 'Hoelzel');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('tulshib2', 1, 'Shan', 'Tulshi');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('xma29', 1, 'Xiaoxin', 'Ma');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('santo3', 1, 'Craig', 'Santo');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('aadomel2', 1, 'Allegra', 'Domel');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('myren2', 1, 'Nathaniel', 'Myren');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('luyugao2', 1, 'Luyu', 'Gao');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('lnair2', 1, 'Lavania', 'Nair');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('parosa2', 1, 'Ada', 'Rosa');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('yshih8', 1, 'Jasmine', 'Shih');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('aipark2', 1, 'Andrew', 'Park');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('samuelm2', 1, 'Samuel', 'McFadden');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('yl6', 1, 'Yanchen', 'Lu');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('dbadri2', 0, 'Divya', 'Badri');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('dschoi3', 0, 'Daniel S', 'Choi');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('daiteng2', 0, 'Dai', 'Teng');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('simran5', 0, 'Saba', 'Imran');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('nagpaul2', 0, 'Divij', 'Nagpaul');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('vani', 0, 'Sushrut', 'Vani');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('anicab2', 0, 'Anica', 'Bhargava');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('lg6', 0, 'Lohitaksh', 'Gupta');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('sliu125', 0, 'Sicong', 'Liu');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('sluo24', 0, 'Sean', 'Luo');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('hding10', 0, 'Haoyang', 'Ding');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('ericdl2', 0, 'Eric', 'Lee');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('klfeng2', 0, 'Keven', 'Feng');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('justinr3', 0, 'Justin', 'Ruan');
INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ('ablkrsh3', 0, 'Ahilan', 'Balakrishnan');

INSERT INTO HeartbeatSequence(NetID, MachineID, NumHeartbeats, Tfail) VALUES ('dbadri2', 1, 0, '00:05:00');
INSERT INTO HeartbeatSequence(NetID, MachineID, NumHeartbeats, Tfail) VALUES ('dschoi3', 2, 0, '00:05:00');
INSERT INTO HeartbeatSequence(NetID, MachineID, NumHeartbeats, Tfail) VALUES ('daiteng2', 3, 0, '00:05:00');
INSERT INTO HeartbeatSequence(NetID, MachineID, NumHeartbeats, Tfail) VALUES ('simran5', 4, 0, '00:05:00');
INSERT INTO HeartbeatSequence(NetID, MachineID, NumHeartbeats, Tfail) VALUES ('nagpaul2', 5, 0, '00:05:00');
INSERT INTO HeartbeatSequence(NetID, MachineID, NumHeartbeats, Tfail) VALUES ('vani', 6, 0, '00:05:00');
INSERT INTO HeartbeatSequence(NetID, MachineID, NumHeartbeats, Tfail) VALUES ('anicab2', 7, 0, '00:05:00');
INSERT INTO HeartbeatSequence(NetID, MachineID, NumHeartbeats, Tfail) VALUES ('lg6', 8, 0, '00:05:00');
INSERT INTO HeartbeatSequence(NetID, MachineID, NumHeartbeats, Tfail) VALUES ('sliu125', 9, 0, '00:05:00');
INSERT INTO HeartbeatSequence(NetID, MachineID, NumHeartbeats, Tfail) VALUES ('sluo24', 10, 0, '00:05:00');
INSERT INTO HeartbeatSequence(NetID, MachineID, NumHeartbeats, Tfail) VALUES ('hding10', 11, 0, '00:05:00');
INSERT INTO HeartbeatSequence(NetID, MachineID, NumHeartbeats, Tfail) VALUES ('ericdl2', 12, 0, '00:05:00');
INSERT INTO HeartbeatSequence(NetID, MachineID, NumHeartbeats, Tfail) VALUES ('klfeng2', 13, 0, '00:05:00');
INSERT INTO HeartbeatSequence(NetID, MachineID, NumHeartbeats, Tfail) VALUES ('justinr3', 14, 0, '00:05:00');
INSERT INTO HeartbeatSequence(NetID, MachineID, NumHeartbeats, Tfail) VALUES ('adlkrsh3', 15, 0, '00:05:00');




/* Mock Hardware */
/* TODO: map somewhere what each Hardware.TYPE value means (0 -> headset) etc. */
INSERT INTO Hardware(HardwareID, Type) VALUES (1, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (2, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (3, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (4, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (5, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (6, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (7, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (8, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (9, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (10, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (11, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (12, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (13, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (14, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (15, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (16, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (17, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (18, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (19, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (20, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (21, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (22, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (23, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (24, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (25, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (26, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (27, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (28, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (29, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (30, 0);
INSERT INTO Hardware(HardwareID, Type) VALUES (31, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (32, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (33, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (34, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (35, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (36, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (37, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (38, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (39, 1);
INSERT INTO Hardware(HardwareID, Type) VALUES (40, 1);


INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Software Problem', 'Lighting engine is giving stack overflow error for MP2', 1, NULL, 'rchnbrg2', 1);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'Lens is dirty', 1, 1, 'rchnbrg2', 1);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'The strap is broken', 1, NULL, 'aburket2', 1);

INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Machine Problem', 'Missing a driver for nvidia', 1, NULL, 'aburket2', 2);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'Left analog stick of controller is stuck', 1, 2, 'hop2', 2);

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
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'Xbox controller is missing', 1, NULL, 'hop2', 15);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Software Problem', 'Unity version error', 1, NULL, 'rchnbrg2', 11);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'Headset has no sound', 1, 1, 'rchnbrg2', 11);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'Cannot boot PC', 1, NULL, 'aburket2', 12);

INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Machine Problem', 'Mice is not working', 1, NULL, 'aburket2', 20);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'Sensor is missing', 1, 2, 'hop2', 12);
  INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Software Problem', 'Cant open Visual studio', 1, NULL, 'rchnbrg2', 17);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'Headset doesnt display image but still output sounds', 1, 1, 'rchnbrg2', 19);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'The strap is broken', 1, NULL, 'aburket2', 1);

INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Machine Problem', 'Cannot login to my account with current NetID and password on this machine', 1, NULL, 'aburket2', 7);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'Controller usb cable missing', 1, 2, 'hop2', 17);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Software Problem', 'Cannot login Oculus store', 1, NULL, 'rchnbrg2', 15);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'Found an extra controller here...', 1, 1, 'rchnbrg2', 12);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'An additional sensor appeared on my desk...', 1, NULL, 'aburket2', 11);

INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Machine Problem', 'My favorite machine is being used by someone else', 1, NULL, 'aburket2', 12);
INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'Only has 1 touch controller', 1, 2, 'hop2', 13);
  INSERT INTO Comments(Category, CommentText, IsResolved, HardwareID, AuthorNetID, MachineID) VALUES
  ('Hardware Problem', 'Xbox controller is connected but not working', 1, NULL, 'aburket2', 1);