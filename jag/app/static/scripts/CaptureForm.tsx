import React, { useState, useEffect, useRef } from 'react';
import LightIndicator from './LightIndicator';

function CaptureForm() {
    const [ rtmpUrl, setRtmpUrl ] = useState('rtmp://nginx-rtmp/live/test');
    const [ isCapturing, setIsCapturing ] = useState(false);
    const [ successfulCapture, setSuccessfulCapture ] = useState(null);

    const toggleCapture = async () => {
        try {
            const formData = new FormData();
            formData.append('rtmp_url', rtmpUrl);
            const response = await fetch('/toggle-capture', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
            if (response.ok) {
                // console.log('isCapturing: ' + data.isCapturing);
              //  setIsCapturing(data.isCapturing == true);
                // console.log('real isCapturing value is: ' + isCapturing)
                 setIsCapturing(c => (data.isCapturing == true));
            } else {
                console.log('data.message: ' + data.message + ' ; isCapturing: ' + data.isCapturing);
                alert('Failed to toggle capture: ' + error.message);
                throw new Error(data.message || 'Failed to toggle capture');
            }
        } catch (error) {
            alert('Failed to toggle capture: ' + error.message);
        }
    };

    useEffect(() => {
    console.log('Capturing status changed:', isCapturing);
}, [isCapturing]);


    const pollCaptureStatus = async () => {
        const response = await fetch('/capture-status');
        if (response.ok) {
            const data = await response.json();
            setIsCapturing( ()=> (data.isCapturing == true));
            setSuccessfulCapture( ()=> (data.successfulCapture == true))

            // setIsCapturing(data.isCapturing == true);
        } else {
            console.log('failed to capture');
            // alert('failed to capture');
        }
    };

    useInterval(pollCaptureStatus, 5000);

    return (
        <div>
            <div className="capture-form-container">
                <form className="form-inline">
                    <label htmlFor="rtmp_url" className="label">RTMP URL:</label>
                    <input
                        type="url"
                        id="rtmp_url"
                        name="rtmp_url"
                        required
                        placeholder="rtmp://nginx-rtmp/live/test"
                        value={ rtmpUrl }
                        onChange={ e => setRtmpUrl(e.target.value) }
                        className="input-field rtmp-url-form"
                    />
                    <button id='capture-button' type="button" onClick={ toggleCapture } className="button">
                        { isCapturing ? 'Stop Capture' : 'Start Capture' }
                    </button>
                    {successfulCapture !== null && <LightIndicator status={successfulCapture} />}
                </form>
            </div>
        </div>
    );

    function useInterval(callback, delay) {
        const savedCallback = useRef();

        useEffect(() => {
            savedCallback.current = callback;
        }, [ callback ]);

        useEffect(() => {
            function tick() {
                if (savedCallback.current) {
                    savedCallback.current();
                }
            }

            if (delay !== null) {
                const id = setInterval(tick, delay);
                return () => clearInterval(id);
            }
        }, [ delay ]);
    }


}

export { CaptureForm };
