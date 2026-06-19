import { test, expect } from '@playwright/test';

test.describe('FootprintIQ Platform E2E Flow', () => {
  test('complete carbon footprint calculation flow', async ({ page }) => {
    // 1. Visit Login page
    await page.goto('/login');
    await expect(page.locator('h1')).toContainText(/Sign In/i);

    // Fill login credentials
    await page.fill('input[type="email"]', 'test@example.com');
    await page.fill('input[type="password"]', 'TestPass123!');
    
    // Check if the sign in button is present and click
    const submitButton = page.locator('button[type="submit"]');
    await expect(submitButton).toBeVisible();

    // 2. Navigate directly to dashboard/calculator
    await page.goto('/dashboard/calculator');
    
    // Wait for the calculator form to render
    const formTitle = page.locator('h2');
    await expect(formTitle).toContainText(/Carbon Footprint Calculator/i);

    // Fill transportation step
    await page.selectOption('select[name="vehicle_type"]', 'car_petrol');
    await page.fill('input[name="km_per_month"]', '600');
    
    // Click Next
    await page.click('button:has-text("Next")');

    // Fill energy step
    await page.fill('input[name="electricity_kwh_per_month"]', '350');
    await page.click('button:has-text("Next")');

    // Fill food step
    await page.selectOption('select[name="diet_type"]', 'vegetarian');
    await page.click('button:has-text("Next")');

    // Fill shopping step
    await page.fill('input[name="clothing_items_per_month"]', '2');
    await page.click('button:has-text("Next")');

    // Fill waste step
    await page.selectOption('select[name="recycling_frequency"]', 'often');
    
    // Click Calculate
    await page.click('button:has-text("Calculate")');

    // Verify result display
    await expect(page.locator('text=Your Carbon Footprint')).toBeVisible();
    await expect(page.locator('text=kg CO2e')).toBeVisible();
  });
});
