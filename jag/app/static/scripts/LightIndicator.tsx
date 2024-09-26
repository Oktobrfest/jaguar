import React from 'react';

// Props type for TypeScript (optional)
type LightIndicatorProps = {
  status: boolean; // true for green, false for red
};

// Functional Component
const LightIndicator: React.FC<LightIndicatorProps> = ({ status }) => {
    <div className={ `light ${ status ? 'green' : 'red' }` }></div>
};

export default LightIndicator;
