-- Insert users
INSERT INTO users (username, full_name, email, password)
VALUES 
('dilawar', 'Dilawar Jahangir', 'dilawar@example.com', 'dilawar'),
('arslaan', 'Arslaan Gondal', 'arslaan@example.com', 'arslaan'),
('syed', 'Syed Momin', 'syed@example.com', 'syed'),
('saliha', 'Saliha Jamil', 'saliha@example.com', 'saliha');

-- Insert devices
INSERT INTO devices (label, name, description)
VALUES
('bulb', 'Bulb', 'A smart bulb with multiple modes'),
('fan', 'Fan', 'A smart fan with motion sensor capability');

-- Insert device modes for Bulb
INSERT INTO device_mode_options (device_id, label, name, description)
VALUES
((SELECT id FROM devices WHERE label = 'bulb'), 'on', 'On', 'The bulb is on'),
((SELECT id FROM devices WHERE label = 'bulb'), 'off', 'Off', 'The bulb is off'),
((SELECT id FROM devices WHERE label = 'bulb'), 'motion', 'Motion', 'The bulb is on motion detection mode'),
((SELECT id FROM devices WHERE label = 'bulb'), 'ambient', 'Ambient', 'The bulb is in ambient mode');

-- Insert device modes for Fan
INSERT INTO device_mode_options (device_id, label, name, description)
VALUES
((SELECT id FROM devices WHERE label = 'fan'), 'on', 'On', 'The fan is on'),
((SELECT id FROM devices WHERE label = 'fan'), 'off', 'Off', 'The fan is off'),
((SELECT id FROM devices WHERE label = 'fan'), 'motion', 'Motion', 'The fan is in motion detection mode');
