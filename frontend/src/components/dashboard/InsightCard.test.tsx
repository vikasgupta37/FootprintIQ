import React from 'react';
import { render, screen } from '@testing-library/react';
import { InsightCard } from './InsightCard';

describe('InsightCard', () => {
  it('renders standard title, description, and impact level', () => {
    render(
      <InsightCard
        title="Switch to Public Transit"
        description="Taking the metro twice a week reduces transport emissions."
        impact_level="High"
      />
    );

    expect(screen.getByText('Switch to Public Transit')).toBeInTheDocument();
    expect(screen.getByText('Taking the metro twice a week reduces transport emissions.')).toBeInTheDocument();
    expect(screen.getByText('High Impact')).toBeInTheDocument();
  });

  it('renders bar chart visualization data', () => {
    render(
      <InsightCard
        title="EV Savings"
        description="Simulated transition to electric vehicle"
        co2_saved={120}
        visualization={{
          chart_type: 'bar',
          metric_label: 'Monthly Emissions',
          before_value: 200,
          after_value: 80,
          unit: 'kg CO2'
        }}
      />
    );

    expect(screen.getByText('Monthly Emissions')).toBeInTheDocument();
    expect(screen.getByText('-120 kg CO2')).toBeInTheDocument();
    expect(screen.getByText('200 kg CO2')).toBeInTheDocument();
    expect(screen.getByText('80 kg CO2')).toBeInTheDocument();
  });

  it('renders progress chart visualization reduction percentages', () => {
    render(
      <InsightCard
        title="Reduce Plastic Waste"
        description="Switching to reusable bottles"
        visualization={{
          chart_type: 'progress',
          metric_label: 'Plastic waste',
          before_value: 100,
          after_value: 20,
          unit: 'units'
        }}
      />
    );

    expect(screen.getByText('Plastic waste')).toBeInTheDocument();
    // 100 to 20 is an 80% reduction
    expect(screen.getByText('-80%')).toBeInTheDocument();
  });
});
