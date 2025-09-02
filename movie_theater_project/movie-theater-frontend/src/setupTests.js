import { TextEncoder, TextDecoder } from 'util';
import '@testing-library/jest-dom';

// Polyfill for TextEncoder and TextDecoder
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
