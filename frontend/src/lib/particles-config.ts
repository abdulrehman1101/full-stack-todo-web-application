import { ISourceOptions } from "@tsparticles/engine";

export const particlesConfig: ISourceOptions = {
  fpsLimit: 120,
  particles: {
    color: {
      value: "#22d3ee", // cyan-400 - cyber glow color
    },
    links: {
      color: "#6366f1", // indigo-500 - cyber accent color
      distance: 150,
      enable: true,
      frequency: 1,
      opacity: 0.3,
    },
    move: {
      enable: true,
      outModes: {
        default: "bounce",
      },
      random: true,
      speed: 1,
      straight: false,
    },
    number: {
      density: {
        enable: true,
        area: 800,
      },
      value: 40,
    },
    opacity: {
      value: 0.5,
    },
    shape: {
      type: "circle",
    },
    size: {
      value: { min: 1, max: 3 },
    },
  },
  detectRetina: true,
  interactivity: {
    events: {
      onClick: {
        enable: true,
        mode: "push",
      },
      onHover: {
        enable: true,
        mode: "repulse",
      },
    },
    modes: {
      push: {
        quantity: 4,
      },
      repulse: {
        distance: 100,
        duration: 0.4,
      },
    },
  },
};

// Bubble atmosphere effect configuration
export const bubbleAtmosphereConfig: ISourceOptions = {
  ...particlesConfig,
  particles: {
    ...particlesConfig.particles,
    color: {
      value: ["#6366f1", "#22d3ee", "#8b5cf6"], // indigo-500, cyan-400, violet-400
    },
    move: {
      ...particlesConfig.particles.move,
      speed: 0.5,
    },
    size: {
      value: { min: 2, max: 5 },
    },
    opacity: {
      value: { min: 0.1, max: 0.4 },
      animation: {
        enable: true,
        speed: 0.5,
        minimumValue: 0.1,
        sync: false,
      },
    },
  },
  interactivity: {
    ...particlesConfig.interactivity,
    events: {
      ...particlesConfig.interactivity.events,
      onDiv: {
        elementId: "repulse-div",
        enable: true,
        mode: "bounce",
        type: "circle",
      },
    },
    modes: {
      ...particlesConfig.interactivity.modes,
      bubble: {
        distance: 200,
        duration: 2,
        mix: true,
        divs: {
          distance: 200,
          duration: 0.4,
          mix: true,
          selectors: "#bubble-div",
        },
      },
    },
  },
};