import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Panel = () => {
    const [devices, setDevices] = useState([]);

    useEffect(() => {
        const fetchDevices = async () => {
            try {
                const response = await axios.get('/get_devices', {
                    headers: {
                        'Authorization': `Bearer ${document.cookie.replace('access_token=', '')}`
                    }
                });
                setDevices(response.data);
            } catch (error) {
                console.error('Error fetching devices', error);
            }
        };

        fetchDevices();
    }, []);

    const handleModeChange = async (deviceLabel, modeLabel) => {
        try {
            await axios.post('/set_device', {
                device_label: deviceLabel,
                mode_label: modeLabel
            }, {
                headers: {
                    'Authorization': `Bearer ${document.cookie.replace('access_token=', '')}`
                }
            });
            alert('Mode changed successfully');
        } catch (error) {
            alert('Failed to change mode');
        }
    };

    return (
        <div>
            <h2>Device Control Panel</h2>
            <table>
                <thead>
                    <tr>
                        <th>Device</th>
                        <th>Current Mode</th>
                        {devices.length > 0 && devices[0].modes.map((mode, index) => (
                            <th key={index}>{mode.name}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {devices.map((device) => (
                        <tr key={device.label}>
                            <td>{device.name}</td>
                            <td>{device.status}</td>
                            {device.modes.map((mode) => (
                                <td key={mode.label}>
                                    <button
                                        onClick={() => handleModeChange(device.label, mode.label)}
                                    >
                                        {mode.name}
                                    </button>
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Panel;
