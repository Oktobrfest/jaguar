import React from "react";
import { CaptureForm } from './CaptureForm';
import { CropFest } from './CropFest';

function AiPage() {
    return (
        <div>
            <div className="cropfest-container">
                <CropFest/>
            </div>
            <div className="capture-form-container">
                <CaptureForm/>
            </div>
        </div>
    );
}

export { AiPage };
