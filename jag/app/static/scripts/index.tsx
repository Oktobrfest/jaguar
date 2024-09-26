import React from "react";
import { createRoot } from "react-dom/client";
import { AiPage } from './AiPage';
import { SettingsPage } from './SettingsPage';


document.addEventListener("DOMContentLoaded", function() {
    const aiContainer = document.getElementById('react-root-ai');
    if (aiContainer) {
        const rootHome = createRoot(aiContainer);
        rootHome.render(<AiPage />);
    }
    
    const settingsAppDiv = document.getElementById('settings-react-app');
    if (settingsAppDiv) {
        const rootSettings = createRoot(settingsAppDiv);
        rootSettings.render(<SettingsPage />);
    }


});
