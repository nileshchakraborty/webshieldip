CREATE CONSTRAINT session_id IF NOT EXISTS FOR (s:Session) REQUIRE s.id IS UNIQUE;
CREATE INDEX device_id_idx IF NOT EXISTS FOR (s:Session) ON (s.deviceId);
