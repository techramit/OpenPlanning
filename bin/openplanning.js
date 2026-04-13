#!/usr/bin/env node

import { OpenPlanningCLI } from '../src/cli/OpenPlanningCLI.js';

const cli = new OpenPlanningCLI();
cli.run().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
