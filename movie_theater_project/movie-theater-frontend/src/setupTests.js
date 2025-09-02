// Polyfill for TextEncoder and TextDecoder
import { TextEncoder, TextDecoder } from 'util';

global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

// Suppress React Router warnings
const originalWarn = console.warn;
console.warn = (...args) => {
  if (
    args[0]?.includes('React Router Future Flag Warning') ||
    args[0]?.includes('Relative route resolution within Splat routes is changing')
  ) {
    return;
  }
  originalWarn(...args);
};

// Extend Jest with additional matchers
import '@testing-library/jest-dom';
