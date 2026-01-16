'use client';

import { useEffect } from 'react';
import Particles from '@tsparticles/react';
import { useTheme } from 'next-themes';
import { bubbleAtmosphereConfig } from '@/src/lib/particles-config';

const ParticlesBackground = () => {
  const { theme } = useTheme();

  // Update particle colors based on theme
  const getParticleConfig = () => {
    if (theme === 'dark' || theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return bubbleAtmosphereConfig;
    }
    return bubbleAtmosphereConfig;
  };

  return (
    <div className="fixed inset-0 -z-10">
      <Particles
        id="tsparticles-background"
        options={getParticleConfig()}
      />
    </div>
  );
};

export default ParticlesBackground;