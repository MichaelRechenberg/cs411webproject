/* Wipe the slate clean */
DROP TABLE IF EXISTS HeartbeatSequence;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS Hardware;
DROP TABLE IF EXISTS Machine;
DROP TABLE IF EXISTS Users;


CREATE TABLE IF NOT EXISTS Users (
	      NetID VARCHAR(20) NOT NULL,
        isTA BOOLEAN NOT NULL,
        FirstName VARCHAR(50) NOT NULL,
        LastName VARCHAR(50) NOT NULL,
        PRIMARY KEY(NetID)
);

CREATE TABLE IF NOT EXISTS Hardware (
        HardwareID INT NOT NULL,
        Type INT NOT NULL,
        PRIMARY KEY(HardwareID)
);

CREATE TABLE IF NOT EXISTS Machine (
        MachineID INT NOT NULL,
        /* Can be NULL b/c it could be the case that no one has used
            this machine yet */  
        NetIDofLastUsed VARCHAR(20),
        /* 0 for BROKEN, 1 for ALIVE */
        Status INT NOT NULL,
        FOREIGN KEY(NetIDofLastUsed) REFERENCES Users(NetID),
        PRIMARY KEY(MachineID)
);

CREATE TABLE IF NOT EXISTS Comments (
        CommentID INT NOT NULL AUTO_INCREMENT,
        /* Any updates/creates update this timestamp */
        LastModifiedTS TIMESTAMP NOT NULL,
        /* TODO: (Mike) change this to a FK to a DownageCategory after Basic Demo*/
        Category VARCHAR(50) NOT NULL,
        /* The text comment made by the user */
        CommentText VARCHAR(400) NOT NULL,
        /* Flag indicating if this comment has been resolved. Once resolved,
            a Comment should not be made "unresolved" again */
        /* DEFAULT FALSE b/c when you first create a Comment, it isn't resolved yet */
        IsResolved BOOLEAN NOT NULL DEFAULT FALSE,
        /* Id for a piece of hardware associated with this comment (if any) */
        HardwareID INT,
        /* NetID of the student authoring this comment */
        AuthorNetID VARCHAR(20) NOT NULL,
        /* MachineID of the machine this comment is associated with */
        MachineID INT NOT NULL,
        FOREIGN KEY(MachineID) REFERENCES Machine(MachineID),
        FOREIGN KEY(AuthorNetID) REFERENCES Users(NetID),
        FOREIGN KEY(HardwareID) REFERENCES Hardware(HardwareID),
        PRIMARY KEY(CommentID)
);


CREATE TABLE IF NOT EXISTS HeartbeatSequence (
        SeqID INT NOT NULL AUTO_INCREMENT,
        FirstTS TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        LastTS TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
        Tfail TIME NOT NULL,
        /* The number of heartbeats received during this heartbeat sequence */
        /* UPDATE this column by one each time we get a heartbeat and LastTS will be updated to the current timestamp automatically */
        NumHeartBeats INT NOT NULL DEFAULT 0,
        NetID VARCHAR(20) NOT NULL,
        MachineID INT NOT NULL,
        FOREIGN KEY(NetID) REFERENCES Users(NetID),
        FOREIGN KEY(MachineID) REFERENCES Machine(MachineID),
        PRIMARY KEY(SeqID)
);

