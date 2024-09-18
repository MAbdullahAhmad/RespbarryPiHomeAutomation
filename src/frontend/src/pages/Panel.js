import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { make_url } from '../config';

// Function to get the cookie value by name
const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;  // Return null if the token is not found
};

const Panel = () => {
    const [devices, setDevices] = useState([]);

    useEffect(() => {
        const fetchDevices = async () => {
            try {
                const accessToken = getCookie('access_token');
                console.log("token",accessToken) // Extract the access token from cookie
                if (!accessToken) {
                    throw new Error('No access token found. Please log in again.');
                }

                const response = await axios.get(make_url('/get_devices'), {
                    headers: {
                        'Authorization': `Bearer ${accessToken}`
                    }
                });
                setDevices(response.data);
            } catch (error) {
                console.error('Error fetching devices:', error);
                if (error.message.includes('No access token')) {
                    alert('Authentication error. Please log in again.');
                    // Optionally, redirect the user to the login page
                    // window.location.href = '/login';
                }
            }
        };

        fetchDevices();
    }, []);

    const handleModeChange = async (deviceLabel, modeLabel) => {
        try {
            const accessToken = getCookie('access_token'); // Extract the access token for each request
            if (!accessToken) {
                throw new Error('No access token found. Please log in again.');
            }

            await axios.post(make_url('/set_device'), {
                device_label: deviceLabel,
                mode_label: modeLabel
            }, {
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            });
            alert('Mode changed successfully');
        } catch (error) {
            alert('Failed to change mode');
            console.error('Error changing mode:', error);
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
