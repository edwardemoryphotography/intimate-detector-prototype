import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App.jsx';

describe('App', () => {
  it('renders upload button', () => {
    render(<App />);
    expect(screen.getByText(/Detect Areas/i)).toBeTruthy();
  });
});
