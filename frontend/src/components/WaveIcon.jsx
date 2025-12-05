import React from 'react';

/**
 * Wavelength/Radio Wave Icon Component
 * SVG icon representing radio waves/wavelengths
 */
const WaveIcon = ({ size = 18, color = '#00ffcc' }) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Radio wave circles */}
      <circle cx="12" cy="12" r="2" fill={color} />
      <circle cx="12" cy="12" r="5" stroke={color} strokeWidth="1.5" fill="none" opacity="0.7" />
      <circle cx="12" cy="12" r="8" stroke={color} strokeWidth="1.5" fill="none" opacity="0.5" />
      <circle cx="12" cy="12" r="11" stroke={color} strokeWidth="1.5" fill="none" opacity="0.3" />
      
      {/* Wave lines */}
      <path
        d="M 2 12 L 6 12 M 18 12 L 22 12"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
      />
      <path
        d="M 2 12 Q 3 10 4 12 T 6 12"
        stroke={color}
        strokeWidth="1.5"
        fill="none"
        opacity="0.8"
      />
      <path
        d="M 18 12 Q 19 10 20 12 T 22 12"
        stroke={color}
        strokeWidth="1.5"
        fill="none"
        opacity="0.8"
      />
    </svg>
  );
};

export default WaveIcon;



