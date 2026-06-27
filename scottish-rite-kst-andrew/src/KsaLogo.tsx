import React from 'react'

interface KsaLogoProps {
  size?: number
}

export const KsaLogo = ({ size = 80 }: KsaLogoProps) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 100 100"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label="Knights of St. Andrew Logo"
  >
    {/* Outer circle */}
    <circle cx="50" cy="50" r="46" stroke="#b8953a" strokeWidth="2" fill="none" />
    {/* Inner circle */}
    <circle cx="50" cy="50" r="40" stroke="#b8953a" strokeWidth="1" fill="none" />
    {/* Saltire (St. Andrew's cross) */}
    <line x1="50" y1="8" x2="50" y2="92" stroke="#b8953a" strokeWidth="3" />
    <line x1="8" y1="92" x2="92" y2="8" stroke="#b8953a" strokeWidth="3" />
    {/* Secondary saltire lines */}
    <line x1="8" y1="8" x2="92" y2="92" stroke="rgba(184,149,58,0.3)" strokeWidth="1" />
    <line x1="92" y1="8" x2="8" y2="92" stroke="rgba(184,149,58,0.3)" strokeWidth="1" />
    {/* Center diamond */}
    <polygon points="50,35 65,50 50,65 35,50" fill="none" stroke="#b8953a" strokeWidth="1.5" />
    {/* Text around circle */}
    <text x="50" y="22" textAnchor="middle" fill="#b8953a" fontSize="7" fontFamily="Georgia, serif" fontWeight="600" letterSpacing="1">KNIGHTS</text>
    <text x="50" y="86" textAnchor="middle" fill="#b8953a" fontSize="7" fontFamily="Georgia, serif" fontWeight="600" letterSpacing="1">ST ANDREW</text>
    {/* Small stars */}
    <text x="50" y="53" textAnchor="middle" fill="#b8953a" fontSize="10">★</text>
  </svg>
)
